import time


def count() -> None:
    print("One")
    time.sleep(1)
    print("Two")
    time.sleep(2)


def main() -> None:
    for _ in range(3):
        count()


if __name__ == "__main__":
    start: float = time.perf_counter()
    main()
    elapsed: float = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed:.2f} seconds.")
