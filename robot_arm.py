'''from machine import Pin, PWM
import time
 
# Define constants for servo PWM control
pwm_frequency = 50     # Standard frequency for servos (50 Hz)
min_duty = 1000        # Minimum duty cycle for 0 degrees
max_duty = 9000        # Maximum duty cycle for 180 degrees
 
# Servo pin mapping
servo_pins = {
    "base": 16,         # Base rotation
    "lower_arm": 17,    # Lower arm
    "front_arm": 18,    # Front arm
    "wrist_tilt": 19,   # Wrist tilt
    "wrist_rotation": 20, # Wrist rotation
    "gripper": 21       # Gripper
}
 
# Function to convert angle to PWM duty cycle
def angle_to_duty_cycle(angle):
    return int((angle / 180) * (max_duty - min_duty) + min_duty)
 
# Robot Arm class
class RobotArm:
    def __init__(self):
        # Initialize servos to default positions on startup
        self.default_positions = {
            "base": 90,          # Base neutral
            "lower_arm": 90,     # Lower arm neutral
            "front_arm": 90,     # Front arm neutral
            "wrist_tilt": 90,    # Wrist tilt neutral
            "wrist_rotation": 140, # Wrist rotation neutral
            "gripper": 60        # Gripper open
        }
        self.pickup_positions = {
            "base": 160,          # Position to align with pickup
            "lower_arm": 90,    # Lower arm for pickup
            "front_arm": 25,    # Adjust front arm for reach
            "wrist_tilt": 140,    # Keep wrist level
            "wrist_rotation": 140, # Wrist neutral
            "gripper": 110       # Gripper closed for pickup
        }
        self.place_positions = {
            "base": 135,         # Position to align with placement area
            "lower_arm": 90,     # Lower arm adjusted for placement
            "front_arm": 70,    # Adjust front arm for reach
            "wrist_tilt": 90,    # Keep wrist level
            "wrist_rotation": 140, # Wrist neutral
            "gripper": 60        # Gripper open to release object
        }
 
        # Move arm to default position at startup with a step delay
        self.move_to_default_position(step_delay=0.05)
 
    # Function to move a single servo to a specific angle with a step delay
    def move_servo_by_name(self, name, target_angle, stop_delay=1, step_delay=0.02, step_size=1):
        if name in servo_pins:
            servo_pin = servo_pins[name]
            servo = PWM(Pin(servo_pin))
            servo.freq(pwm_frequency)
 
            # Get the current angle (start at default if not previously set)
            current_angle = self.default_positions.get(name, 90)
            # Smoothly step from current to target angle
            while abs(current_angle - target_angle) > step_size:
                # Incrementally move towards the target
                current_angle += step_size if current_angle < target_angle else -step_size
                servo.duty_u16(angle_to_duty_cycle(current_angle))
                time.sleep(step_delay)
 
            # Set final position to target
            servo.duty_u16(angle_to_duty_cycle(target_angle))
            time.sleep(stop_delay)
            servo.deinit()
            print(f"Servo '{name}' on pin {servo_pin} moved to {target_angle} degrees.")
        else:
            print(f"Error: Servo '{name}' not found.")
 
    # Move to default position
    def move_to_default_position(self, step_delay=0.02):
        print("Moving to default position...")
        for name, angle in self.default_positions.items():
            self.move_servo_by_name(name, angle, stop_delay=1, step_delay=step_delay)
 
    # Move to pickup position
    def move_to_pickup_position(self, step_delay=0.02):
        print("Moving to pickup position...")
        for name, angle in self.pickup_positions.items():
            self.move_servo_by_name(name, angle, stop_delay=1, step_delay=step_delay)
 
    # Move to place position
    def move_to_place_position(self, step_delay=0.02):
        print("Moving to place position...")
        for name, angle in self.place_positions.items():
            self.move_servo_by_name(name, angle, stop_delay=1, step_delay=step_delay)
 
    # Function to pick up an object
    def pick_up_object(self, step_delay=0.02):
        self.move_to_pickup_position(step_delay=step_delay)
        print("Picking up object...")
        self.move_servo_by_name("gripper", 110, stop_delay=2, step_delay=step_delay)  # Close gripper
        time.sleep(1)
 
    # Function to place an object
    def place_object(self, step_delay=0.02):
        self.move_to_place_position(step_delay=step_delay)
        print("Placing object...")
        self.move_servo_by_name("gripper", 60, stop_delay=2, step_delay=step_delay)   # Open gripper
        time.sleep(1)
 
 
# Example usage of RobotArm
arm = RobotArm()
 
# Execute pick-and-place sequence with smoother movements
arm.pick_up_object(step_delay=0.05)
time.sleep(1)
arm.place_object(step_delay=0.05)'''
#arm.move_to_default_position(step_delay=0.05)

#move_servo(serv0_pin, 160) 15 - 160
#move_servo(serv1_pin, 90) #40 - 150
#move_servo(serv2_pin, 25) #10 -150 (front)
#move_servo(serv3_pin, 140) #10 - 140
#move_servo(serv4_pin, 80) 10 (20 is horizontal) - 140 (80 is vert) 
#move_servo(serv5_pin, 60) open 60 close 110

