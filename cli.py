from time import sleep
from circuit_breaker.breaker import CircuitBreaker
import requests

cb = CircuitBreaker(max_failures=3, reset_timeout=1)


@cb
def ping_site():
    r = requests.get("http://thisbakldaskflwsdj.com")


if __name__ == "__main__":
    try:
        for i in range(1000):
            ping_site()
    except Exception:
        print("SLEEPING 2 SECS")
        sleep(2)
        for i in range(100):
            ping_site()
