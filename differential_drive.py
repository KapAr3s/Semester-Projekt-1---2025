from stepper_motor import StepperMotor
import uasyncio as asyncio
import time
import math

class DifferentialDrive:
    def __init__(self, left, right):
        """
        Initialize the navigation system with two stepper motors.

        :param left: Instance of StepperMotor class for the left motor.
        :param right: Instance of StepperMotor class for the right motor.
        """

        self.left = left
        self.right = right
        self.stop()

    def stop(self):
        self.left.stop()
        self.right.stop()
        
    def move_stepper(self, cycles, direction, delay_us=1000):
        """
        Move the stepper motor a specified number of steps.

        :param cycles: Number of cycles(4 steps) to move. Positive for forward, negative for backward.
        :param direction: Direction to move. "forward" for forward, "backward" for backward.
        :param delay_us: Delay between steps in microseconds.
        """
    
        if direction == "forward":
            sequence = self.sequence
        elif direction == "backward":
            sequence = list(reversed(self.sequence))
        else:
            raise ValueError("Direction must be 'forward' or 'backward'")
        
        for cycle in range(cycles):
            for step in sequence:
                self.left.set_step(step)
                self.right.set_step(step)
                time.sleep_us(delay_us)

    def run(self, motor, steps):
        motor.move_stepper(steps)

    def drive(self, left_steps, right_steps, delay_us):
        self.left.move_stepper(left_steps, delay_us)

    def forward(self, steps, delay_us=1000):
        """
        Move both motors forward a specified number of steps.
        :param steps: Number of steps to move forward.
        :param delay_us: Delay between steps in microseconds.
        """
        self.drive(steps, steps, delay_us)
        self.stop()

    def backward(self, steps, delay_us=1000):
        """
        Move both motors backward a specified number of steps.
        :param steps: Number of steps to move backward.
        :param delay_us: Delay between steps in microseconds.
        """
        self.drive(-steps, -steps, delay_us)
        self.stop()

    def mm_to_steps(self, distance_mm):
        """
        Convert a distance in centimeters to the corresponding number of motor steps.
        :param distance_cm: Distance to move in centimeters.
        :return: Number of steps corresponding to the given distance.
        """
        
        wheel_diameter_mm = 85
        steps_per_revolution = 200
        steps_per_sequence = 4
        
        circumference = wheel_diameter_mm*math.pi
        distance_per_step = (steps_per_sequence/steps_per_revolution)*circumference
        steps = distance_mm / distance_per_step
        steps = round(steps)
        return steps
    
    def degrees_to_steps(self, degrees, turning_radius_mm):
        '''
        Convert a degree to number of steps to turn.
        :param degrees (int): degrees to turn
        :param turning_radius_mm (int): turning radius in mm
        :return (int): number of steps
        '''
        #240 mm from wheel to wheel
        #120 mm from wheel to the centre between the two wheels
        wheel_diameter_mm = 85
        steps_per_revolution = 200
        steps_per_sequence = 4
    
        wheel_circumference_mm = math.pi * wheel_diameter_mm
        turning_circumference_mm = 2 * math.pi * turning_radius_mm

        distance_per_wheel_mm = (degrees / 360) * turning_circumference_mm
        revolutions = distance_per_wheel_mm / wheel_circumference_mm
        total_steps = self.mm_to_steps(distance_per_wheel_mm)
        return total_steps

    def move_distance(self, distance_mm, direction, delay_us=1000):
        """
        Move the robot forward or backward a specific distance in centimeters.

        :param distance_cm: Distance to move in centimeters.
        :param direction: Direction to move, either 'forward' or 'backward'.
        :param delay_us: Delay between steps in microseconds.
        """

        steps = self.mm_to_steps(distance_mm)

        self.move_stepper(steps, direction, delay_us)

        self.stop()
        
    def turn_in_place(self, degrees, direction, delay_us=1000):
        """
        Turn the robot a specific number of degrees.

        :param degrees: The angle in degrees to turn.
        :param direction: Direction to turn, either 'left' or 'right'.
        :param delay_us: Delay between steps in microseconds.
        """
        
        steps = self.degrees_to_steps(degrees, 120)

        if direction == "left":
            # Left wheel moves backward, right wheel moves forward
            for step in range(steps):
                for n in range(len(self.sequence)):
                    self.left.set_step(self.sequence[-(n+1)])
                    self.right.set_step(self.sequence[n])
                    time.sleep_us(delay_us)
           
        elif direction == "right":
            # Right wheel moves backward, left wheel moves forward
            for step in range(steps):
                for n in range(len(self.sequence)):
                    self.left.set_step(self.sequence[n])
                    self.right.set_step(self.sequence[-(n+1)])
                    time.sleep_us(delay_us)
        else:
            raise ValueError("Direction must be 'left' or 'right'")

        self.stop()