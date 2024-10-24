import machine
import time

# Set up pins for robot arm motors (this will depend on your actual motor setup)
shoulder_motor = machine.Pin(2, machine.Pin.OUT)  # Example GPIO for shoulder motor
elbow_motor = machine.Pin(3, machine.Pin.OUT)     # Example GPIO for elbow motor

# Set up pin for the gripper (servo motor)
gripper_servo = machine.PWM(machine.Pin(15))
gripper_servo.freq(50)

# UART (serial communication) setup to listen for commands from Flask backend
uart = machine.UART(0, 9600)

# Function to move the robot arm to a specified angle
def move_arm(shoulder_angle, elbow_angle):
    # Example motor control logic
    shoulder_motor.on()  # Example motor movement, customize for your hardware
    elbow_motor.on()     # Example motor movement, customize for your hardware
    print(f"Moving arm to Shoulder: {shoulder_angle}°, Elbow: {elbow_angle}°")

# Function to control the gripper (open/close)
def open_gripper():
    gripper_servo.duty_u16(3000)  # Adjust for your servo's open position
    print("Gripper opened")

def close_gripper():
    gripper_servo.duty_u16(7000)  # Adjust for your servo's closed position
    print("Gripper closed")

# Main loop to listen for serial commands from the Flask backend
while True:
    if uart.any():
        command = uart.read().decode().strip()
        
        if command == 'start':
            # Perform a pick-and-place operation
            move_arm(90, 45)  # Example movement to a pick-up position
            time.sleep(1)
            close_gripper()  # Close the gripper to grab the object
            time.sleep(1)
            move_arm(45, 90)  # Example movement to a place position
            time.sleep(1)
            open_gripper()  # Open the gripper to release the object

        elif command == 'stop':
            # Stop the robot arm and open the gripper
            shoulder_motor.off()
            elbow_motor.off()
            open_gripper()
            print("Robot arm stopped")
        
    time.sleep(0.1)  # Small delay
