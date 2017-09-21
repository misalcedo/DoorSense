from datetime import datetime, timedelta

from stream.TimestampedValue import TimestampedValue


class TimeWindowStream:
    def __init__(self, window_size_in_seconds):
        assert 0 <= window_size_in_seconds

        self.window_size_in_seconds = timedelta(seconds=window_size_in_seconds)
        self.values = []

    def add(self, value):
        timestamped_value = TimestampedValue(timestamp=datetime.now(), value=value)
        self.values.append(timestamped_value)

    def __iter__(self):
        self._filter_values()
        return iter(self.values)

    def __len__(self):
        self._filter_values()
        return len(self.values)

    def _filter_values(self):
        self.values = list(self._filtered_values(datetime.now()))

    def _filtered_values(self, current_timestamp):
        return filter(
            lambda timestamped_value: current_timestamp < (timestamped_value.timestamp + self.window_size_in_seconds),
            self.values
        )
