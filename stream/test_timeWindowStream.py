from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch

from stream.TimeWindowStream import TimeWindowStream


class TestTimeWindowStream(TestCase):
    def setUp(self):
        self.start = datetime(year=2016, day=29, month=9, hour=2, minute=24, second=34)
        self.stream = TimeWindowStream(30)

    @patch('stream.TimeWindowStream.datetime')
    def test_add(self, mocked_datetime):
        mocked_datetime.now.return_value = self.start
        self.stream.add(1)
        mocked_datetime.now.return_value = self.start + timedelta(seconds=30)

        self.assertEqual(0, len(self.stream))
