from log.SensorStrategyLogger import SensorStrategyLogger


class AccelerometerSensorStrategy:
    def __init__(self, sense_hat, closed_acceleration, allowed_delta):
        assert 0 < allowed_delta

        self.sense_hat = sense_hat
        self.closed_acceleration = closed_acceleration
        self.allowed_delta = allowed_delta

    def is_open(self):
        current_acceleration = self.sense_hat.accelerometer_raw
        return self._within_allowed_delta(current_acceleration)

    @SensorStrategyLogger
    def _within_allowed_delta(self, current_acceleration):
        x_too_large = self._axis_exceeded_allowed_delta(current_acceleration, 'x')
        y_too_large = self._axis_exceeded_allowed_delta(current_acceleration, 'y')
        z_too_large = self._axis_exceeded_allowed_delta(current_acceleration, 'z')

        return x_too_large or y_too_large or z_too_large

    def _axis_exceeded_allowed_delta(self, current_acceleration, axis):
        return self._axis_acceleration_delta(current_acceleration, axis) > self.allowed_delta

    def _axis_acceleration_delta(self, current_acceleration, axis):
        return abs(self.closed_acceleration[axis] - current_acceleration[axis])
