import asyncio
import random

COLORS = (
    "\033[0m",
    "\033[36m",
    "\033[91m",
    "\033[35m",
)


async def make_random(delay, threshold):
    color = COLORS[delay]
    print(f"{color}Initiated make_random({delay}).")
    while (number := random.randint(0, 10)) <= threshold:
        print(f"{color}make_random({delay}) == {number} too low; retrying.")
        await asyncio.sleep(delay)
    print(f"{color}---> Finished: make_random({delay}) == {number}" + COLORS[0])
    return number


async def main():
    return await asyncio.gather(
        make_random(1, 9),
        make_random(2, 8),
        make_random(3, 8),
    )


if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")
