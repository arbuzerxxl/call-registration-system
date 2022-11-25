
import asyncio
import ujson
import requests
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


def make_request(item):
    url = "http://localhost:8888/"
    headers = {}

    # payload = ujson.dumps(item)
    files = []

    response = requests.request("POST", url, headers=headers, data=item, files=files)
    print(response.status_code)
    return response  # чтобы потом можно было понять, на что это ответ


def main():

    data = []

    for i in range(1):
        user_form = {
            "last_name": random.choice(LAST_NAMES),
            "first_name": random.choice(FIRST_NAMES),
            "patronymic": random.choice(PATRONYMIC),
            "phone_number": random.randrange(89000000000, 90000000000),
            "appeal": "TEST"
        }
        data.append(user_form)

    for item in data:
        make_request(item)


if __name__ == "__main__":
    main()
