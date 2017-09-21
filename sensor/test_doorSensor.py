from unittest import TestCase
from unittest.mock import Mock

from sensor.DoorSensor import DoorSensor


class TestDoorSensor(TestCase):
    def setUp(self):
        self.mocked_sensor_strategy = Mock()
        self.door_sensor = DoorSensor(self.mocked_sensor_strategy)

    def test_is_open(self):
        self.mocked_sensor_strategy.is_open.return_value = True
        self.assertTrue(self.door_sensor.is_open())

    def test_times_opened(self):
        self.mocked_sensor_strategy.is_open.return_value = False
        self.assertFalse(self.door_sensor.is_open())
