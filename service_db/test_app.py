import asyncio
from fastapi import FastAPI
from pika_client import PikaClient
from logger import logger, configure_logging
from router import router
import uvicorn


class FooApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        logger.info('Here we got incoming message %s', message)


foo_app = FooApp()
foo_app.include_router(router)


@foo_app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(foo_app.pika_client.consume(loop))
    await task


if __name__ == "__main__":
    configure_logging()
    uvicorn.run(foo_app, host='localhost', port=8001)
