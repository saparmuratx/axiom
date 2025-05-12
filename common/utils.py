import functools
import time
from typing import Callable, Any
import asyncio


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with args: {args} and kwargs: {kwargs}")

            start = time.time()

            try:
                return await func(*args, **kwargs)

            finally:
                end = time.time()

                duration = end - start
                print(f"finished {func} in {duration:.4f} seconds")

        return wrapped

    return wrapper


def sync_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with args: {args} and kwargs: {kwargs}")

            start = time.time()

            try:
                return func(*args, **kwargs)

            finally:
                end = time.time()

                duration = end - start
                print(f"finished {func} in {duration:.4f} seconds")

        return wrapped

    return wrapper


@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f"sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    print(f"finished sleeping for {delay_seconds} second(s)")
    return delay_seconds
