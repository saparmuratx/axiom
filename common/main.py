import os
import threading
import multiprocessing
import time
import requests

# def hello_from_thread():
#     # import os

#     print(f"Inside thread GET PROCESS ID: {os.getpid()}")
#     print(f"Hello from thread {threading.current_thread()}!")


# hello_thread = threading.Thread(target=hello_from_thread)
# hello_thread.start()


def hello_from_process():
    print(f"Hello from child process {os.getpid()}!")


def print_fib(number: int) -> None:
    def fib(n: int) -> int:
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    print(f"PROCESS ID: {os.getpid()}")
    print(f"THREAD: {threading.current_thread()}")
    print(f"fib({number}) is {fib(number)}")


def fibs_no_threading():
    print_fib(30)
    print_fib(31)
    print_fib(30)
    print_fib(31)


def fibs_with_processes():
    hello_process = multiprocessing.Process(target=hello_from_process)
    process = multiprocessing.Process(target=print_fib, args=(40,))
    process2 = multiprocessing.Process(target=print_fib, args=(41,))
    process3 = multiprocessing.Process(target=print_fib, args=(40,))
    process4 = multiprocessing.Process(target=print_fib, args=(41,))

    start = time.time()
    # hello_process.start()
    process.start()
    process2.start()
    # process3.start()
    # process4.start()

    print(f"Hello from parent process {os.getpid()}")

    process.join()
    process2.join()
    # process3.join()
    # process4.join()

    end = time.time()

    # hello_process.join()

    print(f"Completed in {end - start:.4f} seconds.")


def fibs_with_threads():
    process = threading.Thread(target=print_fib, args=(40,))
    process2 = threading.Thread(target=print_fib, args=(41,))
    process3 = threading.Thread(target=print_fib, args=(40,))
    process4 = threading.Thread(target=print_fib, args=(41,))

    start = time.time()
    # hello_process.start()
    process.start()
    process2.start()
    # process3.start()
    # process4.start()

    print(f"Hello from parent process {os.getpid()}")
    total_threads = threading.active_count()
    thread_name = threading.current_thread().name
    print(f"Python is currently running {total_threads} thread(s)")
    print(f"The current thread is {thread_name}")

    process.join()
    process2.join()
    # process3.join()
    # process4.join()

    end = time.time()

    # hello_process.join()

    print(f"Completed in {end - start:.4f} seconds.")


def read_example(url="https://www.example.com", method="GET") -> None:
    if method == "GET":
        response = requests.get(url)
    if method == "POST":
        response = requests.post(url)

    print(response.status_code)
    print(url)


def website_status_sync():
    read_example(
        "https://www.f5.com/company/blog/nginx/api-real-time-test-latency-responsiveness-nginx-rtapi-tool"
    )
    read_example("https://jsonplaceholder.typicode.com/todos")
    read_example("https://www.tinybird.co/docs/forward/monitoring/latency")
    read_example()


def print_thread_info():
    print(f"Hello from parent process {os.getpid()}")
    total_threads = threading.active_count()
    thread_name = threading.current_thread().name
    print(f"Python is currently running {total_threads} thread(s)")
    print(f"The current thread is {thread_name}")


def website_status_threads():
    thread_1 = threading.Thread(
        target=read_example,
        kwargs={
            "url": "https://jsonplaceholder.typicode.com/todos",
            "method": "POST",
        },
    )
    thread_2 = threading.Thread(
        target=read_example,
        kwargs={
            "url": "https://www.f5.com/company/blog/nginx/api-real-time-test-latency-responsiveness-nginx-rtapi-tool"
        },
    )
    thread_3 = threading.Thread(
        target=read_example, kwargs={"url": "https://www.example.com"}
    )
    thread_4 = threading.Thread(
        target=read_example,
        kwargs={"url": "https://www.tinybird.co/docs/forward/monitoring/latency"},
    )

    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()

    print_thread_info()

    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()


if __name__ == "__main__":
    start = time.time()
    # fibs_with_threads()
    # fibs_with_processes()

    # fibs_no_threading()

    # website_status_sync()
    website_status_threads()

    thread_name = threading.current_thread().name
    print(f"The current thread is {thread_name}")

    end = time.time()

    print(f"Completed in {end - start:.4f} seconds.")
