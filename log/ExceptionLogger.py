import logging


class ExceptionLogger:
    def __init__(self, function):
        self.function = function

    def __call__(self, *arguments, **keyword_arguments):
        try:
            self.function(*arguments, **keyword_arguments)
        except (RuntimeError, OSError) as exception:
            logging.exception('An error occurred while calling %s with arguments %s and keyword arguments %s: %s',
                              self.function.__name__,
                              arguments,
                              keyword_arguments,
                              exception)
