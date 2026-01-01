import time
from stepper_motor import StepperMotor
from differential_drive import DifferentialDrive
from  LDR import I2C_ADS_LDR

left = StepperMotor([0,1,2,3],0.50)
right = StepperMotor([4,5,6,7],0.50)
diff_drive = DifferentialDrive(left, right)

adc = I2C_ADS_LDR(0x48,[0,3,4,7])

accelerated = False
acc_left = False
acc_left2 = False 
acc_right = False
acc_right2 = False 
lLDR = 0
rLDR = 0

# for i in range(11):
#   diff_drive.set_speed(i, -i)
#   print(left.speed)
#   time.sleep(2)

# for _ in range(4):
#   diff_drive.move_distance_mm(500, 8)
#   while diff_drive.status == diff_drive.STATUS_JOB:
#     time.sleep(0.1)
#   diff_drive.turn_in_place(-90, 6)
#   while diff_drive.status == diff_drive.STATUS_JOB:
#     time.sleep(0.1)

diff_drive.set_speed(2,2)
time.sleep(0.1)
diff_drive.set_speed(4,4)
time.sleep(0.1)

while True:
    lLDR = adc.read_one(4)
    rLDR = adc.read_one(3)
    print([lLDR,rLDR])
    
    if lLDR < 80 and rLDR < 80:
        if not accelerated:
            diff_drive.accelerate(10)
            accelerated = True
            acc_left = False
            acc_left2 = False 
            acc_right = False
            acc_right2 = False 
    elif lLDR < 80:
        if not acc_left:
            diff_drive.set_speed(10,9)
            accelerated = False 
            acc_left = True 
            acc_right = False
            acc_right2 = False
            time.sleep(0.1)
        if not acc_left2:
            diff_drive.set_speed(10,8)
            acc_left2 = True 
    elif  rLDR < 80:
        if not acc_right:
            diff_drive.set_speed(9,10)
            accelerated = False 
            acc_left = False 
            acc_left2 = False 
            acc_right = True
            time.sleep(0.1)
        if not acc_right2:
            diff_drive.set_speed(8,10)
            acc_right2 = True


    



