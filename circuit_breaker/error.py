class CircuitBreakerTrippedError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        # TODO: figure out better error code
        self.code = 512

    def __str__(self) -> None:
        return repr(self.message)
