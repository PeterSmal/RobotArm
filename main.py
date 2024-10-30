import machine
import time
from robot_arm import RobotArm  # Assuming robot_arm.py defines your RobotArm class

# Initialize onboard LED (Pin 25 on Pico) to visualize actions
led = machine.Pin(25, machine.Pin.OUT)

# Initialize UART for serial communication (UART0 at 9600 baud)
uart = machine.UART(0, 9600)

# Initialize RobotArm instance
arm = RobotArm()

print("Pico listening for UART commands...")
time.sleep(1)  # Allow time for the Pico to initialize

# Default position on startup
arm.move_to_default_position()

while True:
    if uart.any():
        # Read command from UART
        command = uart.read().decode().strip()
        
        if command == 'start':
            led.on()  # Turn on LED to signal "start" action
            print("Received 'start' command: LED turned on")
            
            # Execute the pick-up and place sequence
            arm.move_to_default_position()  # Ensure the arm is in the default position
            arm.pick_up_object()            # Pick up object if detected
            arm.place_object()              # Place object
            arm.move_to_default_position()  # Return to default position after placing

        elif command == 'stop':
            led.off()  # Turn off LED to signal "stop" action
            print("Received 'stop' command: LED turned off")
            arm.move_to_default_position()  # Move arm to default position on stop

        else:
            print(f"Received unknown command: {command}")

    time.sleep(0.1)  # Small delay to prevent overloading