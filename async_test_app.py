import aiohttp
import asyncio
import random
import ujson


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

        async with session.post(f'http://{host}:{port}/appeal', data=payload, headers=headers) as response:

            print(f"Number of queue: {number_of_queue} \n", flush=False)
            print(f"Status: {response.status}", flush=False)
            print(f"Content-type: {response.headers['content-type']}", flush=False)


async def main():

    # планируем одновременные вызовы
    await asyncio.gather(*reqs)

TEST_INTO_CONTAINER = False  # изменить на True при количестве запросов более 500

if TEST_INTO_CONTAINER:
    host = "172.20.0.4"  # заполнить значение вывода команды "sudo docker container inspect backend | grep -i IPAddress"
    port = "8888"
else:
    host = "localhost"
    port = "82"

if __name__ == '__main__':
    for i in range(2000):
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
