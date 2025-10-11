from multiprocessing import Process
import time


def do_something() -> None:
    print("I'm going to sleep")
    time.sleep(1)
    print("I'm awake")


# Create new child process

process_1 = Process(target=do_something)
process_2 = Process(target=do_something)

process_1.start()
process_2.start()


# Join forces the child process to complete before Main Process Exits.

process_1.join()
process_2.join()


print("From Main Process.")
