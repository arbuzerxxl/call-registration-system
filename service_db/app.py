import asyncio
from fastapi import FastAPI
from pika_client import PikaClient
from logger import logger, configure_logging
from models import db_user_appeal, UserAppeal
import uvicorn
from pony.orm import db_session


db_user_appeal.generate_mapping(create_tables=True)


class App(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    @db_session
    def log_incoming_message(cls, message: dict):
        """Выводит полученное с очереди сообщение в логи"""
        UserAppeal(
            last_name=message.get("last_name", None),
            first_name=message.get("first_name", None),
            patronymic=message.get("patronymic", None),
            phone_number=message.get("phone_number", None),
            appeal=message.get("appeal", None))
        logger.info('Получили сообщение: %s', message)


app = App()
configure_logging()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


if __name__ == "__main__":
    configure_logging()
    uvicorn.run(app, host='localhost', port=8001)
