# PyCircuitBreaker

A simple Python library that provides the CircuitBreaker pattern as a function decorator.

## Context
A simple Python implementation of the CircuitBreaker pattern, as popularized by Michael T. Nygard in his book "Release it!: Design and Deploy Production-Ready Software" (Pragmatic Bookshelf, 2007)

The circuit breaker pattern is described as a way to protect a system from excessive requests that could cause it to fail. The idea is to use a "circuit breaker" to monitor the system's performance and trip (i.e., open) the circuit if the system becomes overloaded or unresponsive. This prevents further requests from reaching the system and allows it to recover. 

The circuit breaker pattern has become a popular way to handle failures in distributed systems, and it is used in many different contexts, including web services, microservices, and distributed databases. It is particularly useful in systems that rely on remote resources or services, as it helps to prevent failures from propagating and causing widespread outages.


## Features
This implementation aims to provide the following:
- Closed state: in this state, the circuit breaker will allow through unlimited requests as long as they continue to succeed.
- Open state: in this state, the circuit breaker has "tripped", not allowing any requests to be made until a preconfigured timeout has expired
- Half-open state: in this state, the circuit breaker will allow a new request, but will immediately "trip" if that request fails. If the request succeeds, it will 'close' the circuit again, allowing requests to proceed. The idea behind this state is to carefully allow requests to pass through again without overloading the underlying system and causing more cascading failures. This 'reset' functionality is configured by a `timeout` variable. 

## Usage
Current interface allows for the use of a single circuit breaker as a function decorator
```
cb = CircuitBreaker(max_failures=3, reset_timeout=3)

@cb
def foo():
    # do stuff
```

The function decorator pattern allows a user to decorate multiple functions with a single breaker if so desired, depending on which underlying services are being called.

## TODO
- Allow to `register` circuit breakers, as well as provide an interface to interact with the various breakers (get stats, manually manipulate breakers if needed)
- Allow for a singleton breaker to be used across an entire client (maybe)