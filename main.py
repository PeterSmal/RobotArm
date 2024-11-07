from machine import Pin, PWM, UART
import time
import select
import sys
import ujson
 
# Define constants for servo PWM control
pwm_frequency = 50     # Standard frequency for servos (50 Hz)
min_duty = 1000        # Minimum duty cycle for 0 degrees
max_duty = 9000        # Maximum duty cycle for 180 degrees
 
# LED and UART setup
led = Pin(25, Pin.OUT)  # Onboard LED setup for visual feedback
uart = UART(0, 9600)    # Initialize UART for serial communication (UART0 at 9600 baud)
 
# Set up the poll object to monitor UART input
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)
 
servo_pins = {
    "base": 16,         # Base rotation
    "lower_arm": 17,    # Lower arm
    "front_arm": 18,    # Front arm
    "wrist_tilt": 19,   # Wrist tilt
    "wrist_rotation": 20, # Wrist rotation
    "gripper": 21       # Gripper
}

# Initialize PWM objects for each servo
servos = {name: PWM(Pin(pin)) for name, pin in servo_pins.items()}
for servo in servos.values():
    servo.freq(pwm_frequency)

# Function to load servo positions from a file
position_file = "servo_positions.json"
def load_servo_positions():
    try:
        with open(position_file, 'r') as file:
            return ujson.load(file)
    except (OSError, ValueError):
        # Return default positions if the file doesn't exist or has invalid data
        return {name: 90 for name in servo_pins}

# Function to save servo positions to a file
def save_servo_positions():
    with open(position_file, 'w') as file:
        ujson.dump(servo_positions, file)

# Load previous servo positions or default to 90 degrees
servo_positions = load_servo_positions()

# Position definitions for the arm
def default_position():
    move_servo_by_name("base", 90, stop_delay=1, step_delay=0.05)
    move_servo_by_name("lower_arm", 100, stop_delay=1, step_delay=0.05)
    move_servo_by_name("front_arm", 110, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_tilt", 70, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05)
    move_servo_by_name("gripper", 60, stop_delay=1, step_delay=0.05)

def pickup_position():
    move_servo_by_name("lower_arm", 70, stop_delay=1, step_delay=0.05)
    move_servo_by_name("front_arm", 119, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05)
    move_servo_by_name("gripper", 110, stop_delay=1, step_delay=0.05)

def place_left():
    move_servo_by_name("lower_arm", 90, stop_delay=1, step_delay=0.05)
    move_servo_by_name("front_arm", 100, stop_delay=1, step_delay=0.05)
    move_servo_by_name("base", 160, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05)
    move_servo_by_name("gripper", 50, stop_delay=1, step_delay=0.05)

def pickup_position_2():
    move_servo_by_name("base", 90, stop_delay=1, step_delay=0.05)
    move_servo_by_name("lower_arm", 70, stop_delay=1, step_delay=0.05)
    move_servo_by_name("front_arm", 119, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05)
    move_servo_by_name("gripper", 110, stop_delay=1, step_delay=0.05)

def place_right():
    move_servo_by_name("lower_arm", 90, stop_delay=1, step_delay=0.05)
    move_servo_by_name("front_arm", 100, stop_delay=1, step_delay=0.05)
    move_servo_by_name("base", 10, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05)
    move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05)
    move_servo_by_name("gripper", 50, stop_delay=1, step_delay=0.05)

flashing = False  # LED control flag
print("Pico listening for UART commands...")

# Main loop to listen for UART commands
while True:
    poll_results = poll_obj.poll(1)
    if poll_results:
        data = sys.stdin.readline().strip()
        print("Received data:", data)

        if data == "start_left":
            print("Start command received for left placement")
            flashing = True
            default_position()
            pickup_position()
            place_left()
        
        elif data == "start_right":
            print("Start command received for right placement")
            flashing = True
            default_position()
            pickup_position()
            place_right()
        
        elif data == "stop":
            flashing = False
            led.off()  # Stop flashing LED immediately
            print("Stopping LED flashing and resetting robot arm.")
            default_position()
        
        else:
            print(f"Unknown command: {data}")

    # Flash LED if active
    if flashing:
        led.toggle()
        time.sleep(1.5)  # Adjust LED toggle interval
    else:
        led.off()

    time.sleep(0.1)

 
