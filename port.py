import serial
 
try:
    pico_serial = serial.Serial('COM3', 9600, timeout=1)
    print("Serial connection established!")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")