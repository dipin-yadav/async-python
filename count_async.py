import time
import asyncio


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")
    await asyncio.sleep(2)


async def main():
    await asyncio.gather(count(), count(), count())


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed:.2f} seconds.")
