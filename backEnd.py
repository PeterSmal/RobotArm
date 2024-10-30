from flask import Flask, Response, request, jsonify, render_template
import serial
import time
import cv2
from robot_arm_classes import RobotArm  # Import your RobotArm class
from object_detection import ObjectDetection

app = Flask(__name__)
pico_serial = None
object_detection_active = False
robot_arm = RobotArm()  # Initialize the robot arm globally

# Initialize object detection model
object_detector = ObjectDetection('./yolo-Weights/yolov8n.pt')

# Function to initialize serial connection
def initialize_serial():
    global pico_serial
    if pico_serial is None or not pico_serial.is_open:
        try:
            pico_serial = serial.Serial('COM5', 9600, timeout=1)
            print("Serial connection established!")
        except serial.SerialException as e:
            if "Access is denied" in str(e):
                print("Error: Access to the serial port was denied. Try running as administrator or checking if the port is in use.")
            else:
                print(f"Error opening serial port: {e}")
            pico_serial = None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            pico_serial = None

initialize_serial()

@app.route('/')
def index():
    return render_template('app.html')

# Video stream with object detection integration, controlled by start button
def generate_frames():
    global object_detection_active
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Run object detection only if the start command has been issued
            if object_detection_active:
                results = object_detector.detect_objects(frame)

                # Check if a target object is detected
                target_detected = False
                for obj in results:
                    if obj['name'] in ['car', 'motorbike', 'aeroplane']:  # Change to your target objects
                        target_detected = True
                        break

                # If target object detected, send start command to Pico and move robot arm
                if target_detected:
                    if pico_serial and pico_serial.is_open:
                        pico_serial.write(b'start\n')
                        print("Object detected, sending 'start' command to Pico")

                    # Execute pick-up and place sequence
                    robot_arm.pick_up_object(step_delay=0.05)
                    robot_arm.place_object(step_delay=0.05)
                    robot_arm.move_to_default_position(step_delay=0.05)

                    # Stop further detection after action
                    object_detection_active = False

            # Display the frame with or without detection
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
        object_detection_active = True  # Activate object detection
        print("Object detection activated by start button.")
        return jsonify({"status": "Object detection started"}), 200

    elif command == 'stop':
        object_detection_active = False  # Stop object detection
        if pico_serial.is_open:
            pico_serial.write(b'stop\n')
            print("Sent 'stop' command to Pico.")
        return jsonify({"status": "Object detection and robot arm stopped"}), 200

    else:
        print(f"Invalid command received: {command}")
        return jsonify({"error": "Invalid command"}), 400

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

 
