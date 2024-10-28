import machine
import time
 
# Initialize onboard LED (Pin 25 on Pico)
led = machine.Pin(25, machine.Pin.OUT)
 
# Initialize UART for serial communication (UART0 at 9600 baud)
uart = machine.UART(0, 9600)
 
print("Pico listening for UART commands...")
time.sleep(1)  # Give the Pico some time to start up
 
while True:
    if uart.any():
        # Read the command sent via UART
        command = uart.read().decode().strip()
        # Check command and perform action
        if command == 'start':
            led.on()  # Turn on the LED or start the robot arm
            print("Received 'start' command: LED turned on")
 
        elif command == 'stop':
            led.off()  # Turn off the LED or stop the robot arm
            print("Received 'stop' command: LED turned off")
 
        else:
            print(f"Received unknown command: {command}")
 
    time.sleep(0.1)  # Small delay to avoid overloading