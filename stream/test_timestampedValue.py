from datetime import datetime
from unittest import TestCase

from stream.TimestampedValue import TimestampedValue


class TestTimestampedValue(TestCase):
    def test___init__(self):
        now = datetime.now()
        timestamped_value = TimestampedValue(now, 1)

        self.assertEqual(now, timestamped_value.timestamp)
        self.assertEqual(1, timestamped_value.value)
