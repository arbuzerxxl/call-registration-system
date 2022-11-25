import aiohttp
import asyncio
import random


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

    async with aiohttp.ClientSession() as session:
        headers = {}
        files = []
        async with session.get('http://localhost:82', data=item, headers=headers) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])


async def main():

    # планируем одновременные вызовы
    await asyncio.gather(*reqs)


if __name__ == '__main__':
    for i in range(50000):
        user_form = {
            "last_name": random.choice(LAST_NAMES),
            "first_name": random.choice(FIRST_NAMES),
            "patronymic": random.choice(PATRONYMIC),
            "phone_number": random.randrange(89000000000, 90000000000),
            "appeal": "TEST"
        }

        data.append(user_form)

    for item in data:
        reqs.append(make_request(item))
    # Запускаем цикл событий
    results = asyncio.run(main())
