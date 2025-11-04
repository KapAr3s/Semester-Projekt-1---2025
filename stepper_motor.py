from machine import Pin, PWM
import time

class StepperMotor:
    def __init__(self, pins, pwm_pct = 0.15, frequency=18_000):
        """
        Initialize a StepperMotor object.

        :param pins: List of GPIO pin numbers connected to the motor driver.
        :param pwm_pct: Percentage of the maximum PWM duty cycle.
        :param frequency: Frequency for the PWM signals.
        """

        self.pins = [PWM(Pin(pin)) for pin in pins]
        
        pwm_max = 65535
        self.pwm_val = int(pwm_max * pwm_pct)

        for pin in self.pins:
            pin.freq(frequency)
            
        self.direction = 0
        
        self.odometer = 0
        
        self.sequence = self.create_micro_sequence(8)
            
    def move_stepper(self, steps, delay_us=1000):
        """
        Move the stepper motor a specified number of steps.
        :param steps: Number of steps to move. Positive for forward, negative for backward.
        :param delay: Delay between steps in seconds.
        """
        
        delay_us = self.check_for_delay_limit(delay_us)
        
        sequence = self.make_sequence(steps)
        
        for _ in range(0, steps, self.direction):
            self.run_sequence(sequence, delay_us)
    
    def check_for_delay_limit(self, delay_us):
        '''
        Checks if delay is sat to low if then return the minimum delay
        else return desired delay.
        :param delay (float): Delay
        '''
        if delay_us < 100:
            delay_us = 100
            print("! Delay limit !")
        return delay_us
        
    def make_sequence(self, steps):
        '''
        Find the direction the motor is going by checking if a number is postive or negative.
        :param number (int): postive for forward and negative for backward.
        '''
        try:
            direction = int(steps/abs(steps))
            # Reverse the sequence if negative
            if direction == -1:
                sequence = self.sequence[::-1]
            else:
                sequence = self.sequence
            self.direction = direction
            # In case of zero
        except ZeroDivisionError:
            print("Error, direction is sad to forward")
            sequence = self.sequence

        full_sequence = sequence * steps
        full_sequence.append([0,0,0,0])
        print(full_sequence)
        return sequence
    
    def run_sequence(self, sequence, delay):
        '''
        Loops trough the sequence.
        :param delay (float): delay between each element in sequence
        '''
        for step in range(len(sequence)):
            self.set_step(sequence[step])
            # Remeber to update the odometer
            self.odometer += 1*self.direction
            time.sleep_us(delay)
                                       
    def set_step(self, step):
        '''
        Sets the PWM value for each pin.
        :param step (array): a step in sequence
        '''
        for pin in range(len(self.pins)):
            self.pins[pin].duty_u16(step[pin])
            
    def stop(self):
        '''
        Sets all pins to zero to stop the motor
        '''
        stop_sequence = [0, 0, 0, 0]
        self.set_step(stop_sequence)
        print("Stop --> {}\n".format(stop_sequence))
        print("Odometer: {}\n".format(self.odometer))
        
    def create_micro_sequence(self, size):
        '''
        Create new micro steps.
        :param size (int): the size of the microstep e.g. 3 then the micro steps is going pwm_val*1//3, pwm_val*2//3 and pwm_val,
        before is going down.
        '''
        one_step = []
        four_phases = []
        
        # One coil completely on, the next coil varming up 
        for i in range(size+1):
            one_step.append([self.pwm_val, self.pwm_val*i//size])
        # The one that was on is now slowly cooling of 
        for u in reversed(range(1, size)):
            one_step.append([self.pwm_val*u//size, self.pwm_val])
        
        # We now shift the one_step array in our sequence four times.  
        for u in range(4):
            # The lenght of sequence depends on the one_step size
            for i in range(len(one_step)):
                elements = [0,0,0,0]
                a = one_step[i][0]
                b = one_step[i][1]
                elements[u] = a
                # When index is longer than list is it because the value needs to be in the start.  
                if u+1 >= len(elements):
                    elements[0] = b
                else:
                    elements[u+1] = b
                four_phases.append(elements)        
        
        return four_phases
            
    # The micro step function is not perfect. It only affecting one of the adjacent coils to the coil completely on.
    # e.g. [pwm_val, pwm_val*2//3, 0, 0] istead of [pwm_val, pwm_val*2//3, pwm_val*1//3, 0]
    # The micro step function is not creating a wave effect, more a slow warm up or cooldown of the adjacent coil.