import machine
import time
import sys

led = machine.Pin(25, machine.Pin.OUT)  # Example action: control onboard LED

while True:
    if sys.stdin.read() == 'start':
        led.on()  # Action to control the robot arm
        print("Robot arm started")
    elif sys.stdin.read() == 'stop':
        led.off()
        print("Robot arm stopped")
    time.sleep(0.1)