import queue


def task(name: str, work_queue: queue.Queue[int]) -> None:
    if work_queue.empty():
        print(f"Task {name} nothing to do")
    else:
        while not work_queue.empty():
            count = work_queue.get()
            total = 0
            print(f"Task {name} running")
            for _ in range(count):
                total += 1
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

    # Create some synchronous tasks
    tasks = [(task, "One", work_queue), (task, "Two", work_queue)]

    # Run the tasks
    for t, n, q in tasks:
        t(n, q)


if __name__ == "__main__":
    main()
