from flask import Flask, request, jsonify
import serial
 
app = Flask(__name__)
 
# Initialize pico_serial to None globally
pico_serial = None
 
# Function to initialize serial connection
def initialize_serial():
    global pico_serial
    if pico_serial is None or not pico_serial.is_open:
        try:
            # Replace COM3 with the correct port number
            pico_serial = serial.Serial('COM3', 9600, timeout=1)
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
 
# Flask hook: Ensure serial connection before every request
@app.before_request
def ensure_serial_connection():
    initialize_serial()
 
@app.route('/control', methods=['GET'])
def control():
    global pico_serial  # Access the global variable
 
    # Check if the serial connection was established
    if pico_serial is None or not pico_serial.is_open:
        return jsonify({"error": "Serial port not available"}), 500
 
    command = request.args.get('cmd')
 
    if command == 'start':
        pico_serial.write(b'start\n')  # Send 'start' command to Pico
        return jsonify({"status": "Robot arm started"}), 200
    elif command == 'stop':
        pico_serial.write(b'stop\n')  # Send 'stop' command to Pico
        return jsonify({"status": "Robot arm stopped"}), 200
    else:
        return jsonify({"error": "Invalid command"}), 400
 
# Route to manually close the serial connection
@app.route('/close_serial', methods=['GET'])
def close_serial():
    global pico_serial
    if pico_serial is not None and pico_serial.is_open:
        pico_serial.close()
        print("Serial connection closed!")
        return jsonify({"status": "Serial connection closed"}), 200
    else:
        return jsonify({"error": "Serial port not open"}), 400
 
# Ensure the serial port is closed properly when the app shuts down
@app.teardown_appcontext
def shutdown_serial_connection(exception=None):
    global pico_serial
    if pico_serial is not None and pico_serial.is_open:
        pico_serial.close()
        print("Serial connection closed during app shutdown")
 
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)  # Run Flask on port 5001
    except Exception as e:
        print(f"Flask app encountered an error: {e}")
    finally:
        # Ensure serial port is closed when the Flask app terminates
        if pico_serial is not None and pico_serial.is_open:
            pico_serial.close()
            print("Serial connection closed during Flask shutdown")
 