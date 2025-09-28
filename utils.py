"""
Shared utilities: decorators, error messaging, and small helpers.
"""
import functools
import time

class AppError(Exception):
    pass

def human_error(e: Exception) -> str:
    return f"{e.__class__.__name__}: {e}"

def timing(label: str):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = (time.time() - start) * 1000.0
                print(f"[TIMING] {label} took {elapsed:.1f} ms")
        return _wrapper
    return _decorator

def logged(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        print(f"[LOG] Enter: {func.__qualname__}")
        try:
            return func(*args, **kwargs)
        finally:
            print(f"[LOG] Exit:  {func.__qualname__}")
    return _wrapper

def validate_nonempty(param_name: str):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            value = kwargs.get(param_name, None)
            if value is None and len(args) >= 2:
                value = args[1]
            if value is None or (isinstance(value, str) and not value.strip()):
                raise AppError(f"'{param_name}' cannot be empty.")
            return func(*args, **kwargs)
        return _wrapper
    return _decorator

class LoggingMixin:
    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")

class TimingMixin:
    def _time_block(self, label: str):
        return time.perf_counter(), label
    def _time_end(self, start_ts: float, label: str):
        elapsed = (time.perf_counter() - start_ts) * 1000.0
        self.log(f"{label} took {elapsed:.2f} ms")

def explain_oop_choices() -> str:
    return (
        "Here’s how we used OOP in our project:\n"
        "- Encapsulation: We keep the model objects hidden inside the class so you can only access them through properties.\n"
        "- Polymorphism: Both models have the same .run(input_data) method, so the GUI doesn’t care which one it’s using.\n"
        "- Method overriding: The subclasses change how run() and model_info() work compared to the base class.\n"
        "- Multiple inheritance: We used LoggingMixin and TimingMixin together to show that a class can get features from more than one parent.\n"
        "- Multiple decorators: We stacked @logged, @timing, and @validate_nonempty on top of functions to add extra checks and info.\n"
    )
