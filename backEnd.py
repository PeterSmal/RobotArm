from flask import Flask, request, jsonify
import serial
from robot_arm_classes import RobotArm, Gripper, Controller
import time

app = Flask(__name__)

# Initialize serial communication with Pico
pico_serial = None

def initialize_serial():
    global pico_serial
    if pico_serial is None or not pico_serial.is_open:
        try:
            pico_serial = serial.Serial('COM3', 9600, timeout=1)  # Adjust COM port as needed
            print("Serial connection established!")
        except serial.SerialException as e:
            if "Access is denied" in str(e):
                print("Error: Access to the serial port was denied. Try running as administrator or checking if the port is in use.")
            else:
                print(f"Error opening serial port: {e}")
            pico_serial = None
        except Exception as e:
            print(f"Unexpected error: {e}")
            pico_serial = None

@app.before_request
def ensure_serial_connection():
    initialize_serial()

# Initialize robot arm and gripper
L1 = 10  # Length of the first arm segment
L2 = 10  # Length of the second arm segment
robot_arm = RobotArm(L1, L2)
gripper = Gripper(pin=15)  # Assuming the gripper is connected to Pin 15
controller = Controller(robot_arm, gripper)

@app.route('/control', methods=['GET'])
def control():
    global pico_serial
    if pico_serial is None or not pico_serial.is_open:
        return jsonify({"error": "Serial port not available"}), 500

    command = request.args.get('cmd')

    if command == 'start':
        # Perform a simple pick-and-place operation (can customize further)
        controller.pick_and_place(pick_x=15, pick_y=10, place_x=25, place_y=5)
        return jsonify({"status": "Robot arm started with pick-and-place"}), 200
    elif command == 'stop':
        pico_serial.write(b'stop\n')  # Stop the current motion
        gripper.open()  # Open the gripper as part of the stop command
        return jsonify({"status": "Robot arm stopped and gripper opened"}), 200
    else:
        return jsonify({"error": "Invalid command"}), 400

@app.route('/close_serial', methods=['GET'])
def close_serial():
    global pico_serial
    if pico_serial is not None and pico_serial.is_open:
        pico_serial.close()
        print("Serial connection closed!")
        return jsonify({"status": "Serial connection closed"}), 200
    else:
        return jsonify({"error": "Serial port not open"}), 400

@app.teardown_appcontext
def shutdown_serial_connection(exception=None):
    global pico_serial
    if pico_serial is not None and pico_serial.is_open:
        pico_serial.close()
        print("Serial connection closed during app shutdown")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)
    finally:
        if pico_serial is not None and pico_serial.is_open:
            pico_serial.close()
            print("Serial connection closed during Flask shutdown")
