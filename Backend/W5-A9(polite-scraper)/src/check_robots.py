"""Run once: python -m src.check_robots
Requests robots.txt a single time and prints what to paste into the README's
Target classification section."""
import requests
from . import config


def main():
    try:
        resp = requests.get(config.ROBOTS_URL, timeout=config.REQUEST_TIMEOUT_SECONDS,
                             headers={"User-Agent": config.USER_AGENT})
    except requests.exceptions.RequestException as exc:
        print(f"robots.txt request failed: {exc}")
        print('README line: "no robots file found" is NOT accurate here — a request error is not a missing file, note the error instead.')
        return

    if resp.status_code == 404:
        print("robots.txt: 404 — no robots file found.")
    elif resp.status_code == 200:
        print("robots.txt: 200 — contents below, paste the relevant lines into the README:\n")
        print(resp.text)
    else:
        print(f"robots.txt: unexpected status {resp.status_code}")


if __name__ == "__main__":
    main()
