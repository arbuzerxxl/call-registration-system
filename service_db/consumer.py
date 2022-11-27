import pika
from logger import logger
import os
import json
from aio_pika import connect_robust


class Consumer:

    LOGIN = os.environ.get('RABBITMQ_DEFAULT_USER', 'rabbit')
    PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS', 'mypassword')

    def __init__(self, process_callable):

        credentials = pika.PlainCredentials(self.LOGIN, self.PASSWORD)
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'),
                                      credentials=credentials,
                                      heartbeat=3600,
                                      connection_attempts=3,
                                      port=5672,
                                      virtual_host='/')
        )
        self._channel = self._connection.channel()

        self._process_callable = process_callable
        logger.info('Успешное подключение к RabbitMQ')

    async def consume(self, loop):
        """Подключение слушателя очереди"""

        connection = await connect_robust(host=os.environ.get('RABBIT_HOST', 'localhost'),
                                          login=self.LOGIN,
                                          password=self.PASSWORD,
                                          port=5672,
                                          loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(os.environ.get('CONSUME_QUEUE', 'user_appeals'))
        await queue.consume(self.process_incoming_message, no_ack=False)
        logger.info('Очередь подключена к форме')
        return connection

    async def process_incoming_message(self, message):
        """Отображение полученного сообещния в логи"""

        await message.ack()
        body = message.body
        if body:
            self._process_callable(json.loads(body))

    def disconnect(self):

        self._connection.close()
