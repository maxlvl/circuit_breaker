from time import sleep
from short_circuit.breaker import CircuitBreaker
import requests

cb = CircuitBreaker(max_failures=3, reset_timeout=3)


@cb
def ping_site(site):
    try:
        if not site:
            r = requests.get("http://thisbakldaskflwsdj.com")
        else:
            r = requests.get(site)
            print("SUCCESFUL QUERY")
    except Exception:
        raise


def repeat_ping(site=None):
    try:
        ping_site(site)
    except Exception:
        sleep(4)
        site = "http://www.google.com"
        print(f"sleeping 4 secs, site is {site}")
        ping_site(site)


if __name__ == "__main__":
    repeat_ping()
