import asyncio
import logging
from fastapi import FastAPI
from pony.orm import db_session
from consumer import Consumer
from models import UserAppealDB, UserAppeal


UserAppealDB.generate_mapping(create_tables=True)


class App(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer = Consumer(self.write_incoming_message_to_db)
        try:
            self.consumer.run()
        except KeyboardInterrupt:
            self.consumer.disconnect()
        except Exception:
            self.consumer.disconnect()

    @classmethod
    @db_session
    def write_incoming_message_to_db(cls, message: dict):
        """Заносит обращение в БД"""

        UserAppeal(**message)

        logger.info("Обращение зарегистрированно в БД")


def configure_logging():

    global logger

    logger = logging.getLogger('FastAPILog')
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
        fmt='%(levelname) -9s [%(asctime)s] %(name) -15s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S'
    )
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)


configure_logging()
app = App()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.consumer.consume(loop))
    await task
