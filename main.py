import logging
import sys
from argparse import ArgumentParser
from datetime import datetime

from sense_hat import SenseHat

from log.ExceptionLogger import ExceptionLogger
from notification.EmailNotificationStrategy import EmailNotificationStrategy
from notification.Notifier import Notifier
from rate.RateLimiter import RateLimiter
from sensor.AccelerometerSensorStrategy import AccelerometerSensorStrategy
from sensor.DoorSensor import DoorSensor


def parse_arguments(arguments):
    parser = ArgumentParser(description='Notify recipients when a door is opened.')

    parser.add_argument('-a', '--allowed_acceleration_delta', type=float, default=0.03,
                        help='Acceleration in Gs the sensor must accelerate before the door is considered open.')

    parser.add_argument('-d', '--dedupe_window', type=int, default=30,
                        help='Time window where new notifications will be dropped to avoid spamming recipients.')

    parser.add_argument('-f', '--sensor_frequency', type=int, default=5,
                        help='How many times per second to check the sensors.')

    parser.add_argument('-m', '--message', default='Door was opened on {timestamp}!',
                        help='Message text to send when the door is opened.'
                             'Supports dynamic substitution of supported attributes by including '
                             'the attribute name enclosed in "{}" (eg. "Some message {timestamp}"). '
                             'Supported attributes : timestamp.')

    parser.add_argument('-r', '--recipients', nargs='+', default=[],
                        help='Email addresses to send a notification to when door is opened.')

    parser.add_argument('-s', '--subject', default='Door Status Update',
                        help='Subject text for the message sent if the door is opened.')

    parser.add_argument('-t', '--timestamp_format', default='%A, %B %d, %Y at %I:%M:%S %p',
                        help='Format for timestamp provided as a dynamic message attribute. '
                             'See https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior '
                             'for more details.')

    parser.add_argument('-v', '--version', action='version', version='DoorSense 1.0')

    return parser.parse_args(arguments)


def main(arguments):
    logging.basicConfig(filename='door_sense.log', format='%(asctime)-15s [%(levelname)s] %(message)s', level=logging.DEBUG)

    sense_hat = SenseHat()
    sensor_strategy = AccelerometerSensorStrategy(sense_hat,
                                                  sense_hat.accelerometer_raw,
                                                  arguments.allowed_acceleration_delta)
    door_sensor = DoorSensor(sensor_strategy)

    notification_strategy = EmailNotificationStrategy()
    notifier = Notifier(notification_strategy, arguments.dedupe_window)

    rate_limiter = RateLimiter(arguments.sensor_frequency)

    while True:
        check_door_state(arguments, door_sensor, notifier, rate_limiter)


@ExceptionLogger
def check_door_state(arguments, door_sensor, notifier, rate_limiter):
    rate_limiter.acquire()
    if door_sensor.is_open():
        notifier.notify(arguments.subject,
                        build_message(arguments.message, arguments.timestamp_format),
                        arguments.recipients)


def build_message(message, timestamp_format):
    time_now = datetime.now().strftime(timestamp_format)
    return message.format(**{'timestamp': time_now})


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
