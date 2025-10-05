import asyncio
import random
import time


async def main() -> None:
    queue: asyncio.Queue[dict[str, str | int] | None] = asyncio.Queue()
    user_ids: list[int] = [1, 2, 3]

    start: float = time.perf_counter()
    await asyncio.gather(
        producer(queue, user_ids),
        *(consumer(queue) for _ in user_ids),
    )
    end: float = time.perf_counter()
    print(f"\n==> Total time: {end - start:.2f} seconds")


async def producer(
    queue: asyncio.Queue[dict[str, str | int] | None], user_ids: list[int]
) -> None:
    async def fetch_user(user_id: int) -> None:
        delay: float = random.uniform(0.5, 2.0)
        print(f"Producer: fetching user by {user_id=}...")
        await asyncio.sleep(delay)
        user: dict[str, str | int] = {"id": user_id, "name": f"User{user_id}"}
        print(f"Producer: fetched user with {user_id=} (done in {delay:.1f}s)")
        await queue.put(user)

    await asyncio.gather(*(fetch_user(uid) for uid in user_ids))
    for _ in range(len(user_ids)):
        await queue.put(None)  # Sentinels for consumers to terminate


async def consumer(queue: asyncio.Queue[dict[str, str | int] | None]) -> None:
    while True:
        user: dict[str, str | int] | None = await queue.get()
        if user is None:
            break
        delay: float = random.uniform(0.5, 2.0)
        print(f"Consumer: retrieving posts for {user['name']}...")
        await asyncio.sleep(delay)
        posts: list[str] = [f"Post {i} by {user['name']}" for i in range(1, 3)]
        print(
            f"Consumer: got {len(posts)} posts by {user['name']}"
            f" (done in {delay:.1f}s):"
        )
        for post in posts:
            print(f"  - {post}")


if __name__ == "__main__":
    random.seed(444)
    asyncio.run(main(), debug=True)
