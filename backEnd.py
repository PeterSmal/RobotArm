from flask import Flask, request, jsonify
import serial
 
app = Flask(__name__)
 
# Try opening the serial port with exception handling
try:
    pico_serial = serial.Serial('COM3', 9600, timeout=1)
    print("Serial connection established!")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    pico_serial = None
 
@app.route('/control', methods=['GET'])
def control():
    command = request.args.get('cmd')
 
    if pico_serial is None:
        return jsonify({"error": "Serial port not available"}), 500
 
    if command == 'start':
        pico_serial.write(b'start\n')
        return jsonify({"status": "Robot arm started"}), 200
    elif command == 'stop':
        pico_serial.write(b'stop\n')
        return jsonify({"status": "Robot arm stopped"}), 200
    else:
        return jsonify({"error": "Invalid command"}), 400
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Run Flask on port 5001
 