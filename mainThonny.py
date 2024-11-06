from machine import Pin, PWM
import time
import ujson

# Servo pin mapping
servo_pins = {
    "base": 16,         # Base rotation
    "lower_arm": 17,    # Lower arm
    "front_arm": 18,    # Front arm
    "wrist_tilt": 19,   # Wrist tilt
    "wrist_rotation": 20, # Wrist rotation
    "gripper": 21       # Gripper
}

pwm_frequency = 50     # Standard frequency for servos (50 Hz)
min_duty = 1000        # Minimum duty cycle for 0 degrees
max_duty = 9000        # Maximum duty cycle for 180 degrees
position_file = "servo_positions.json"

# Initialize PWM objects for each servo
servos = {name: PWM(Pin(pin)) for name, pin in servo_pins.items()}
for servo in servos.values():
    servo.freq(pwm_frequency)

# Function to convert angle to PWM duty cycle
def angle_to_duty_cycle(angle):
    return int((angle / 180) * (max_duty - min_duty) + min_duty)

# Function to load servo positions from a file
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

# Function to move the servo to a specified angle gradually
def move_servo_by_name(name, target_angle, stop_delay=1, step_delay=0.02):
    if name in servos:
        servo = servos[name]
        current_angle = servo_positions[name]  # Get the stored current angle

        # Determine direction of movement
        step = 1 if target_angle > current_angle else -1

        # Gradually move to target angle
        for angle in range(current_angle, target_angle + step, step):
            servo.duty_u16(angle_to_duty_cycle(angle))
            time.sleep(step_delay)  # Delay between each incremental movement

        # Update and save the stored current angle
        servo_positions[name] = target_angle
        save_servo_positions()  # Save updated positions to the file
        
        # Stop delay to allow the servo to reach the angle
        time.sleep(stop_delay)
        print(f"Servo '{name}' moved to {target_angle} degrees.")
    else:
        print(f"Error: Servo '{name}' not found.")

# Example usage: Move each servo to a specific angle directly
#move_servo_by_name("base", 90, stop_delay=1, step_delay=0.05) #160 is completely left, 10 right
#move_servo_by_name("lower_arm", 60, stop_delay=1, step_delay=0.05) #30 completely front, 150 backwards
#move_servo_by_name("front_arm", 130, stop_delay=1, step_delay=0.05) #10 back,130 front
#move_servo_by_name("wrist_tilt", 80, stop_delay=1, step_delay=0.05) #10 to the ground, 150 back
#move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05) #80 is straight
#move_servo_by_name("gripper", 50, stop_delay=1, step_delay=0.05) #100 is closed,50 is open

#default
#move_servo_by_name("base", 90, stop_delay=1, step_delay=0.05) #160 is completely left, 10 right
#move_servo_by_name("lower_arm", 100, stop_delay=1, step_delay=0.05) #30 completely front, 150 backwards
#move_servo_by_name("front_arm", 110, stop_delay=1, step_delay=0.05) #10 back,130 front
#move_servo_by_name("wrist_tilt", 70, stop_delay=1, step_delay=0.05) #10 to the ground, 150 back
#move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05) #80 is straight
#move_servo_by_name("gripper", 60, stop_delay=1, step_delay=0.05) #100 is closed,50 is open

#pickup position
#move_servo_by_name("lower_arm", 70, stop_delay=1, step_delay=0.05) #30 completely front, 150 backwards
#move_servo_by_name("front_arm", 119, stop_delay=1, step_delay=0.05) #10 back,130 front
#move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05) #10 to the ground, 150 back
#move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05) #80 is straight
#move_servo_by_name("gripper", 110, stop_delay=1, step_delay=0.05) #1100 is closed,50 is open

#place sequence left
#move_servo_by_name("lower_arm", 90, stop_delay=1, step_delay=0.05) #30 completely front, 150 backwards
#move_servo_by_name("front_arm", 100, stop_delay=1, step_delay=0.05) #10 back,130 front
#move_servo_by_name("base", 160, stop_delay=1, step_delay=0.05) #160 is completely left, 10 right
#move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05) #10 to the ground, 150 back
#move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05) #80 is straight
#move_servo_by_name("gripper", 50, stop_delay=1, step_delay=0.05) #1100 is closed,50 is open

#pickup 2
#move_servo_by_name("base", 90, stop_delay=1, step_delay=0.05) #160 is completely left, 10 right
#move_servo_by_name("lower_arm", 70, stop_delay=1, step_delay=0.05) #30 completely front, 150 backwards
#move_servo_by_name("front_arm", 119, stop_delay=1, step_delay=0.05) #10 back,130 front
#move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05) #10 to the ground, 150 back
#move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05) #80 is straight
#move_servo_by_name("gripper", 110, stop_delay=1, step_delay=0.05) #1100 is closed,50 is open

#place sequence right
#move_servo_by_name("lower_arm", 90, stop_delay=1, step_delay=0.05) #30 completely front, 150 backwards
#move_servo_by_name("front_arm", 100, stop_delay=1, step_delay=0.05) #10 back,130 front
#move_servo_by_name("base", 10, stop_delay=1, step_delay=0.05) #160 is completely left, 10 right
#move_servo_by_name("wrist_tilt", 20, stop_delay=1, step_delay=0.05) #10 to the ground, 150 back
#move_servo_by_name("wrist_rotation", 80, stop_delay=1, step_delay=0.05) #80 is straight
#move_servo_by_name("gripper", 50, stop_delay=1, step_delay=0.05) #1100 is closed,50 is open

# Define methods for each movement sequence
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

# Example usage of the methods
default_position()
pickup_position()
place_left()
pickup_position_2()
place_right()




# Clean up and deactivate PWM for all servos
for servo in servos.values():
    servo.deinit()