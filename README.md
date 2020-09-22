# Utility Package

This is a simple utility package.
It comes with:

- functions making listing folders and files easier [here](code_utils/os_utils.py)
- function to easily create a logger [here](code_utils/logger.py)
- decorators for functions and classes [here](code_utils/decorators)

---

## OS utils

Get the paths of files and/or folders inside a given directory.

The `strings_to_contain` parameter allows to pass a string or a list of strings which these files and/or folders need to contain. It defaults to `['']`, which is in every string.

The `mode` can either be `any` or `all`. It defines if one or all of the elements of `strings_to_contain` need to be present in the file/folder names. It defaults to `any`.

## Logger

Create and return a logger with a filepath, a name and additional keyword arguments.

The format defaults to `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`. It can be overridden by passing it using the `format` keyword.

---

## Decorators

### Base decorators

At the moment three [base decorators](code_utils/decorators/base.py) are implemented:

- A function based decorator `base_decorator_func`, which does wrap a function.
- A function based decorator `base_decorator_func_with_args`, which allows to pass arguments to the decorator. It also works with void parentheses:

    ```python

    @base_decorator_func_with_args
    def do_nothing_void(*args, **kwargs):
        pass

    @base_decorator_func_with_args()
    def do_nothing_void(*args, **kwargs):
        pass

    @base_decorator_func_with_args(1)
    def do_nothing_arg(*args, **kwargs):
        pass

    @base_decorator_func_with_args(one=1)
    def do_nothing_kwarg(*args, **kwargs):
        pass
    ```

- A class based decorator `BaseDecorator`, from which can be inherited. It allows, just like `base_decorator_func_with_args` above, to pass arguments to te decorator, to leave the parentheses void or not use them at all. Its advantage is, that in the child class only the `run` method has to be overridden.

### Concurrency

At the moment four [decorators](code_utils/decorators/concurrency.py) are implemented. All are function based.

- `run_in_thread`: Run function in separate thread
- `threaded`: Run function in a thread pool, one thread for each item in the passed iterables
- `run_in_process`: Run function in separate process
- `parallel`: Run function in a process pool, one process for each item in the passed iterables

Additionally the `synchronized` decorator from the package [wrapt](https://github.com/GrahamDumpleton/wrapt) can be used. It allows to run a function in a threading scheme using a lock.

### Exceptions

At the moment one [decorators](code_utils/decorators/exceptions.py) is implemented. It is function based.

- `ignore_exception`: Call the function, if it throws an error simply pass

### Logging

At the moment one [decorators](code_utils/decorators/log.py) is implemented. It is function based.

- `log`: Call the function, log the function's name, the arguments and the result

### Printing

At the moment one [decorators](code_utils/decorators/printing.py) is implemented. It is function based.

- `print_me`: Call the function, print the function's name, the arguments and the result to the console

### Timing

At the moment two [decorators](code_utils/decorators/timing.py) are implemented. All are function based.

- `timer`: Call the function and print its duration to the console
- `time_all_class_methods`: Decorate all methods of a class with timing.

### Warnings

At the moment one [decorators](code_utils/decorators/warnings.py) is implemented. It is function based.

- `deprecated`: Call the function and warn the user if the function is deprecated
