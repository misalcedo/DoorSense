class DoorSensor:
    def __init__(self, sensor_strategy):
        self.sensor_strategy = sensor_strategy

    def is_open(self):
        return self.sensor_strategy.is_open()
