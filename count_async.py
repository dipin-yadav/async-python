import time
import asyncio


async def count() -> None:
    print("One")
    await asyncio.sleep(1)
    print("Two")
    await asyncio.sleep(2)


async def main() -> None:
    await asyncio.gather(count(), count(), count())


if __name__ == "__main__":
    start: float = time.perf_counter()
    asyncio.run(main())
    elapsed: float = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed:.2f} seconds.")
