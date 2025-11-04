from stepper_motor import StepperMotor
from differential_drive import DifferentialDrive
import time

# LED pinout 16, 17, 18, 19, 20, 21, 22, 26
# motor pinout left: 0, 1, 2, 3 og right: 4, 5, 6, 7
left_motor = StepperMotor([16, 17, 18, 19], pwm_pct=0.7, frequency=16_000)
right_motor = StepperMotor([20, 21, 22, 26], pwm_pct=0.7, frequency=16_000)

robot = DifferentialDrive(left_motor, right_motor)
robot.forward(1)

#robot.forward(1)
#robot.move_distance(267, "forward")
#print(robot.degrees_to_steps(360, 120))

#robot.move_distance(1000, "backward", 500)
#robot.move_distance(1000, "forward", delay_us=1)
#robot.turn_in_place(360, "left", delay_us=1)