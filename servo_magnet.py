from machine import Pin, PWM
from differential_drive import DifferentialDrive
import time


class ServoMagnet:
    def __init__(self, servo_pin="GP12", magnet_pin=8):
        # Servo setup
        self.servo = PWM(Pin(servo_pin))
        self.servo.freq(40)
        
        # Motor setup
        self.motor = DifferentialDrive()

        # Magnet setup
        self.magnet = PWM(Pin(magnet_pin))
        self.magnet.freq(8000)

        # Constants
        self.duty_max = 65535
        self.top = 1100 # Found via physical test
        self.bot = 6150 # Found via physical test
        self.step = 20

        # State
        self.servo_val = self.top
        self.counter = 0
    

    def magnet_on(self, strength=0.8):
        self.magnet.duty_u16(int(self.duty_max * strength))

    def magnet_off(self):
        self.magnet.duty_u16(0)

    def move_up(self):
        #self.magnet_on() # This is for testing the mechanism works
        #if self.servo_val >= self.top:
        self.servo_val -= self.step
        self.servo.duty_u16(self.servo_val)
        #print(self.servo_val)
        time.sleep(0.005)
        """else:
            self.counter = 1
            time.sleep(0.5)
            self.magnet_off()
            time.sleep(1)""" # This is for testing the mechanism works

    def move_down(self):
        #if self.servo_val <= self.bot:
        self.servo_val += self.step
        self.servo.duty_u16(self.servo_val)
        #print(self.servo_val)
        time.sleep(0.005)
        """else:
            self.counter = 0
            time.sleep(1)""" # This is for testing the mechanism works
            
    def pickup(self):
        self.wiggle = 0
        time.sleep(0.5)
        self.motor.move_distance_mm(300, 5, 5)
        while self.motor.status == self.motor.STATUS_JOB:
            time.sleep(0.01)
        self.motor.destroy
        time.sleep(0.5)
        while self.servo_val <= self.bot:
            self.move_down()
        self.magnet_on()
        time.sleep(0.5)
        self.motor.move_distance_mm(250, -5, -5)
        while self.motor.status == self.motor.STATUS_JOB:
            time.sleep(0.01)
        self.motor.destroy
        time.sleep(1)
        while self.servo_val >= self.top:
            self.move_up()
        time.sleep(0.5)
        self.magnet_off()
        time.sleep(0.2)
        while self.wiggle <= 2:
            self.wiggle += 1
            self.servo.duty_u16(1350) 
            time.sleep(0.05)
            self.servo.duty_u16(1100)
            time.sleep(0.1)
        time.sleep(0.5)
        
        
        
        

    def run(self):
        while True:
            if self.counter == 0:
                self.move_up()
            else:
                self.move_down()

