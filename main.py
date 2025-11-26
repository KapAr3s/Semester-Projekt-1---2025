import time
from stepper_motor2 import StepperMotor
from differential_drive import DifferentialDrive

left = StepperMotor([0,1,2,3])
right = StepperMotor([4,5,6,7])
diff_drive = DifferentialDrive(left, right)

# for i in range(11):
#   diff_drive.set_speed(i, -i)
#   print(left.speed)
#   time.sleep(1)

for _ in range(4):
  diff_drive.move_distance_mm(500, 9)
  while diff_drive.status == diff_drive.STATUS_JOB:
    time.sleep(0.1)
  diff_drive.turn_in_place(-90, 6)
  while diff_drive.status == diff_drive.STATUS_JOB:
    time.sleep(0.1)


diff_drive.destroy()