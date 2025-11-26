from machine import Pin, PWM
import time

PWM_MAX = 65535

class StepperMotor:

  def __init__(self, pins, pwm_pct = 0.15, frequency=18_000,):
    self.direction = 0
    self.sequence = [[0,0,0,0]]
    self.odometer = 0
    self.speed = 0
    self.step_index = 0
    self.pwm_val = int(PWM_MAX * pwm_pct)
    self.pins = [PWM(Pin(pin)) for pin in pins]
    for pin in self.pins:
      pin.freq(frequency)

  def print(self):
     print([self.odometer, self.speed, self.sequence[self.step_index], self.step_index, self.direction])

  def step(self):
    self.step_index = (self.step_index + self.direction) % len(self.sequence)
    step = self.sequence[self.step_index]
    for pin in range(len(self.pins)):
      self.pins[pin].duty_u16(step[pin])

    if self.speed != 0 and self.step_index % (self.speed*2) == 0:
       self.odometer += 1

  def set_speed(self, speed):
    if abs(speed) > 10:
      self.speed = 1
    else:
      self.speed = 11-abs(speed)
    if speed < 0:
      direction = -1
    elif speed == 0:
      direction = 0
      self.speed = 0
    else:
      direction = 1

    orginal_seq_len = len(self.sequence)
    self.sequence = self.create_sequence(self.speed)
    self.step_index = int((self.step_index*len(self.sequence))/orginal_seq_len)
    self.direction = direction

  def create_sequence(self, size):
    '''
    Create new micro steps.
    :param size (int): the size of the microstep e.g. 3 then the micro steps is going pwm_val*1//3, pwm_val*2//3 and pwm_val,
    before is going down.
    '''
    if size == 0:
      return [[0,0,0,0]]
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