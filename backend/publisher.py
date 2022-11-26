#!/usr/bin/env python

import pika
import os
from pika.exchange_type import ExchangeType
from logger import logger


class Publisher:

    QUEUE_NAME = os.environ.get('CONSUME_QUEUE', 'user_appeals')
    EXCHANGE_NAME = os.environ.get('EXCHANGE_NAME', 'exchange_appeals')
    LOGIN = os.environ.get('RABBIT_LOGIN', 'rabbit')
    PASSWORD = os.environ.get('RABBIT_PASSWORD', 'mypassword')
    EXCHANGE_TYPE = ExchangeType.fanout

    def __init__(self):

        self._channel = None
        self._connection = None
        self.connect_to_channel()
        self.setup_exchange()
        self.setup_queue()
        self.queue_bind()
        self.disconnect()

    def setup_exchange(self):

        self._channel.exchange_declare(
            exchange=self.EXCHANGE_NAME,
            exchange_type=self.EXCHANGE_TYPE,
        )

    def setup_queue(self):

        self._channel.queue_declare(
            queue=self.QUEUE_NAME,
        )

    def queue_bind(self):

        self._channel.queue_bind(
            queue=self.QUEUE_NAME,
            exchange=self.EXCHANGE_NAME,
        )

    def connect_to_channel(self):

        credentials = pika.PlainCredentials(self.LOGIN, self.PASSWORD)

        parameters = pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'),
                                               port=os.environ.get('RABBIT_PORT', '5672'),
                                               virtual_host='/',
                                               credentials=credentials)

        connection = pika.BlockingConnection(parameters)
        # connection = pika.SelectConnection(parameters=parameters)

        self._connection = connection

        channel = connection.channel()

        self._channel = channel

    def publish(self, body):

        self._channel.basic_publish(exchange=self.EXCHANGE_NAME,
                                    routing_key=f'{self.QUEUE_NAME}-{self.EXCHANGE_NAME}',
                                    body=body)

        logger.info(f'Сообщение опубликовано в очереди: {self.QUEUE_NAME}')

    def disconnect(self):

        self._connection.close()
