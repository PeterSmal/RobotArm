from flask import Flask, Response, request, jsonify, render_template
import serial
import time

from object_detection import ObjectDetection
import cv2
from object_detection import ObjectDetection


object_detection = ObjectDetection()
object_detector = ObjectDetection('./yolo-Weights/yolov8n.pt')
 
# Initialize pico_serial to None globally
pico_serial = None
 
# Function to initialize serial connection
def initialize_serial():
    global pico_serial
    if pico_serial is None or not pico_serial.is_open:
        try:
            # Replace COM3 with the correct port number
            pico_serial = serial.Serial('COM2', 9600, timeout=1)
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

app = Flask(__name__)

# Flask hook: Ensure serial connection before every request
@app.before_request
def ensure_serial_connection():
    initialize_serial()

# Serve the HTML file at the root URL
@app.route('/')
def index():
    return render_template('app.html')

def generate_frames():
    cap = cv2.VideoCapture(0)  # Open the camera (index 0 for default camera)
   
    while True:
        success, frame = cap.read()  # Capture frame-by-frame
        if not success:
            break  # If frame capture fails, break out of the loop
        else:
            # Pass the captured frame to the detect_objects() method
            img, detected_objects = object_detector.detect_objects(frame)  # Pass the frame here
 
            # Encode the frame in JPEG format for streaming
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
 
            # Yield the frame in byte format for streaming to the frontend
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
    cap.release()  # Release the camera when done
 
 
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['GET'])
def control():
    global pico_serial
    # Fetch the command from the URL parameters
    command = request.args.get('cmd')
 
    # Check if the serial connection was established
    if pico_serial is None or not pico_serial.is_open:
        print("Serial port is not available or closed.")
        return jsonify({"error": "Serial port not available"}), 500
 
    # Ensure the command is valid
    if command not in ['start', 'stop']:
        print(f"Invalid command received: {command}")
        return jsonify({"error": "Invalid command"}), 400
 
    try:
        # Send the command to the Pico via UART
        pico_serial.write(f"{command}\n".encode())  # Send 'start' or 'stop' with a newline
        print(f"Sent '{command}' command to Pico")
 
        # Respond with a success message
        return jsonify({"status": f"Robot arm {command}ed"}), 200
    except Exception as e:
        print(f"Error sending command to Pico: {e}")
        return jsonify({"error": "Failed to send command"}), 500
 

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
 
