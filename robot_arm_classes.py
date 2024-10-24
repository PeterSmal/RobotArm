import math
import machine
import time

class RobotArm:
    def __init__(self, L1, L2):
        self.L1 = L1  # Length of the first arm segment
        self.L2 = L2  # Length of the second arm segment

    def inverse_kinematics(self, x, y):
        """Calculate joint angles for a given (x, y) position."""
        # Calculate theta2 (elbow joint)
        cos_theta2 = (x**2 + y**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        cos_theta2 = min(1, max(-1, cos_theta2))  # Ensure cos_theta2 is within valid range
        theta2 = math.acos(cos_theta2)

        # Calculate theta1 (shoulder joint)
        theta1 = math.atan2(y, x) - math.atan2(self.L2 * math.sin(theta2), self.L1 + self.L2 * math.cos(theta2))

        # Convert radians to degrees for easier control
        return math.degrees(theta1), math.degrees(theta2)

    def move_arm(self, theta1, theta2):
        """Send commands to move the robot arm to the calculated angles."""
        # Placeholder for the actual motor control code
        print(f"Moving arm to Shoulder angle: {theta1:.2f}°, Elbow angle: {theta2:.2f}°")
        # Here, you'd include motor control logic to set the motors to theta1 and theta2

    def move_to_position(self, x, y):
        """Calculate the joint angles and move the arm to the (x, y) position."""
        theta1, theta2 = self.inverse_kinematics(x, y)
        self.move_arm(theta1, theta2)


class Gripper:
    def __init__(self, pin):
        """Initialize the gripper servo motor."""
        self.servo = machine.PWM(machine.Pin(pin))  # Servo connected to specified pin
        self.servo.freq(50)

    def open(self):
        """Open the gripper."""
        self.servo.duty_u16(3000)  # Adjust based on your servo's open position
        print("Gripper opened")

    def close(self):
        """Close the gripper."""
        self.servo.duty_u16(7000)  # Adjust based on your servo's closed position
        print("Gripper closed")


class Controller:
    def __init__(self, robot_arm, gripper):
        """Initialize the controller with a RobotArm and Gripper instance."""
        self.robot_arm = robot_arm
        self.gripper = gripper

    def pick_and_place(self, pick_x, pick_y, place_x, place_y):
        """Perform the full pick-and-place operation."""
        # Move to the pick-up position
        print("Moving to pick-up position...")
        self.robot_arm.move_to_position(pick_x, pick_y)
        time.sleep(1)  # Wait for the arm to move into position

        # Close the gripper to pick up the object
        self.gripper.close()
        time.sleep(1)

        # Move to the place position
        print("Moving to place position...")
        self.robot_arm.move_to_position(place_x, place_y)
        time.sleep(1)

        # Open the gripper to release the object
        self.gripper.open()
        time.sleep(1)
