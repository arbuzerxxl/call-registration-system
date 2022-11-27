import aiohttp
import asyncio
import random
import ujson
import time


LAST_NAMES = [
    'Белов', 'Сидоров', 'Иванов', 'Петров', 'Игнатьев',
]

FIRST_NAMES = [
    'Сергей', 'Дмитрий', 'Петр', 'Иван', 'Олег',
]

PATRONYMIC = [
    'Сергевич', 'Петрович', 'Андреевич', 'Николаевич', 'Александрович',
]

reqs = []

data = []


async def make_request(item):

    number_of_queue = item.pop("number_of_queue")

    payload = ujson.dumps(item)

    delay = random.randint(1, 20)

    await asyncio.sleep(delay)

    async with aiohttp.ClientSession(trust_env=True) as session:

        headers = {}

        async with session.post('http://172.20.0.5:8888/appeal', data=payload, headers=headers) as response:

            pass

            print(f"Status: {response.status}", flush=False)
            print(f"Content-type: {response.headers['content-type']}", flush=False)
            print(f"Number of queue: {number_of_queue}", flush=False)


async def main():

    # планируем одновременные вызовы
    await asyncio.gather(*reqs)


if __name__ == '__main__':
    for i in range(10000):
        user_form = {
            "last_name": random.choice(LAST_NAMES),
            "first_name": random.choice(FIRST_NAMES),
            "patronymic": random.choice(PATRONYMIC),
            "phone_number": random.randrange(89000000000, 90000000000),
            "appeal": "TEST",
            "number_of_queue": i
        }

        data.append(user_form)

    for item in data:
        reqs.append(make_request(item))
    # Запускаем цикл событий
    results = asyncio.run(main())
