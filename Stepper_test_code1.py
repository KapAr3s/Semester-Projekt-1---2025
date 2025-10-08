from machine import Pin, PWM
import time

class StepperMotor:
    def __init__(self, pins, pwm_pct=0.15, frequency=18000):
        self.pins = [PWM(Pin(pin)) for pin in pins]
        self.pwm_pct = pwm_pct
        self.frequency = frequency
        self.pwm_max = 65535
        self.pwm_val = int(self.pwm_max * self.pwm_pct)
        for pin in self.pins:
            pin.freq(self.frequency)

    def step(self, seq):
        for i, val in enumerate(seq):
            self.pins[i].duty_u16(self.pwm_val if val else 0)

    def release(self):
        for pin in self.pins:
            pin.duty_u16(0)

def move_both_steppers(left_motor, right_motor, steps, delay=0.01, direction="forward"):
    step_sequence = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]
    if direction == "backward":
        step_sequence = step_sequence[::-1]

    for step in range(steps):
        seq = step_sequence[step % len(step_sequence)]
        left_motor.step(seq)
        right_motor.step(seq)
        time.sleep(delay)
    left_motor.release()
    right_motor.release()

# Example usage
if __name__ == '__main__':
    left_motor = StepperMotor([0, 1, 2, 3], 1, 18000)
    right_motor = StepperMotor([4, 5, 6, 7], 1, 18000)

    steps = 400
    delay = 0.01

    move_both_steppers(left_motor, right_motor, steps, delay, direction="forward")
