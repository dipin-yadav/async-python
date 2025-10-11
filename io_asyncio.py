import asyncio
import time

import aiohttp


async def main() -> None:
    sites: list[str] = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time: float = time.perf_counter()
    await download_all_sites(sites)
    duration: float = time.perf_counter() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")


async def download_all_sites(sites: list[str]) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = [download_site(url, session) for url in sites]
        await asyncio.gather(*tasks, return_exceptions=True)


async def download_site(url: str, session: aiohttp.ClientSession) -> None:
    async with session.get(url) as response:
        print(f"Read {len(await response.read())} bytes from {url}")


if __name__ == "__main__":
    asyncio.run(main())
