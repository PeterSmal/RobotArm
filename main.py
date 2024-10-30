from machine import Pin, PWM, UART
import time
import select
import sys
 
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
 
# Servo pin mapping
servo_pins = {
    "base": 16,
    "lower_arm": 17,
    "front_arm": 18,
    "wrist_tilt": 19,
    "wrist_rotation": 20,
    "gripper": 21
}
 
# Function to convert angle to PWM duty cycle
def angle_to_duty_cycle(angle):
    return int((angle / 180) * (max_duty - min_duty) + min_duty)
 
# Robot Arm class
class RobotArm:
    def __init__(self):
        self.default_positions = {
            "base": 90,
            "lower_arm": 80,
            "front_arm": 70,
            "wrist_tilt": 80,
            "wrist_rotation": 140,
            "gripper": 60
        }
        self.pickup_positions = {
            "base": 160,
            "lower_arm": 90,
            "front_arm": 25,
            "wrist_tilt": 140,
            "wrist_rotation": 140,
            "gripper": 110
        }
        self.place_positions = {
            "base": 135,
            "lower_arm": 90,
            "front_arm": 70,
            "wrist_tilt": 90,
            "wrist_rotation": 140,
            "gripper": 60
        }
        self.move_to_default_position(step_delay=0.05)
 
    # Move to a specific servo angle with a step delay for smooth movement
    def move_servo_by_name(self, name, target_angle, stop_delay=1, step_delay=0.02, step_size=1):
        if name in servo_pins:
            servo_pin = servo_pins[name]
            servo = PWM(Pin(servo_pin))
            servo.freq(pwm_frequency)
            current_angle = self.default_positions.get(name, 90)
            while abs(current_angle - target_angle) > step_size:
                current_angle += step_size if current_angle < target_angle else -step_size
                servo.duty_u16(angle_to_duty_cycle(current_angle))
                time.sleep(step_delay)
            servo.duty_u16(angle_to_duty_cycle(target_angle))
            time.sleep(stop_delay)
            servo.deinit()
            print(f"Servo '{name}' moved to {target_angle} degrees.")
 
    # Move to positions
    def move_to_default_position(self, step_delay=0.02):
        print("Moving to default position...")
        for name, angle in self.default_positions.items():
            self.move_servo_by_name(name, angle, step_delay=step_delay)
        # Ensure gripper remains open when moving to default position
 
    def move_to_pickup_position(self, step_delay=0.02):
        print("Moving to pickup position...")
        for name in ["base", "lower_arm", "front_arm", "wrist_tilt", "wrist_rotation"]:  # Exclude gripper
            self.move_servo_by_name(name, self.pickup_positions[name], step_delay=step_delay)
        # The gripper remains open until explicitly closed in pick_up_object
 
    def move_to_place_position(self, step_delay=0.02):
    print("Moving to place position...")
    self.move_servo_by_name("front_arm", self.place_positions["front_arm"], step_delay=step_delay)
    for name in ["lower_arm", "wrist_tilt", "wrist_rotation", "base"]:
        if name in self.place_positions:
            self.move_servo_by_name(name, self.place_positions[name], step_delay=step_delay)
    # Move gripper to open position only at the end of placing object
    self.move_servo_by_name("gripper", self.place_positions["gripper"], step_delay=step_delay)
 
    # Pick and place operations
    def pick_up_object(self, step_delay=0.02):
        self.move_to_pickup_position(step_delay=step_delay)
        print("Picking up object...")
        self.move_servo_by_name("gripper", 110, stop_delay=2, step_delay=step_delay)  # Close gripper here, as last step

    def place_object(self, step_delay=0.02):
        self.move_to_place_position(step_delay=step_delay)
        print("Placing object...")
        self.move_servo_by_name("gripper", 60, stop_delay=2, step_delay=step_delay)  # Open gripper after placing object
 
# Initialize RobotArm instance
arm = RobotArm()
flashing = False  # LED control flag
 
print("Pico listening for UART commands...")
 
# Main loop
while True:
    # Check for UART commands
    poll_results = poll_obj.poll(1)
    if poll_results:
        data = sys.stdin.readline().strip()
        print("Received data:", data)
        if data == "start":
            flashing = True
            print("Starting LED flashing and robot operation...")
            arm.pick_up_object(step_delay=0.05)
            arm.place_object(step_delay=0.05)
            arm.move_to_default_position(step_delay=0.05)
 
        elif data == "stop":
            flashing = False
            led.off()  # Stop flashing LED immediately
            print("Stopping LED flashing and resetting robot arm.")
            arm.move_to_default_position(step_delay=0.05)
 
        else:
            print(f"Unknown command: {data}")
 
    # Flash LED if active
    if flashing:
        led.toggle()
        time.sleep(1.5)  # Adjust LED toggle interval
    else:
        led.off()
 
    time.sleep(0.1)