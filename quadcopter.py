import time
import pigpio


class Quadcopter:
    def __init__(self):
        self._esc_pins = range(23, 27)
        self._pis = [pigpio.pi() for i in range(4)]
        [pi.set_mode(esc_pin, pigpio.OUTPUT) for pi, esc_pin in zip(self._pis, self._esc_pins)]
        [pi.set_PWM_frequency(esc_pin, 50) for pi, esc_pin in zip(self._pis, self._esc_pins)]  # 20ms

        self._min_pulse_width = 1000
        self._max_pulse_width = 2000

        self._throttle = 0  # ratio 0-1
        self._fans = [1, 1, 1, 1]  # ratios of throttle, total must be 4
        self._safety_throttle_factor_limit = 1.1  # a single fan must not exceed this limit

    def calibrate_esc(self):
        print('Calibrating ESCs ...')
        [pi.set_servo_pulsewidth(esc_pin, self._max_pulse_width) for pi, esc_pin in zip(self._pis, self._esc_pins)]  # Maximum throttle.
        time.sleep(2)
        [pi.set_servo_pulsewidth(esc_pin, self._min_pulse_width) for pi, esc_pin in zip(self._pis, self._esc_pins)]  # Minimum throttle.
        time.sleep(2)

    def turn_off_esc(self):
        [pi.set_servo_pulsewidth(esc_pin, 0) for pi, esc_pin in zip(self._pis, self._esc_pins)]
        [pi.stop() for pi in self._pis]

    def _fan_percentage_to_dutycycle(self, fan_percentage):
        # TODO: include safety factor?
        return self._min_pulse_width + self._throttle * (self._max_pulse_width - self._min_pulse_width) * fan_percentage

    def _set_dutycycles(self):
        dutycycles = []
        [pi.set_servo_pulsewidth(esc_pin, self._fan_percentage_to_dutycycle(1)) for pi, esc_pin in zip(self._pis, self._esc_pins)]

    @property
    def throttle(self):
        return self._throttle

    @throttle.setter
    def throttle(self, throttle):
        self._throttle = throttle
        self._set_dutycycles()

