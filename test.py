'''from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)

while True:
    led.toggle()
    sleep(0.5)'''

import serial
import time
 
try:
    pico_serial = serial.Serial('COM5', 9600, timeout=1)  # Ensure COM5 matches your Pico's port
    time.sleep(2)  # Wait for the connection to establish
    pico_serial.write(b'start\n')  # Send 'start' command
    print("Sent 'start' command")
    time.sleep(10)  # Wait and observe the Pico LED
    pico_serial.write(b'stop\n')  # Send 'stop' command
    print("Sent 'stop' command")
except Exception as e:
    print(f"Error: {e}")
finally:
    if pico_serial.is_open:
        pico_serial.close()
        print("Serial connection closed.")