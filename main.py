import time
from stepper_motor import StepperMotor
from differential_drive import DifferentialDrive
from LDR import I2C_ADS_LDR
from servo_magnet import ServoMagnet

left = StepperMotor([0,1,2,3])
right = StepperMotor([4,5,6,7])
diff_drive = DifferentialDrive(left, right)
magnet = ServoMagnet()

adc = I2C_ADS_LDR(0x48,[0,3,4,7])

bolt_count = 0
fail6 = False
circle = 0

diff_drive.move_distance_mm(100,5,5)
while diff_drive.status == diff_drive.STATUS_JOB:
    time.sleep(0.1)
   
def follow_line(subj,differntial_drive):
    if subj == [0,1,1,0]:
        differntial_drive.set_speed(7, 7)
        #print("forward")
    elif subj == [0,1,0,0]:
        differntial_drive.set_speed(0, 7)
        #print("left")
    elif subj == [0,0,1,0]:
        differntial_drive.set_speed(7, 0)    

def function1():
    diff_drive.destroy()
    global bolt_count
    notDone = True
    diff_drive.set_speed(7,7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        #print(adc.read_all())
        follow_line(subject,diff_drive)
        
        if subject[0]==1:
            print("mark seen")
            if subject[3]==1:
                return None
            else:
                diff_drive.move_distance_mm(5,5,5)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)
                if subject[0]==1 and subject[3]==1:
                    return None
                else:
                    diff_drive.move_distance_mm(5,5,5)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.5)
                    print("Magnet time bby :D")
                    magnet.pickup()
                    diff_drive.turn_in_place(15,5)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.1)
                    bolt_count += 1
                
                    
                    
            
