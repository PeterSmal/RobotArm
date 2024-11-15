from machine import Pin, PWM, UART
import time
import select
import sys
import ujson

# Constants for servo control
pwm_frequency = 50
min_duty = 1000
max_duty = 9000

# LED and UART setup
led = Pin(25, Pin.OUT)
uart = UART(0, 9600)

# Poll object for UART input
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

servo_pins = {
    "base": 16, "lower_arm": 17, "front_arm": 18,
    "wrist_tilt": 19, "wrist_rotation": 20, "gripper": 21
}

position_file = "servo_positions.json"

# Initialize PWM objects for each servo
servos = {name: PWM(Pin(pin)) for name, pin in servo_pins.items()}
for servo in servos.values():
    servo.freq(pwm_frequency)

def angle_to_duty_cycle(angle):
    return int((angle / 180) * (max_duty - min_duty) + min_duty)

def load_servo_positions():
    try:
        with open(position_file, 'r') as file:
            return ujson.load(file)
    except (OSError, ValueError):
        return {name: 90 for name in servo_pins}

def save_servo_positions():
    with open(position_file, 'w') as file:
        ujson.dump(servo_positions, file)

servo_positions = load_servo_positions()

def move_servo_by_name(name, target_angle, stop_delay=1, step_delay=0.02):
    if name in servos:
        servo = servos[name]
        current_angle = servo_positions[name]
        step = 1 if target_angle > current_angle else -1
        for angle in range(current_angle, target_angle + step, step):
            servo.duty_u16(angle_to_duty_cycle(angle))
            time.sleep(step_delay)
        servo_positions[name] = target_angle
        save_servo_positions()
        time.sleep(stop_delay)
        print(f"Servo '{name}' moved to {target_angle} degrees.")
    else:
        print(f"Error: Servo '{name}' not found.")

# Default sequences
def default_position():
    move_servo_by_name("base", 90)
    move_servo_by_name("lower_arm", 100)
    move_servo_by_name("front_arm", 110)
    move_servo_by_name("wrist_tilt", 70)
    move_servo_by_name("wrist_rotation", 80)
    move_servo_by_name("gripper", 60)

def pickup_position():
    move_servo_by_name("lower_arm", 70)
    move_servo_by_name("front_arm", 119)
    move_servo_by_name("wrist_tilt", 20)
    move_servo_by_name("wrist_rotation", 80)
    move_servo_by_name("gripper", 110)

# Car sequence
def place_car():
    move_servo_by_name("lower_arm", 90)
    move_servo_by_name("front_arm", 100)
    move_servo_by_name("base", 160)
    move_servo_by_name("wrist_tilt", 20)
    move_servo_by_name("wrist_rotation", 80)
    move_servo_by_name("gripper", 50)

# Motorbike sequence
def place_motorcycle():
    move_servo_by_name("lower_arm", 90)
    move_servo_by_name("front_arm", 100)
    move_servo_by_name("base", 10)
    move_servo_by_name("wrist_tilt", 20)
    move_servo_by_name("wrist_rotation", 80)
    move_servo_by_name("gripper", 50)
    
# Aeroplane sequence
def place_aeroplane():
    move_servo_by_name("lower_arm", 90)
    move_servo_by_name("front_arm", 100)
    move_servo_by_name("base", 45)
    move_servo_by_name("wrist_tilt", 20)
    move_servo_by_name("wrist_rotation", 80)
    move_servo_by_name("gripper", 50)

# Classes for different detections
class CarMovement:
    @staticmethod
    def execute():
        print("Executing car movement...")
        default_position()
        pickup_position()
        place_car()
        default_position()

<<<<<<< HEAD
# Example usage of the methods
#default_position()
#pickup_position()
#place_left()
#pickup_position_2()
#place_right()

# Clean up and deactivate PWM for all servos
for servo in servos.values():
    servo.deinit()

flashing = False  # LED control flag
 
=======
class AeroplaneMovement:
    @staticmethod
    def execute():
        print("Executing aeroplane movement...")
        default_position()
        pickup_position()
        place_aeroplane()
        default_position()

class MotorcycleMovement:
    @staticmethod
    def execute():
        print("Executing motorbike movement...")
        default_position()
        pickup_position()
        place_motorcycle()
        default_position()

# Flashing status for LED control
flashing = False

>>>>>>> b57f04e38cb95d91248718bac72143cdee208fcf
print("Pico listening for UART commands...")

while True:
    poll_results = poll_obj.poll(1)
    if poll_results:
        data = sys.stdin.readline().strip()
        print("Received data:", data)
        
        if data == "car":
            flashing = True
<<<<<<< HEAD
            print("Starting LED flashing and robot operation...")
            default_position()
            pickup_position()
            place_left()
            pickup_position_2()
            place_right()
 
=======
            CarMovement.execute()
            flashing = False

        elif data == "airplane":
            flashing = True
            AeroplaneMovement.execute()
            flashing = False

        elif data == "motorcycle":
            flashing = True
            MotorcycleMovement.execute()
            flashing = False

>>>>>>> b57f04e38cb95d91248718bac72143cdee208fcf
        elif data == "stop":
            flashing = False
            led.off()
            print("Stopping LED flashing and resetting robot arm.")
<<<<<<< HEAD
            default_position()
 
=======
        
>>>>>>> b57f04e38cb95d91248718bac72143cdee208fcf
        else:
            print(f"Unknown command: {data}")
    
    if flashing:
        led.toggle()
        time.sleep(1.5)
    else:
        led.off()
    
    time.sleep(0.1)
