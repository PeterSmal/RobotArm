from flask import Flask, Response, request, jsonify, render_template
import serial
import time

from object_detection import ObjectDetection
import cv2


app = Flask(__name__)

object_detector = ObjectDetection('./yolo-Weights/yolov8n.pt')
 
# Initialize pico_serial to None globally
pico_serial = None
object_detection_active = False  # New flag to control object detection
 
# Function to initialize serial connection
def initialize_serial():
    global pico_serial
    if pico_serial is None or not pico_serial.is_open:
        try:
            # Replace COM3 with the correct port number
            pico_serial = serial.Serial('COM5', 9600, timeout=1)
            print("Serial connection established!")
        except serial.SerialException as e:
            if "Access is denied" in str(e):
                print("Error: Access to the serial port was denied. Try running as administrator or checking if the port is in use.")
            else:
                print(f"Error opening serial port: {e}")
            pico_serial = None  # Set to None if serial connection failed
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            pico_serial = None

# Run the serial initialization outside of Flask's lifecycle
initialize_serial()

# Serve the HTML file at the root URL
@app.route('/')
def index():
    return render_template('app.html')

# Video stream with object detection integration, controlled by start button
def generate_frames():
    global object_detection_active
    cap = cv2.VideoCapture(0)  # Open camera (index 0 for default camera)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
             # Activate object detection if start is pressed
            if object_detection_active:
                img, detected_objects = object_detector.detect_objects(frame)
                for obj in detected_objects:
                    if obj['name'] in ['Car', 'Motorbike','Aeroplane']:
                        print("Object detected:", obj['name'])
                        robot_arm.pick_up_object()
                        robot_arm.place_object()
                        object_detection_active = False
                        break
            else:
                img = frame

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
 
 
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Control route to handle start and stop commands
@app.route('/control', methods=['GET'])
def control():
    global pico_serial, object_detection_active
    command = request.args.get('cmd')

    if pico_serial is None or not pico_serial.is_open:
        print("Serial port is not available or closed.")
        return jsonify({"error": "Serial port not available"}), 500

    if command == 'start':
        object_detection_active = True  # Start object detection
        print("Object detection activated by start button.")
        return jsonify({"status": "Object detection started"}), 200

    elif command == 'stop':
        object_detection_active = False  # Stop object detection
        if pico_serial.is_open:
            pico_serial.write(b'stop\n')  # Send stop command to Pico
            print("Sent 'stop' command to Pico.")
        return jsonify({"status": "Object detection and robot arm stopped"}), 200

    else:
        print(f"Invalid command received: {command}")
        return jsonify({"error": "Invalid command"}), 400

# Route to manually close the serial connection
@app.route('/close_serial', methods=['GET'])
def close_serial():
    global pico_serial
    if pico_serial and pico_serial.is_open:
        pico_serial.close()
        print("Serial connection manually closed!")
        return jsonify({"status": "Serial connection manually closed"}), 200
    else:
        return jsonify({"error": "Serial port is not open"}), 400
    
#http://127.0.0.1:5001/close_serial

 
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
        if pico_serial is not None and pico_serial.is_open:
            pico_serial.close()
            print("Serial connection closed during Flask shutdown")
 
