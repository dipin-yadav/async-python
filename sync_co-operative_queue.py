"""The next version of the program allows the two tasks to work together. Adding a yield statement means the loop will yield control at the specified point while still maintaining its context. This way, the yielding task can be restarted later.

The yield statement turns task() into a generator. A generator function is called just like any other function in Python, but when the yield statement is executed, control is returned to the caller of the function. This is essentially a context switch, as control moves from the generator function to the caller.

The interesting part is that control can be given back to the generator function by calling next() on the generator. This is a context switch back to the generator function, which picks up execution with all function variables that were defined before the yield still intact.

The while loop in main() takes advantage of this when it calls next(t). This statement restarts the task at the point where it previously yielded. All of this means that you’re in control when the context switch happens: when the yield statement is executed in task().

This is a form of cooperative multitasking. The program is yielding control of its current context so that something else can run. In this case, it allows the while loop in main() to run two instances of task() as a generator function. Each instance consumes work from the same queue. This is sort of clever, but it’s also a lot of work to get the same results as the first program. The program example_2.py demonstrates this simple concurrency and is listed below:"""

import queue
from typing import Any, Generator


def task(name: str, queue: queue.Queue[int]) -> Generator[None, Any, None]:
    while not queue.empty():
        count: int = queue.get()
        total = 0
        print(f"Task {name} running")
        for _ in range(count):
            total += 1
            # Context Switch happens and control goes back to main() -> next(t)
            yield
        print(f"Task {name} total: {total}")


def main() -> None:
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue: queue.Queue[int] = queue.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    # Create some tasks
    tasks: list[Generator[None, Any, None]] = [
        task("One", work_queue),
        task("Two", work_queue),
    ]

    # Run the tasks
    done = False
    while not done:
        for t in tasks:
            try:
                # Context Start from here,
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                print("All Tasks completed.")
                done = True


if __name__ == "__main__":
    main()


""" You can see that both Task One and Task Two are running and consuming work from the queue. This is what’s intended, as both tasks are processing work, and each is responsible for two items in the queue. This is interesting, but again, it takes quite a bit of work to achieve these results.

The trick here is using the yield statement, which turns task() into a generator and performs a context switch. The program uses this context switch to give control to the while loop in main(), allowing two instances of a task to run cooperatively.

Notice how Task Two outputs its total first. This might lead you to think that the tasks are running asynchronously. However, this is still a synchronous program. It’s structured so the two tasks can trade contexts back and forth. The reason why Task Two outputs its total first is that it’s only counting to 10, while Task One is counting to 15. Task Two simply arrives at its total first, so it gets to print its output to the console before Task One """
