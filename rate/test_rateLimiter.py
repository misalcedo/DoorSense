from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from rate.RateLimiter import RateLimiter


class TestRateLimiter(TestCase):
    def setUp(self):
        self.start = datetime(year=2016, day=29, month=9, hour=2, minute=24, second=34)

    @patch('rate.RateLimiter.sleep')
    @patch('rate.RateLimiter.datetime')
    def test_acquire(self, mocked_datetime, mocked_sleep):
        mocked_datetime.now.return_value = self.start

        rate_limiter = RateLimiter(1, 0.1, 0.1)

        rate_limiter.acquire(0.1)
        rate_limiter.acquire(0.4)

        self.assertAlmostEqual(4.0, mocked_sleep.call_args[0][0], delta=0.01)

    def test___init__(self):
        rate_limiter = RateLimiter(1)
        self.assertEqual(1, rate_limiter.max_tokens)
        self.assertEqual(1, rate_limiter.tokens_per_second)
        self.assertEqual(1, rate_limiter.remaining_tokens)
