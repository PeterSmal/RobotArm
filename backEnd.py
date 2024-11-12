'''import serial
from flask import Flask, Response, request, jsonify, render_template
import cv2
from object_detection import ObjectDetection
import time

app = Flask(__name__)

# Initialize global variables
object_detector = ObjectDetection('./yolo-Weights/yolov8n.pt')
pico_serial = None  # Set initially to None for lazy initialization
object_detection_active = False

@app.route('/')
def index():
    return render_template('app.html')

# Function to generate video frames
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
                # Debugging: Print the structure and contents of detected_objects
                print("Detected objects:", detected_objects)
 
                # Check if target object is detected
                try:
                    target_detected = any(obj.get('name') in ['car', 'motorbike'] for obj in detected_objects)
                except KeyError as e:
                    print(f"KeyError: {e}. Ensure 'name' is a valid key in detected_objects.")
                    target_detected = False  # Fallback if structure doesn't match
 
                # If target detected, send start signal to Pico
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

# Function to send commands to Pico
def send_command_to_pico(command):
    global pico_serial
    if pico_serial is None:
        try:
            pico_serial = serial.Serial(port="COM5", baudrate=9600, timeout=1)
            time.sleep(2)  # Allow time for connection to establish
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
            print("Serial connection closed on app exit.")'''

'''from flask import Flask, Response, render_template, request, jsonify
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
                # Print out detected objects for debugging
                print("Detected objects:", detected_objects)
 
                # Check if target object is detected
                try:
                    target_detected = any(obj.get('class') in ['car', 'motorbike', 'aeroplane'] for obj in detected_objects)
                    print("Target detected:", target_detected)  # Debugging: Check if target is detected
                except KeyError as e:
                    print(f"KeyError: {e}. Ensure 'name' is a valid key in detected_objects.")
                    target_detected = False  # Fallback if structure doesn't match
 
                # If target detected, send start signal to Pico and stop detection
                if target_detected:
                    print("Target object detected, checking serial connection to send 'start' command...")
                    if pico_serial:
                        if pico_serial.is_open:
                            pico_serial.write(b'start\n')
                            print("Object detected, sending 'start' command to Pico")
                            object_detection_active = False  # Stop detection after initial trigger
                        else:
                            print("Error: Serial port is not open.")
                    else:
                        print("Error: pico_serial is None, unable to send 'start' command.")
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
            print("Serial connection closed on app exit.")'''

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
                # Print out detected objects for debugging
                print("Detected objects:", detected_objects)

                # Check for target objects (car, motorbike, aeroplane) and send corresponding command
                detected_class = None
                for obj in detected_objects:
                    if obj.get('class') in ['car', 'motorbike', 'aeroplane']:
                        detected_class = obj.get('class')
                        break

                # If target detected, send specific command to Pico and stop detection
                if detected_class:
                    print(f"Target object '{detected_class}' detected, checking serial connection to send command...")
                    if pico_serial:
                        if pico_serial.is_open:
                            pico_serial.write(f'{detected_class}\n'.encode())
                            print(f"Sent '{detected_class}' command to Pico.")
                            object_detection_active = False  # Stop detection after initial trigger
                        else:
                            print("Error: Serial port is not open.")
                    else:
                        print("Error: pico_serial is None, unable to send command.")
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








 
