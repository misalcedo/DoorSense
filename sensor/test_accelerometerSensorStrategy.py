from unittest import TestCase
from unittest.mock import Mock

from sensor.AccelerometerSensorStrategy import AccelerometerSensorStrategy


class TestAccelerometerSensorStrategy(TestCase):
    def setUp(self):
        self.mocked_sense_hat = Mock()
        self.closed_acceleration = {'x': -5, 'y': -2, 'z': 1}
        self.sensor_strategy = AccelerometerSensorStrategy(self.mocked_sense_hat, self.closed_acceleration, 0.1)

    def test_is_closed(self):
        self.mocked_sense_hat.accelerometer_raw = self._increment_axis(0.1, 'x')
        self.assertFalse(self.sensor_strategy.is_open())

    def test_is_open_x(self):
        self.mocked_sense_hat.accelerometer_raw = self._increment_axis(0.10001, 'x')
        self.assertTrue(self.sensor_strategy.is_open())

    def test_is_open_y(self):
        self.mocked_sense_hat.accelerometer_raw = self._increment_axis(-0.11, 'y')
        self.assertTrue(self.sensor_strategy.is_open())

    def test_is_open_z(self):
        self.mocked_sense_hat.accelerometer_raw = self._increment_axis(-10, 'z')
        self.assertTrue(self.sensor_strategy.is_open())

    def _increment_axis(self, increment, axis):
        acceleration = self.closed_acceleration.copy()
        acceleration[axis] = self.closed_acceleration[axis] + increment

        return acceleration
