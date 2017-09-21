import logging
from types import MethodType


class SensorStrategyLogger:
    def __init__(self, function):
        self.function = function

    def __call__(self, sensor_strategy, current_accelerometer):
        is_open = self.function(sensor_strategy, current_accelerometer)

        logging.info('[SENSOR] %s', {
            'current_accelerometer': current_accelerometer,
            'closed_accelerometer': sensor_strategy.closed_acceleration,
            'allowed_delta': sensor_strategy.allowed_delta,
            'is_open': is_open
        })

        return is_open

    def __get__(self, sensor_strategy, _):
        return MethodType(self, sensor_strategy)
