"""The next version of the program has been modified quite a bit. It makes use of Python async features using asyncio/await provided in Python 3.

The time and queue modules have been replaced with the asyncio package. This gives your program access to asynchronous friendly (non-blocking) sleep and queue functionality. The change to task() defines it as asynchronous with the addition of the async prefix on line 4. This indicates to Python that the function will be asynchronous.

The other big change is removing the time.sleep(delay) and yield statements, and replacing them with await asyncio.sleep(delay). This creates a non-blocking delay that will perform a context switch back to the caller main().

The while loop inside main() no longer exists. Instead of task_array, there’s a call to await asyncio.gather(...). This tells asyncio two things:

Create two tasks based on task() and start running them.
Wait for both of these to be completed before moving forward.
The last line of the program asyncio.run(main()) runs main(). This creates what’s known as an event loop). It’s this loop that will run main(), which in turn will run the two instances of task().

The event loop is at the heart of the Python async system. It runs all the code, including main(). When task code is executing, the CPU is busy doing work. When the await keyword is reached, a context switch occurs, and control passes back to the event loop. The event loop looks at all the tasks waiting for an event (in this case, an asyncio.sleep(delay) timeout) and passes control to a task with an event that’s ready.

await asyncio.sleep(delay) is non-blocking in regards to the CPU. Instead of waiting for the delay to timeout, the CPU registers a sleep event on the event loop task queue and performs a context switch by passing control to the event loop. The event loop continuously looks for completed events and passes control back to the task waiting for that event. In this way, the CPU can stay busy if work is available, while the event loop monitors the events that will happen in the future."""

import asyncio
from codetiming import Timer


async def task(name: str, work_queue: asyncio.Queue[int]) -> None:
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    while not work_queue.empty():
        delay: int = await work_queue.get()
        print(f"Task {name} running")
        timer.start()
        await asyncio.sleep(delay)
        timer.stop()


async def main() -> None:
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue: asyncio.Queue[int] = asyncio.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)

    # Run the tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


if __name__ == "__main__":
    asyncio.run(main())
