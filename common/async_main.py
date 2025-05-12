import asyncio
import time
from asyncio.futures import Future
from utils import delay, async_timed
import requests
import aiohttp


def add_one(number: int) -> int:
    return number + 1


async def async_add_one(number: int) -> int:
    await asyncio.sleep(number)
    return number + 1


async def timer(duration: int):
    for i in range(duration):
        await asyncio.sleep(1)
        print("I'm running other code while I'm waiting!")


async def main():
    sleep_for_three = asyncio.create_task(delay(4))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(5))
    # timer_task = asyncio.create_task(timer(5))

    print("this is executed immediately")

    await timer(5)
    await sleep_for_three
    await sleep_again
    await sleep_once_more

    print("this not is executed immediately")


async def not_main():
    sleep_for_three = asyncio.create_task(delay(10))
    sleep_again = asyncio.create_task(delay(5))
    sleep_once_more = asyncio.create_task(delay(12))

    await sleep_for_three
    await sleep_again
    await sleep_once_more

    print("this not is executed immediately")


async def not_not_main():
    delayed_task = asyncio.create_task(delay(3))

    print(type(delayed_task))

    try:
        result = await asyncio.wait_for(asyncio.shield(delayed_task), timeout=1.5)
        print(result)
    except asyncio.TimeoutError as e:
        print("got a timeout!")
        print(str(e))
        print(f"is task cancelled: {delayed_task.cancelled()}")

        result = await delayed_task

        print(type(result))
        print(result)

        print(f"DELAYED TASK RESULT: {delayed_task.result()}")


def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_result(future))

    return future


async def set_future_result(future: Future):
    await delay(2)

    future.set_result(42)


@async_timed()
async def cpu_bound_task() -> int:
    counter = 0

    for i in range(100000000):
        counter += 1

    return counter


@async_timed()
async def make_request_sync(url: str = "http://www.example.com"):
    response = requests.get(url)

    return response.status_code


@async_timed()
async def make_request_async(url: str = "http://www.example.com"):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.status


@async_timed()
async def main_request():
    url = "https://6b2d349e-6621-436f-9c4d-655632a679e4.mock.pstmn.io"

    # delay_task = asyncio.create_task(delay(3))
    task_one = asyncio.create_task(make_request_sync())
    task_two = asyncio.create_task(make_request_sync())

    # await delay_task
    status = await task_one
    status1 = await task_two

    print(status)
    print(status1)


if __name__ == "__main__":
    # start = time.time()

    # # asyncio.run(main())
    # asyncio.run(main_request())

    event_loop = asyncio.new_event_loop()

    try:
        event_loop.run_until_complete(main_request())
    finally:
        event_loop.close()
    # end = time.time()

    # print(f"Completed in {end - start:.4f} seconds.")
