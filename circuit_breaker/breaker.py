from time import time
from .error import CircuitBreakerTrippedError

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
        self.last_failure_time: time = None

    def _trip_breaker(self) -> None:
        self.tripped = True

    def _reset_breaker(self) -> None:
        self.current_failures = 0
        self.tripped = False

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.tripped:
                if time() - self.last_failure_time > self.reset_timeout:
                    self._reset_breaker()
                else:
                    raise CircuitBreakerTrippedError(
                        message="Circuit breaker is tripped"
                    )
            try:
                return func(*args, **kwargs)
            except Exception:
                self.current_failures += 1
                if self.current_failures >= self.max_failures:
                    self._trip_breaker()
                    self.last_failure_time = time()

        return wrapper
