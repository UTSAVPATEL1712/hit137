import time
from functools import wraps

def execution_timer(func):
    """
    Decorator that measures and prints the execution time of a method.
    This decorator is applied to methods that perform time-intensive operations like model inference.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def log_method_calls(func):
    """
    Decorator that logs when a method is called.
    This decorator is used to track method invocations for debugging and monitoring purposes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Method {func.__name__} was called")
        return func(*args, **kwargs)
    return wrapper

def validate_input_type(expected_type):
    """
    Decorator that validates the type of the first argument passed to a function.
    This decorator ensures that the input provided to model processing functions is of the expected type.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, input_data, *args, **kwargs):
            if not isinstance(input_data, expected_type):
                raise TypeError(f"Expected {expected_type.__name__}, got {type(input_data).__name__}")
            return func(self, input_data, *args, **kwargs)
        return wrapper
    return decorator