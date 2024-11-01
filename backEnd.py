import serial
from flask import Flask, Response, request, jsonify, render_template
import cv2
from object_detection import ObjectDetection

app = Flask(__name__)

# Initialize global variables
object_detector = ObjectDetection('./yolo-Weights/yolov8n.pt')
pico_serial = None
object_detection_active = False

@app.route('/')
def index():
    return render_template('app.html')

def generate_frames():
    global object_detection_active, pico_serial
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Run object detection if enabled
            if object_detection_active:
                img, detected_objects = object_detector.detect_objects(frame)
                
                # Check if target object is detected
                target_detected = any(obj['name'] == 'car','motorbike' for obj in detected_objects)
                
                if target_detected and pico_serial and pico_serial.is_open:
                    pico_serial.write(b'start\n')
                    print("Object detected, sending 'start' command to Pico")
                    object_detection_active = False  # Stop detection after initial trigger

            else:
                img = frame  # If detection not active, show normal frame

            # Encode and yield frame for streaming
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['GET'])
def control():
    global pico_serial, object_detection_active
    command = request.args.get('cmd')

    if command == 'start':
        object_detection_active = True
        print("Object detection activated by start button.")
        return jsonify({"status": "Object detection started"}), 200

    elif command == 'stop':
        object_detection_active = False
        print("Stopping object detection and robot arm.")
        send_command_to_pico("stop")
        return jsonify({"status": "Object detection and robot arm stopped"}), 200

    else:
        print(f"Invalid command received: {command}")
        return jsonify({"error": "Invalid command"}), 400

def send_command_to_pico(command):
    global pico_serial
    if pico_serial is None:
        try:
            pico_serial = serial.Serial(port="COM5", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
            pico_serial.flush()
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")
            return

    if pico_serial.is_open:
        pico_serial.write(f"{command}\n".encode())
        print(f"Sent '{command}' command to Pico.")

# Ensure the serial port is closed properly when the app shuts down
@app.teardown_appcontext
def shutdown_serial_connection(exception=None):
    global pico_serial
    if pico_serial is not None and pico_serial.is_open:
        pico_serial.close()
        print("Serial connection closed during app shutdown")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=False)
    finally:
        if pico_serial and pico_serial.is_open:
            pico_serial.close()
            print("Serial connection closed on app exit.")



 
