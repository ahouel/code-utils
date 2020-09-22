"""Python Decorator Templated"""
from functools import wraps, partial

__all__ = [
    'base_decorator_func',
    'base_decorator_func_with_args',
    'BaseDecorator',
]

def base_decorator_func(func):
    """Decorator function:
    This decorator overrides original 'function' and
    returns the wrapper function.

    Parameters
    ----------
    function : function
        Function which execution shall be wrapper.

    Returns
    -------
    function
        The wrapper function
    """
    @wraps(function)  # maintain all the info about the function
    def wrapper(*args, **kwargs):
        """Wrapper function:
        This wrapper executes the wrapper function along with whatever functionality
        you like.
        """
        print('{} is called from the decorator' \
            'with arguments={} and kwargs={}'.format(
                func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        print('{} returns {}'.format(func.__name__, result))
        return result
    return wrapper


def base_decorator_func_with_args(func=None, *dec_args, **dec_kwargs):
    """Decorator function with optional arguments:
    This decorator receives arguments and
    returns the wrapper function.
    If the decorator is set with arguments when decorating a function,
    the decorator is returned as a partial function along with the kwargs.

    Parameters
    ----------
    function : function, optional
        The function which shall be wrapper, by default None

    dec_kwargs: arguments, optional
        additional decorator arguments which can be used
        inside the wrapper function

    Returns
    -------
    function
        The wrapper function
    """
    if func is None:
        """A partial is a "non-complete function call" that includes
        a function and some arguments, so that they are passed around
        as one object without actually calling the function yet.
        """
        return partial(base_decorator_func_with_args, args=dec_args, kwargs=dec_kwargs)

    @wraps(function)  # maintain all the info about the function
    def wrapper(*args, **kwargs):
        """Wrapper function:
        This wrapper executes the wrapper function along with whatever functionality
        you like. The dec_kwargs can be used here.
        """
        print('{} is called from the decorator with arguments={} and kwargs={}'.format(func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        print('{} returns {}'.format(func.__name__, result))
        return result
    return wrapper

# Sentinel to detect undefined function argument.
UNDEFINED_FUNCTION = object()

class BaseDecorator(object):
    """Base class to easily create convenient decorators.

    Override :py:meth:`setup`, :py:meth:`run` or :py:meth:`decorate` to create
    custom decorators:

    * :py:meth:`setup` is dedicated to setup, i.e. setting decorator's internal
      options.
      :py:meth:`__init__` calls :py:meth:`setup`.

    * :py:meth:`decorate` is dedicated to wrapping function, i.e. remember the
      function to decorate.
      :py:meth:`__init__` and :py:meth:`__call__` may call :py:meth:`decorate`,
      depending on the usage.

    * :py:meth:`run` is dedicated to execution, i.e. running the decorated
      function.
      :py:meth:`__call__` calls :py:meth:`run` if a function has already been
      decorated.

    Decorator instances are callables. The :py:meth:`__call__` method has a
    special implementation in Decorator. Generally, consider overriding
    :py:meth:`run` instead of :py:meth:`__call__`.

    This base class transparently proxies to decorated function:

    >>> @BaseDecorator
    ... def return_args(*args, **kwargs):
    ...    return (args, kwargs)
    >>> return_args()
    ((), {})
    >>> return_args(1, 2, three=3)
    ((1, 2), {'three': 3})

    This base class stores decorator's options in ``options`` dictionary
    (but it doesn't use it):

    >>> @BaseDecorator
    ... def do_nothing():
    ...    pass
    >>> do_nothing.kwargs
    {}
    >>> @BaseDecorator()
    ... def do_nothing():
    ...    pass
    >>> do_nothing.kwargs
    {}
    >>> @BaseDecorator(one=1)
    ... def do_nothing():
    ...    pass
    >>> do_nothing.kwargs
    {'one': 1}
    """
    def __init__(self, *args, **kwargs):
        """Constructor.

        Accepts positional and keyword argument:
        If the function is passed to the constructor it has to be the first argument.
        """
        self.decorated = None

        # Check if the first argument is callable = a function is passed
        # If yes -> set it as decorated function and remove it from the args
        if args:
            if callable(args[0]):
                self.decorate(args[0])
                args = args[1:]
        self.setup(*args, **kwargs)

    def decorate(self, func):
        """Remember the function to decorate.

        Raises TypeError if ``func`` is not callable.
        """
        if not callable(func):
            raise TypeError('Cannot decorate a non callable object "{}"'
                            .format(func))
        self.decorated = func

    def setup(self, *args, **kwargs):
        """Store decorator's args and kwargs"""
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """Run decorated function if available, else decorate first arg.

        This base implementation is a transparent proxy to the decorated
        function: it passes positional and keyword arguments as is, and returns
        result."""
        func = self.decorated
        if func is None:
            func = args[0]
            if args[1:] or kwargs:
                raise ValueError('Cannot decorate and setup simultaneously '
                                 'with __call__(). Use __init__() or '
                                 'setup() for setup. Use __call__() or '
                                 'decorate() to decorate.')
            self.decorate(func)
            return self
        else:
            return self.run(func, *args, **kwargs)

    def run(self, func, *args, **kwargs):
        """Actually run the decorator.

        This base implementation is a transparent proxy to the decorated
        function: it passes positional and keyword arguments as is, and returns
        result.
        """
        @wraps(func)  # maintain all the info about the function
        def wrapper(*args, **kwargs):
            """Run function:
            This wrapper executes the wrapper function along with whatever functionality
            you like. The args and kwargs can be used here.
            """
            print('{} is called from the decorator with arguments={} and kwargs={}'.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            print('{} returns {}'.format(func.__name__, result))
            return result

        return wrapper(*args, **kwargs)

    def __getattr__(self, name):
        return self.decorated.__getattribute__(name)

    def __str__(self):
        return self.decorated.__str__()



# class Decorated(object):
#     """A representation of a decorated class.
#     This user-immutable object provides information about the decorated
#     class, method, or function. The decorated callable can be called
#     by directly calling the ``Decorated`` instance, or via the
#     ``wrapped`` instance attribute.
#     The example below illustrates direct instantiation of the
#     ``Decorated`` class, but generally you will only deal with
#     instances of this class when they are passed to the functions
#     specified on generic decorators.
#     .. code:: python
#         from pydecor import Decorated
#         def some_function(*args, **kwargs):
#             return 'foo'
#         decorated = Decorated(some_function, ('a', 'b'), {'c': 'c'})
#         assert decorated.wrapped.__name__ == some_function.__name__
#         assert decorated.args == ('a', 'b')
#         assert decorated.kwargs == {'c': 'c'}
#         assert decorated.result is None  # has not yet been called
#         res = decorated(decorated.args, decorated.kwargs)
#         assert 'foo' == res == decorated.result
#     .. note::
#         identity tests ``decorated.wrapped is some_decorated_function``
#         will not work on the ``wrapped`` attribute of a ``Decorated``
#         instance, because internally the wrapped callable is wrapped
#         in a method that ensures that ``Decorated.result`` is set
#         whenever the callable is called. It is wrapped using
#         ``functools.wraps``, so attributes like ``__name__``,
#         ``__doc__``, ``__module__``, etc. should still be the
#         same as on an actual reference.
#         If you need to access a real reference to the wrapped
#         function for any reason, you can do so by accessing
#         the ``__wrapped__`` property, on ``wrapped``, which is
#         set by ``functools.wraps``, e.g.
#         ``decorated.wrapped.__wrapped__``.
#     :param wrapped: a reference to the wrapped callable. Calling the
#         wrapped callable via this reference will set the ``result``
#         attribute.
#     :param args: a tuple of arguments with which the decorated function
#         was called
#     :param kwargs: a dict of arguments with which the decorated function
#         was called
#     :param result: either ``None`` if the wrapped callable has not yet
#         been called or the result of that call
#     """

#     __slots__ = ("args", "kwargs", "wrapped", "result")

#     args: tuple
#     kwargs: dict
#     wrapped: t.Callable
#     result: t.Optional[t.Any]

#     def __init__(self, wrapped, args, kwargs, result=None):
#         """Instantiate a Decorated object
#         :param callable wrapped: the callable object being wrapped
#         :param tuple args: args with which the callable was called
#         :param dict kwargs: keyword arguments with which the callable
#             was called
#         :param
#         """
#         sup = super(Decorated, self)
#         sup.__setattr__("args", get_fn_args(wrapped, args))
#         sup.__setattr__("kwargs", kwargs)
#         sup.__setattr__("wrapped", self._sets_results(wrapped))
#         sup.__setattr__("result", result)

#     def __str__(self):
#         """Return a nice string of self"""
#         if hasattr(self.wrapped, "__name__"):
#             name = self.wrapped.__name__
#         else:
#             name = str(self.wrapped)
#         return "<Decorated {}({}, {})>".format(name, self.args, self.kwargs)

#     def __call__(self, *args, **kwargs):
#         """Call the function the specified arguments.
#         Also set ``self.result``
#         """
#         return self.wrapped(*args, **kwargs)

#     def __setattr__(self, key, value):
#         """Disallow attribute setting"""
#         raise AttributeError(
#             'Cannot set "{}" because {} is immutable'.format(key, self)
#         )

#     def _sets_results(self, wrapped):
#         """Ensure that calling ``wrapped()`` sets the result attr
#         :param callable wrapped: the wrapped function, class, or method
#         """

#         @wraps(wrapped)
#         def wrapped_wrapped(*args, **kwargs):
#             """Set self.result after calling wrapped"""
#             res = wrapped(*args, **kwargs)
#             super(Decorated, self).__setattr__("result", res)
#             return res

#         return wrapped_wrapped