def function2():
    print("func 2")
    global bolt_count
    diff_drive.move_distance_mm(80,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.turn_in_place(90,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(200,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    notDone = True
    diff_drive.set_speed(7,7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        #print(adc.read_all())
        follow_line(subject,diff_drive)
        
        if subject[0]==1:
            print("mark seen")
            if subject[3]==1:
                return None
            else:
                diff_drive.move_distance_mm(5,5,5)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.3)
                if subject[0]==1 and subject[3]==1:
                    return None
                else:
                    diff_drive.move_distance_mm(5,5,5)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.5)
                    print("Magnet time bby :D")
                    magnet.pickup()
                    diff_drive.turn_in_place(15,5)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.1)
                    bolt_count += 1
                    
        
def function3():
    print("func3")
    global bolt_count
    diff_drive.move_distance_mm(80,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.turn_in_place(180,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(5,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(5,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    notDone = True
    diff_drive.set_speed(7,7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        #print(adc.read_all())
        follow_line(subject,diff_drive)
        if subject[0]==1:
            if subject[3]==1:
                return None
            else:
                diff_drive.move_distance_mm(5,5,5)
                if subject[0]==1 and subject[3]==1:
                    return None
                else:
                    #diff_drive.move_dist
                    #ance_mm(5,-5,-5)
                    diff_drive.move_distance_mm(5,5,5)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.1)

def function4():
    global bolt_count
    diff_drive.move_distance_mm(80,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.turn_in_place(90,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(5,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    notDone = True
    diff_drive.set_speed(7,7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        #print(adc.read_all())
        follow_line(subject,diff_drive)
        if subject[0]==1:
            if subject[3]==1:
                return None
            else:
                diff_drive.move_distance_mm(5,5,5)
                if subject[0]==1 and subject[3]==1:
                    return None
                else:
                    diff_drive.move_distance_mm(5,5,5)
                print("Magnet time bby :D")
                magnet.pickup()
                bolt_count += 1
                diff_drive.turn_in_place(15,5)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)

#Function 5 is a early version, to test some things for the course. It is not used in the final product
def function5(): 
    global bolt_count
    diff_drive.turn_in_place(-45,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(5,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    n = 0
    notDone = True
    diff_drive.set_speed(7,7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        #print(adc.read_all())
        if subject == [1,1,0,0]:
            diff_drive.set_speed(7, 7)
            #print("forward")
        elif subject == [1,0,0,0]:
            diff_drive.set_speed(0, 7)
            #print("left")
        elif subject == [1,1,1,0]:
            diff_drive.set_speed(7, 0)        
        if subject[0]==1:
            print("Magnet time bby :D")
            bolt_count += 1
            n += 1
            if n == 2:
                return None
            
def function5v2():
    global bolt_count
    global circle
    diff_drive.turn_in_place(-45,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(100,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    notDone = True
    diff_drive.set_speed(7,7)
    time.sleep(0.5)
    while notDone:
        subject = adc.see_line()
        #print(subject)
        if circle != 2:
            if subject[0] == 1:
                magnet.pickup()
                circle += 1
                bolt_count += 1
                diff_drive.turn_in_place(15,5)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)
                    
            else:
                if subject == [0,1,1,1]:
                    diff_drive.set_speed(7, 7)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.1)
                if subject == [0,1,1,0]:
                    diff_drive.set_speed(0, 7)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.1)
                if subject == [0,0,1,1]:
                    diff_drive.set_speed(7, 0)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.1)
        else:
            return None

                    
            
        
def function6v2():
    notDone = True
    diff_drive.set_speed(7,7)
    time.sleep(0.5)
    while notDone:
        subject = adc.see_line()
        if subject == [1,1,1,1]:
            diff_drive.move_distance_mm(80,5,5)
            while diff_drive.status == diff_drive.STATUS_JOB:
                time.sleep(0.1)
            diff_drive.turn_in_place(-90,5)
            while diff_drive.status == diff_drive.STATUS_JOB:
                time.sleep(0.1)
            return None
        else:
            if subject == [0,1,1,1]:
                diff_drive.set_speed(7, 7)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)
            if subject == [0,1,1,0]:
                diff_drive.set_speed(0, 7)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)
            if subject == [0,0,1,1]:
                diff_drive.set_speed(7, 0)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)
        
    

def function7v2():
    diff_drive.destroy()
    global bolt_count
    notDone = True
    diff_drive.set_speed(7,7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        #print(adc.read_all())
        follow_line(subject,diff_drive)
        
        if subject[0]==1:
            print("mark seen")
            if subject[3]==1:
                pass
            else:
                diff_drive.move_distance_mm(5,5,5)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)
                else:
                    diff_drive.move_distance_mm(5,5,5)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.5)
                    print("Magnet time bby :D")
                    magnet.pickup()
                    diff_drive.turn_in_place(15,5)
                    while diff_drive.status == diff_drive.STATUS_JOB:
                        time.sleep(0.1)
                    bolt_count += 1
    
            
            
    
# The next functions, are not used in the final competetion, because we did not have enough time to test them out.
    
    
            
def function6():
    global bolt_count, fail6
    diff_drive.turn_in_place(100,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(50,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    notDone = True
    diff_drive.set_speed(-7,-7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        print(adc.read_all())
        if subject[0] == 1:
            print("Magnet time bby :D")
            bolt_count += 1
            return None
        elif subject[1] == subject[2] == 1:
            fail6 = True
            diff_drive.move_distance_mm(50,5)
            while diff_drive.status == diff_drive.STATUS_JOB:
                time.sleep(0.1)
            diff_drive.turn_in_place(-90,5)
            while diff_drive.status == diff_drive.STATUS_JOB:
                time.sleep(0.1)
            getBack = True
            while getBack:
                time.sleep(0.1)
                subject = adc.see_line()
                #print(subject)
                print(adc.read_all())
                if subject == [0,0,1,1]:
                    diff_drive.set_speed(-7, -7)
                    #print("forward")
                elif subject == [0,0,0,1]:
                    diff_drive.set_speed(-7, 0)
                    #print("left")
                elif subject == [0,1,1,1]:
                    diff_drive.set_speed(0, -7)        
                if subject[3]==1:
                    diff_drive.move_distance_mm(80,5)
                    diff_drive.turn_in_place(90,5)
                    diff_drive.move_distance_mm(80,5)
                    return None
    
def function7():
    diff_drive.turn_in_place(-45,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(100,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)

def function8():
    function1()
    
def function9():
    global bolt_count
    jesus = True
    diff_drive.move_distance_mm(80,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
        
    diff_drive.turn_in_place(90,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
        
    diff_drive.move_distance_mm(200,5,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    notDone = True
    diff_drive.set_speed(-7,-7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        print(adc.read_all())
        follow_line(subject,diff_drive)
        if subject[3] == 1 and jesus:
            diff_drive.turn_in_place(135,5)
            while diff_drive.status == diff_drive.STATUS_JOB:
                time.sleep(0.1)
            diff_drive.set_speed(-7,-7)
            jesus = False
        if subject[0]==1:
            if subject[3]==1:
                return None
            else:
                diff_drive.move_distance_mm(5,5,5)
                while diff_drive.status == diff_drive.STATUS_JOB:
                    time.sleep(0.1)
                if subject[0]==1 and subject[3]==1:
                    return None
        
def function10():
    global bolt_count
    notDone = True
    diff_drive.turn_in_place(180,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.set_speed(-7,-7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        print(adc.read_all())
        if subject == [0,1,1,0]:
            diff_drive.set_speed(-7, -7)
            #print("forward")
        elif subject == [0,1,0,0]:
            diff_drive.set_speed(2, -5)
            #print("left")
        elif subject == [0,0,1,0]:
            diff_drive.set_speed(-5, 2)    

        
        if subject[0]==1:
            if subject[3]==1:
                return None
            else:
                diff_drive.move_distance_mm(5,-5,-5)
                if subject[0]==1 and subject[3]==1:
                    return None
                else:
                    diff_drive.move_distance_mm(5,5,5)
            print("Magnet time bby :D")
            bolt_count += 1
            
def function11():
    notDone = True
    diff_drive.turn_in_place(180,5)
    diff_drive.set_speed(-7,-7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        print(adc.read_all())
        if subject == [0,1,1,0]:
            diff_drive.set_speed(-7, -7)
            #print("forward")
        elif subject == [0,1,0,0]:
            diff_drive.set_speed(2, -5)
            #print("left")
        elif subject == [0,0,1,0]:
            diff_drive.set_speed(-5, 2)    

        
        if subject[0]==1:
            if subject[3]==1:
                return None
            else:
                diff_drive.move_distance_mm(5,-5,-5)
                if subject[0]==1 and subject[3]==1:
                    return None
                else:
                    diff_drive.move_distance_mm(5,5,5)
            
def function12():
    global bolt_count
    diff_drive.move_distance_mm(80,-5,-5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.turn_in_place(90,5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    diff_drive.move_distance_mm(200,-5,-5)
    while diff_drive.status == diff_drive.STATUS_JOB:
        time.sleep(0.1)
    notDone = True
    diff_drive.set_speed(-7,-7)
    while notDone:
        time.sleep(0.1)
        subject = adc.see_line()
        #print(subject)
        print(adc.read_all())
        follow_line(subject,diff_drive)
        if subject[0]==1:
            print("Magnet time bby :D")
            bolt_count += 1
        if subject[1]==subject[2]==0:
            diff_drive.move_distance_mm(100,5)
            while diff_drive.status == diff_drive.STATUS_JOB:
                time.sleep(0.1)
            return None

    
    
function1()
function2()
function3()
function4()
function52()
function62()
function72()

# We did not have enough time, to test and integrate the last functions for the course.
"""if not fail6:
    function7()
function8()
function9()
function10()
function11()
function12()
diff_drive.destroy()"""


