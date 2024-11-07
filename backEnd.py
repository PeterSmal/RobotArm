from flask import Flask, Response, render_template, request, jsonify
import cv2
import serial
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
            print("Error: Could not read frame from camera.")
            break
        else:
            # Run object detection if enabled
            if object_detection_active:
                img, detected_objects = object_detector.detect_objects(frame)
                # Print detected objects for debugging
                print("Detected objects:", detected_objects)

                # Check if target object is detected
                try:
                    car_detected = any(obj.get('class') == 'car' for obj in detected_objects)
                    motorbike_detected = any(obj.get('class') == 'motorbike' for obj in detected_objects)
                    aeroplane_detected = any(obj.get('class') == 'aeroplane' for obj in detected_objects)
                    
                    # Debugging: Check if target detected
                    print("Car detected:", car_detected)
                    print("Motorbike detected:", motorbike_detected)
                    print("Aeroplane detected:", aeroplane_detected)

                except KeyError as e:
                    print(f"KeyError: {e}. Ensure 'class' is a valid key in detected_objects.")
                    car_detected = motorbike_detected = aeroplane_detected = False

                # Send the appropriate command based on detection
                if car_detected or motorbike_detected:
                    print("Car or Motorbike detected, preparing to send 'place_left' command to Pico...")
                    if pico_serial and pico_serial.is_open:
                        pico_serial.write(b'place_left\n')
                        print("Sent 'place_left' command to Pico for car or motorbike")
                        object_detection_active = False  # Stop detection after command
                    else:
                        print("Error: Serial port not open or pico_serial is None.")
                elif aeroplane_detected:
                    print("Aeroplane detected, preparing to send 'place_right' command to Pico...")
                    if pico_serial and pico_serial.is_open:
                        pico_serial.write(b'place_right\n')
                        print("Sent 'place_right' command to Pico for aeroplane")
                        object_detection_active = False  # Stop detection after command
                    else:
                        print("Error: Serial port not open or pico_serial is None.")

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
        object_detection_active = True  # Start object detection
        print("Object detection activated by start button.")
        return jsonify({"status": "Object detection started"}), 200

    elif command == 'stop':
        object_detection_active = False  # Stop object detection
        print("Sent 'stop' command to Pico.")
        if pico_serial and pico_serial.is_open:
            pico_serial.write(b'stop\n')
        return jsonify({"status": "Object detection and robot arm stopped"}), 200

    else:
        print(f"Invalid command received: {command}")
        return jsonify({"error": "Invalid command"}), 400

if __name__ == '__main__':
    try:
        pico_serial = serial.Serial(port="COM5", baudrate=9600, timeout=1)
        pico_serial.flush()
        print("Serial connection established on COM5.")
        app.run(host='0.0.0.0', port=5001, debug=False)
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
    finally:
        if pico_serial and pico_serial.is_open:
            pico_serial.close()
            print("Serial connection closed on app exit.")




 
