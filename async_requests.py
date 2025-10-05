import asyncio
import aiohttp
from codetiming import Timer


async def task(name: str, work_queue: asyncio.Queue[str]) -> None:
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url: str = await work_queue.get()
            print(f"Task {name} getting URL: {url}")
            timer.start()
            async with session.get(url) as response:
                await response.text()
            timer.stop()


async def main() -> None:
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue: asyncio.Queue[str] = asyncio.Queue()

    # Put some work in the queue
    for url in [
        "http://google.com",
        "http://yahoo.com",
        "http://linkedin.com",
        "http://apple.com",
        "http://microsoft.com",
        "http://facebook.com",
        # "http://twitter.com",
    ]:
        await work_queue.put(url)

    # Run the tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


if __name__ == "__main__":
    asyncio.run(main())