from machine import Pin, PWM
import time
 
# Define constants for servo PWM control
pwm_frequency = 50     # Standard frequency for servos (50 Hz)
min_duty = 1000        # Minimum duty cycle for 0 degrees
max_duty = 9000        # Maximum duty cycle for 180 degrees
 
# Servo pin mapping
servo_pins = {
    "base": 16,         # Base rotation
    "lower_arm": 17,    # Lower arm
    "front_arm": 18,    # Front arm
    "wrist_tilt": 19,   # Wrist tilt
    "wrist_rotation": 20, # Wrist rotation
    "gripper": 21       # Gripper
}
 
# Function to convert angle to PWM duty cycle
def angle_to_duty_cycle(angle):
    return int((angle / 180) * (max_duty - min_duty) + min_duty)
 
# Robot Arm class
class RobotArm:
    def __init__(self):
        # Initialize servos to default positions on startup
        self.default_positions = {
            "base": 90,          # Base neutral
            "lower_arm": 90,     # Lower arm neutral
            "front_arm": 90,     # Front arm neutral
            "wrist_tilt": 90,    # Wrist tilt neutral
            "wrist_rotation": 140, # Wrist rotation neutral
            "gripper": 60        # Gripper open
        }
        self.pickup_positions = {
            "base": 160,         # Position to align with pickup
            "lower_arm": 90,     # Lower arm for pickup
            "front_arm": 25,     # Adjust front arm for reach
            "wrist_tilt": 140,   # Keep wrist level
            "wrist_rotation": 140, # Wrist neutral
            "gripper": 110       # Gripper closed for pickup
        }
        self.place_positions = {
            "base": 135,         # Position to align with placement area
            "lower_arm": 90,     # Lower arm adjusted for placement
            "front_arm": 70,     # Adjust front arm for reach
            "wrist_tilt": 90,    # Keep wrist level
            "wrist_rotation": 140, # Wrist neutral
            "gripper": 60        # Gripper open to release object
        }
 
        # Move arm to default position at startup with a step delay
        self.move_to_default_position(step_delay=0.05)
 
    # Function to move a single servo to a specific angle with a step delay
    def move_servo_by_name(self, name, target_angle, stop_delay=1, step_delay=0.02, step_size=1):
        if name in servo_pins:
            servo_pin = servo_pins[name]
            servo = PWM(Pin(servo_pin))
            servo.freq(pwm_frequency)
 
            # Get the current angle (start at default if not previously set)
            current_angle = self.default_positions.get(name, 90)
            # Smoothly step from current to target angle
            while abs(current_angle - target_angle) > step_size:
                # Incrementally move towards the target
                current_angle += step_size if current_angle < target_angle else -step_size
                servo.duty_u16(angle_to_duty_cycle(current_angle))
                time.sleep(step_delay)
 
            # Set final position to target
            servo.duty_u16(angle_to_duty_cycle(target_angle))
            time.sleep(stop_delay)
            servo.deinit()
            print(f"Servo '{name}' on pin {servo_pin} moved to {target_angle} degrees.")
        else:
            print(f"Error: Servo '{name}' not found.")
 
    # Move to default position
    def move_to_default_position(self, step_delay=0.02):
        print("Moving to default position...")
        for name, angle in self.default_positions.items():
            self.move_servo_by_name(name, angle, stop_delay=1, step_delay=step_delay)
 
    # Move to pickup position
    def move_to_pickup_position(self, step_delay=0.02):
        print("Moving to pickup position...")
        for name, angle in self.pickup_positions.items():
            self.move_servo_by_name(name, angle, stop_delay=1, step_delay=step_delay)
 
    # Move to place position with front arm movement first
    def move_to_place_position(self, step_delay=0.02):
        print("Moving to place position...")
        # Move front arm first
        self.move_servo_by_name("front_arm", self.place_positions["front_arm"], stop_delay=1, step_delay=step_delay)
        
        # Then move other servos in desired order
        for name in ["lower_arm", "wrist_tilt", "wrist_rotation", "base"]:
            if name in self.place_positions:
                self.move_servo_by_name(name, self.place_positions[name], stop_delay=1, step_delay=step_delay)
        
        # Open the gripper last to release the object
        self.move_servo_by_name("gripper", self.place_positions["gripper"], stop_delay=2, step_delay=step_delay)
 
    # Function to pick up an object
    def pick_up_object(self, step_delay=0.02):
        self.move_to_pickup_position(step_delay=step_delay)
        print("Picking up object...")
        self.move_servo_by_name("gripper", 110, stop_delay=2, step_delay=step_delay)  # Close gripper
        time.sleep(1)
 
    # Function to place an object
    def place_object(self, step_delay=0.02):
        self.move_to_place_position(step_delay=step_delay)
        print("Placing object...")
        self.move_servo_by_name("gripper", 60, stop_delay=2, step_delay=step_delay)   # Open gripper
        time.sleep(1)
 
 
# Example usage of RobotArm
arm = RobotArm()
 
# Execute pick-and-place sequence with smoother movements
arm.pick_up_object(step_delay=0.05)
time.sleep(1)
arm.place_object(step_delay=0.05)