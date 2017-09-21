from datetime import datetime
from time import sleep

_SLEEP_BUFFER_SECONDS = 0.001  # necessary wait buffer due to sleep inaccuracy
_MICROSECONDS_PER_SECOND = float(10 ** 6)


class RateLimiter:
    def __init__(self, max_tokens=1, tokens_per_second=None, initial_tokens=None):
        assert 0 < max_tokens
        self.max_tokens = max_tokens

        self._initialize_tokens_per_second(tokens_per_second)
        assert 0 < self.tokens_per_second

        self._initialize_remaining_tokens(initial_tokens)
        assert 0 <= self.remaining_tokens <= self.max_tokens

        self.refreshed_at = datetime.now()

    def _initialize_remaining_tokens(self, initial_tokens):
        if initial_tokens is None:
            self.remaining_tokens = self.max_tokens
        else:
            self.remaining_tokens = initial_tokens

    def _initialize_tokens_per_second(self, tokens_per_second):
        if tokens_per_second is None:
            self.tokens_per_second = self.max_tokens
        else:
            self.tokens_per_second = tokens_per_second

    def acquire(self, tokens=1):
        assert 0 <= tokens <= self.max_tokens

        self._block_until_ready(tokens)
        self._refresh()

        self.remaining_tokens -= tokens

    def _block_until_ready(self, tokens):
        if self.has_tokens(tokens):
            return

        seconds_to_sleep = self._seconds_to_acquire(tokens)
        if seconds_to_sleep > 0:
            sleep(seconds_to_sleep + _SLEEP_BUFFER_SECONDS)

    def _seconds_to_acquire(self, tokens):
        return max(0, tokens - self.remaining_tokens) / self.tokens_per_second

    def _refresh(self):
        seconds_to_refresh = self._seconds(datetime.now() - self.refreshed_at)
        tokens_to_add = seconds_to_refresh * self.tokens_per_second

        self.remaining_tokens = min(self.remaining_tokens + tokens_to_add, self.max_tokens)
        self.refreshed_at = datetime.now()

    def has_tokens(self, tokens):
        self._refresh()
        return self.remaining_tokens >= tokens

    @staticmethod
    def _seconds(delta):
        return delta.seconds + (delta.microseconds / _MICROSECONDS_PER_SECOND)
