import pigpio

from quadcopter import Quadcopter


class Transmitter:
    def __init__(self, drone: Quadcopter):
        # Throttle pin
        self._throttle_pin = 22

        # Transmitter signal
        self._min_ms = 1.2  # 1.07
        self._max_ms = 2  # 1.72

        self._tick = 0

        self._pi = pigpio.pi()
        self._pi.set_mode(self._throttle_pin, pigpio.INPUT)

        self._cb1 = None
        self._cb2 = None

        self._drone = drone

    def start(self):
        self._cb1 = self._pi.callback(self._throttle_pin, pigpio.RISING_EDGE, self._set_rising_time_callback())
        self._cb2 = self._pi.callback(self._throttle_pin, pigpio.FALLING_EDGE, self._set_output_callback())

    def close(self):
        if self._cb1 is not None:
            self._cb1.cancel()
            self._cb2.cancel()
        self._pi.stop()

    def _ms_to_ratio(self, ms):
        return (ms - self._min_ms) / (self._max_ms - self._min_ms)

    def _set_rising_time_callback(self):
        def _set_rising_time(gpio_pin, level, tick):
            self._tick = tick
        return _set_rising_time

    def _set_output_callback(self):
        def _set_output(gpio_pin, level, tick):  # tick in micro-s
            if self._tick == 0:
                print('Missed rising edge')
            else:
                # pass
                # print((tick-_tick)/1000)
                # print(self._tick)
                self._drone.throttle = self._ms_to_ratio((tick-self._tick)/1000)
                self._tick = 0
        return _set_output
