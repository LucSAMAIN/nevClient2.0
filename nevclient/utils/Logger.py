#! usr/env/bin python3
# nevclient.utils.Logger

import functools
import inspect

def log_debug_event(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0] # 'self'
        bound_args = inspect.signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()
        args_repr = [f"{name}={value!r}" for name, value in bound_args.arguments.items() if name != 'self']
        if hasattr(instance, 'logger'):
            instance.logger.debug(f"Calling {func.__name__} with args: {', '.join(args_repr)}")
        return func(*args, **kwargs)
    return wrapper

class Logger:
    _C = {                     # foreground colours
        "RESET":  "\033[0m",
        "INFO":   "\033[0;32m",   # green
        "WARNING":"\033[0;33m",   # yellow
        "ERROR":  "\033[0;31m",   # red
        "DEBUG":  "\033[0;36m",   # cyan
        "MAJOR":  "\033[1;35m",   # magenta (bold)
        "DEEP_DEBUG": "\033[90m",   # dark gray
    }

    DEBUG = False
    DEEP_DEBUG = False

    def __init__(self, name: str):
        self.name = name

    def info(self, msg):
        print(f"{self._C['INFO']}[INFO] {self.name}: {msg}{self._C['RESET']}")

    def warning(self, msg):
        print(f"{self._C['WARNING']}[WARNING] {self.name}: {msg}{self._C['RESET']}")

    def error(self, msg):
        print(f"{self._C['ERROR']}[ERROR] {self.name}: {msg}{self._C['RESET']}")

    def debug(self, msg):
        if Logger.DEBUG:
            print(f"{self._C['DEBUG']}[DEBUG] {self.name}: {msg}{self._C['RESET']}")
    
    def deepDebug(self, msg):
        if Logger.DEEP_DEBUG:
            print(f"{self._C['DEEP_DEBUG']}[DEEP_DEBUG] {self.name}: {msg}{self._C['RESET']}")

    def majorInfo(self, msg):
        print(f"{self._C['MAJOR']}======================================================================{self._C['RESET']}")
        print(f"{self._C['MAJOR']}[MAJOR] {self.name}: {msg}{self._C['RESET']}")
        print(f"{self._C['MAJOR']}======================================================================{self._C['RESET']}")
