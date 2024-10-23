import machine
import time
 
led = machine.Pin(25, machine.Pin.OUT)  # Using onboard LED for demonstration
uart = machine.UART(0, 9600)  # UART0 for serial communication
 
while True:
    if uart.any():
        command = uart.read().decode().strip()  # Read the command from serial input
        if command == 'start':
            led.on()  # Replace with your robot arm start logic
            print("Robot arm started")
        elif command == 'stop':
            led.off()  # Replace with your robot arm stop logic
            print("Robot arm stopped")
    time.sleep(0.1)  # Small delay to prevent overloading