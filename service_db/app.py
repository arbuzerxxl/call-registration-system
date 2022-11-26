import asyncio
import uvicorn
from fastapi import FastAPI
from pony.orm import db_session
from consumer import Consumer
from logger import logger, configure_logging
from models import db_user_appeal, UserAppeal


db_user_appeal.generate_mapping(create_tables=True)


class App(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = Consumer(self.log_incoming_message)

    @classmethod
    @db_session
    def log_incoming_message(cls, message: dict):
        """Выводит сообщение, полученное из очереди, в логи"""
        logger.info(f'Получено сообщение из очереди: {message}')
        UserAppeal(**message)
        logger.info(f'Обращение зарегистрированно в БД')


app = App()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.Consumer.consume(loop))
    await task


if __name__ == "__main__":
    configure_logging()
    uvicorn.run(app, host='localhost', port=8001)
