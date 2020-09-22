

__all__ = [
    'ignore_exception',
]
def ignore_exception(function):
    """
    Decorator for supressing all exceptions
    """
    def wrapper(*func_args, **func_kwargs):
        try:
            return function(*func_args, **func_kwargs)
        except:
            pass
    return wrapper