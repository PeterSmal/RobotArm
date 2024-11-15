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

'''def generate_frames():
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

                # Initialize detected_class as None
                detected_class = None

                # Check for target objects (car, motorbike, aeroplane) and send corresponding command
                for obj in detected_objects:
                    if obj.get('class') in ['car', 'motorcycle', 'airplane']:
                        detected_class = obj.get('class')
                        break  # Exit loop after first valid target is found

                # If target detected, send specific command to Pico and stop detection
                if detected_class:
                    print(f"Target object '{detected_class}' detected, checking serial connection to send command...")
                    if pico_serial:
                        if pico_serial.is_open:
                            pico_serial.write(f'{detected_class}\n'.encode())  # Send the detected class to Pico
                            print(f"Sent '{detected_class}' command to Pico.")
                            object_detection_active = False  # Stop detection after initial trigger
                        else:
                            print("Error: Serial port is not open.")
                    else:
                        print("Error: pico_serial is None, unable to send command.")

                    # Reset detected_class after sending the command to avoid re-sending the same command
                    detected_class = None  # Clear detected_class to allow for future detections

            else:
                img = frame  # If detection not active, show normal frame

            # Encode and yield frame for streaming
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()'''

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

                # Initialize detected_class as None
                detected_class = None

                # Check for target objects (car, motorbike, aeroplane) and send corresponding command
                for obj in detected_objects:
                    if obj.get('class') in ['car', 'motorcycle', 'airplane']:
                        detected_class = obj.get('class')
                        break  # Exit loop after first valid target is found

                # If target detected, send specific command to Pico
                if detected_class:
                    print(f"Target object '{detected_class}' detected, checking serial connection to send command...")
                    if pico_serial:
                        if pico_serial.is_open:
                            pico_serial.write(f'{detected_class}\n'.encode())  # Send the detected class to Pico
                            print(f"Sent '{detected_class}' command to Pico.")
                        else:
                            print("Error: Serial port is not open.")
                    else:
                        print("Error: pico_serial is None, unable to send command.")

                    # Pause detection briefly to allow sequence completion, then restart
                    print("Pausing detection briefly to allow sequence completion...")
                    object_detection_active = False
                    cv2.waitKey(32000)  # Wait for 15 seconds (adjust based on sequence duration)
                    print("Resuming detection...")
                    object_detection_active = True

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
        pico_serial = serial.Serial(port="COM8", baudrate=9600, timeout=1)
        pico_serial.flush()
        print("Serial connection established on COM8.")
        app.run(host='0.0.0.0', port=5001, debug=False)
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
    finally:
        if pico_serial and pico_serial.is_open:
            pico_serial.close()
            print("Serial connection closed on app exit.")








 
