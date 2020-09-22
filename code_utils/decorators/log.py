# timing.py
from functools import wraps, partial
import logging

__all__ = [
    'log',
]


def log(function=None, *, logger=logging.getLogger(__name__), level='info'):
    if function is None:
        """A partial is a "non-complete function call" that includes
        a function and some arguments, so that they are passed around
        as one object without actually calling the function yet.
        """
        return partial(log, logger=logger, level=level)
    @wraps(function)  # maintain all the info about the function
    def wrapper(*func_args, **func_kwargs):
        logger.log(level, '{} was called with arguments={} and kwargs={}'.format(function, func_args, func_kwargs))
        result = function(*func_args, **func_kwargs)
        logger.log(level, '{} return value {}'.format(function, result))
        return result
    return wrapper
