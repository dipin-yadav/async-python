import asyncio
import random
import time


async def main() -> None:
    user_ids: list[int] = [1, 2, 3]
    start: float = time.perf_counter()
    await asyncio.gather(*(get_user_with_posts(user_id) for user_id in user_ids))
    end: float = time.perf_counter()
    print(f"\n==> Total time: {end - start:.2f} seconds")


async def get_user_with_posts(user_id: int) -> None:
    user: dict[str, str | int] = await fetch_user(user_id)
    await fetch_posts(user)


async def fetch_user(user_id: int) -> dict[str, str | int]:
    delay: float = random.uniform(0.5, 2.0)
    print(f"User coro: fetching user by {user_id=}...")
    await asyncio.sleep(delay)
    user: dict[str, str | int] = {"id": user_id, "name": f"User{user_id}"}
    print(f"User coro: fetched user with {user_id=} (done in {delay:.1f}s).")
    return user


async def fetch_posts(user: dict[str, str | int]) -> None:
    delay: float = random.uniform(0.5, 2.0)
    print(f"Post coro: retrieving posts for {user['name']}...")
    await asyncio.sleep(delay)
    posts: list[str] = [f"Post {i} by {user['name']}" for i in range(1, 3)]
    print(
        f"Post coro: got {len(posts)} posts by {user['name']} (done in {delay:.1f}s):"
    )
    for post in posts:
        print(f" - {post}")


if __name__ == "__main__":
    random.seed(444)
    asyncio.run(main(), debug=True)
