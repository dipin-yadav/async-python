import time

import requests


def main() -> None:
    sites: list[str] = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time: float = time.perf_counter()
    download_all_sites(sites)
    duration: float = time.perf_counter() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")


def download_all_sites(sites: list[str]) -> None:
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


def download_site(url: str, session: requests.Session) -> None:
    with session.get(url) as response:
        print(f"Read {len(response.content)} bytes from {url}")


if __name__ == "__main__":
    main()
