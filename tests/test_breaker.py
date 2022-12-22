from circuit_breaker.breaker import CircuitBreaker
import pytest
from time import sleep

from circuit_breaker.error import CircuitBreakerError


class TestBreaker:
    def test_initial_state(self):
        cb = CircuitBreaker(max_failures=3, reset_timeout=1)
        assert cb.tripped is False
        assert cb.current_failures == 0

