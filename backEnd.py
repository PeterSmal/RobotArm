from flask import Flask, request
import serial

app = Flask(__name__)

# Replace with your Pico's serial port
pico_serial = serial.Serial('/dev/ttyUSB0', 9600)

@app.route('/control', methods=['GET'])
def control():
    command = request.args.get('cmd')
    if command == 'start':
        pico_serial.write(b'start\n')  # Send 'start' command to Pico
        return {"status": "started"}, 200
    elif command == 'stop':
        pico_serial.write(b'stop\n')  # Send 'stop' command to Pico
        return {"status": "stopped"}, 200
    return {"error": "invalid command"}, 400

if __name__ == "__main__":
    app.run(debug=True)