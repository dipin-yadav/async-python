"""The next version of the program is the same as the last, except for the addition of a time.sleep(delay) in the body of your task loop. This adds a delay based on the value retrieved from the work queue to every iteration of the task loop. The delay simulates the effect of a blocking call occurring in your task.

A blocking call is code that stops the CPU from doing anything else for some period of time. In the thought experiments above, if a parent wasn’t able to break away from balancing the checkbook until it was complete, that would be a blocking call.

time.sleep(delay) does the same thing in this example, because the CPU can’t do anything else but wait for the delay to expire."""

import time
import queue
from typing import Any, Generator
from codetiming import Timer


def task(name: str, queue: queue.Queue[int]) -> Generator[None, Any, None]:
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    while not queue.empty():
        delay: int = queue.get()
        print(f"Task {name} running")
        timer.start()
        time.sleep(delay)
        timer.stop()
        # Context Switch to main() -> next(t)
        yield


def main() -> None:
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue: queue.Queue[int] = queue.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    tasks: list[Generator[None, Any, None]] = [
        task("One", work_queue),
        task("Two", work_queue),
    ]

    # Run the tasks
    done = False
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        while not done:
            for t in tasks:
                try:
                    # Context Start
                    next(t)
                except StopIteration:
                    tasks.remove(t)
                if len(tasks) == 0:
                    print("All tasks completed.")
                    done = True


if __name__ == "__main__":
    main()


""" As before, both Task One and Task Two are running, consuming work from the queue and processing it. However, even with the addition of the delay, you can see that cooperative concurrency hasn’t gotten you anything. The delay stops the processing of the entire program, and the CPU just waits for the IO delay to be over.

This is exactly what’s meant by blocking code in Python async documentation. You’ll notice that the time it takes to run the entire program is just the cumulative time of all the delays. Running tasks this way is not a win. """
