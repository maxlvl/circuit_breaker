from time import time
from .error import CircuitBreakerError
import threading

# TODO: Implement half-open state
# TODO: implement register method to register a circuit breaker
# TODO: implement get_circuits method to get a list of multiple circuit breakers
# TODO: Figure out what other interface is required to work with circuitbreakers (what are the use cases?)
# TODO: Build in proper docstrings
# TODO: figure out what kind of errors the circuitbreaker should be counting? Should this be part of the config / interface
# the caller can decide what errors to keep track of in the circuitbreaker?


class CircuitBreaker:
    def __init__(self, max_failures: int, reset_timeout: time):
        self.max_failures: int = max_failures
        self.reset_timeout: time = reset_timeout
        self.current_failures: int = 0
        self.tripped: bool = False
        self.timer: threading.Timer = None

    def _trip_breaker(self) -> None:
        print("TRIPPING BREAKER")
        self.tripped = True

    def _reset_breaker(self) -> None:
        print("RESETTING BREAKER")
        self.current_failures = 0
        self.tripped = False

    def _half_open_breaker(self) -> None:
        print("SETTING TO HALF OPEN STATE")
        self.tripped = False

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if not self.tripped:
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    self.current_failures += 1
                    if self.current_failures >= self.max_failures:
                        # set state to 'open'
                        self._trip_breaker()
                        # this will take care of setting it to a half_open state
                        # if we're still getting an error, it'll get incrememented and trip immediately
                        # this avoids cascading failures by limiting the number of requests that can
                        # pass through the circuit breaker while the underlying system is in a vulnerable state
                        self.timer = threading.Timer(
                            self.reset_timeout, self._half_open_breaker
                        ).start()
                        raise
                else:
                    # set the state to closed
                    self._reset_breaker()
                    self.timer.cancel()
                    return result
            else:
                raise CircuitBreakerError("CircuitBreaker was tripped")

        return wrapper
