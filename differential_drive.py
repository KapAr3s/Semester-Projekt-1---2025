from stepper_motor import StepperMotor
from machine import Timer
import time
import math

tim = Timer()

STEPS_PER_REVOLUTION = 200
WHEEL_DIAMETER_MM = 85
CIRCUMFERENCE_MM = WHEEL_DIAMETER_MM * math.pi
STEP_DISTANCE_MM = CIRCUMFERENCE_MM / STEPS_PER_REVOLUTION
WHEEL_BASE_MM = 240
WHEEL_BASE_CIRCUMFERENCE_MM = WHEEL_BASE_MM * math.pi
WHEEL_BASE_CIRCUMFERENCE_STEPS = WHEEL_BASE_CIRCUMFERENCE_MM / STEP_DISTANCE_MM

class DifferentialDrive:
    STATUS_IDLE = 0 
    STATUS_JOB = 1
    def __init__(self, left = StepperMotor([0,1,2,3]), right = StepperMotor([4,5,6,7])):
        """
        Initialize the navigation system with two stepper motors.

        :param left: Instance of StepperMotor class for the left motor.
        :param right: Instance of StepperMotor class for the right motor.
        """
        self.left = left
        self.right = right
        self.max_odometer = 0
        self.set_speed(0,0)

        self.status = DifferentialDrive.STATUS_IDLE

    def set_speed(self, left_speed, right_speed):
        tim.deinit()
        # the direction of travel is in this case reveresed from the way stepper motor class is designed.
        self.left.set_speed(-left_speed) 
        self.right.set_speed(-right_speed)
        tim.init(period=1, mode=Timer.PERIODIC, callback=self.drive)

    def drive(self, timer):
        self.left.step()
        self.right.step()
        if self.max_odometer > 0 and max(self.left.odometer, self.right.odometer) >= self.max_odometer:
            self.set_speed(0,0)
            self.max_odometer = 0
            self.status = DifferentialDrive.STATUS_IDLE

    def destroy(self):
        tim.deinit()
        self.set_speed(0,0)
        self.drive(None)

    def move_steps(self, steps, left_speed, right_speed = None):
        self.status = DifferentialDrive.STATUS_JOB
        self.left.odometer = 0
        self.right.odometer = 0
        self.max_odometer = steps
        if right_speed == None:
            right_speed = left_speed 
        self.set_speed(left_speed, right_speed)
    
    def move_distance_mm(self, distance_mm, left_speed, right_speed = None):
        steps = round(distance_mm / STEP_DISTANCE_MM)
        self.move_steps(steps, left_speed, right_speed)
                    
    def turn_in_place(self, degrees, speed = 1):
        """
        Turn the robot a specific number of degrees.

        :param degrees: The angle in degrees to turn.
        :param speed: How fast can it go round?
        """
        if degrees < 0:
            speed = -speed

        steps = abs(round(WHEEL_BASE_CIRCUMFERENCE_STEPS * degrees / 360))
        self.move_steps(steps, left_speed=speed, right_speed= -speed)

    def accelerate(self, terminal_speed):
        # no neeed to "slowly" accelerate to speed 7 
        if abs(terminal_speed) <= 7:
            self.set_speed(terminal_speed, terminal_speed)
        else:
            direction = 1
            if terminal_speed < 0:
                direction = -1
            for i in range(7, abs(terminal_speed)+1):
                self.set_speed(i*direction, i*direction)
                time.sleep_us(100000) #0.1 seconds 