from unittest import TestCase
from unittest.mock import patch

from log.SensorStrategyLogger import SensorStrategyLogger


class TestSensorStrategyLogger(TestCase):
    def setUp(self):
        self.closed_acceleration = 1
        self.allowed_delta = 2

    @patch('log.SensorStrategyLogger.logging')
    def test___call__(self, mocked_logging):
        self.fake_method(0)
        self.assertEqual(1, mocked_logging.info.call_count)

    @SensorStrategyLogger
    def fake_method(self, current_acceleration):
        return current_acceleration is not None
