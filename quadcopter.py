import time


class Quadcopter:
    def __init__(self):
        self.esc_pins = range(23, 27)
        self.pis = [pigpio.pi() for i in range(4)]
        [pi.set_mode(esc_pin, pigpio.OUTPUT) for pi, esc_pin in zip(self.pis, self.esc_pins)]
        [pi.set_PWM_frequency(esc_pin, 50) for pi, esc_pin in zip(self.pis, self.esc_pins)]  # 20ms

        self.min_pulse_width = 1000
        self.max_pulse_width = 2000

        self.throttle = 0  # percentage 0-100
        self.fans = [1, 1, 1, 1]  # ratio of throttle, total must be 4
        self.safety_throttle_factor_limit = 1.2  # a single fan must not exceed this limit

    def calibrate_esc(self):
        print('Calibrating ESCs ...')
        [pi.set_servo_pulsewidth(esc_pin, self.max_pulse_width) for pi, esc_pin in zip(self.pis, self.esc_pins)]  # Maximum throttle.
        time.sleep(2)
        [pi.set_servo_pulsewidth(esc_pin, self.min_pulse_width) for pi, esc_pin in zip(self.pis, self.esc_pins)]  # Minimum throttle.
        time.sleep(2)

    def _fan_percentage_to_dutycycle(self, percentage):
        return self.min_pulse_width + self.throttle/100 * (self.max_pulse_width - self.min_pulse_width) * percentage

    def _set_dutycycles(self):
        dutycycles = []


