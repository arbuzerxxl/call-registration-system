#!/usr/bin/env python

import pika
import logging
import os
from pika.exchange_type import ExchangeType


def configure_logging():

    global logger

    logger = logging.getLogger('PublisherLog')
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
        fmt='%(levelname) -10s [%(asctime)s] %(name) -15s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S'
    )
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)


class Publisher:

    QUEUE_NAME = os.environ.get('CONSUME_QUEUE', 'user_appeals')
    EXCHANGE_NAME = os.environ.get('EXCHANGE_NAME', 'exchange_appeals')
    LOGIN = os.environ.get('RABBITMQ_DEFAULT_USER', 'rabbit')
    PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS', 'mypassword')
    EXCHANGE_TYPE = ExchangeType.fanout

    def __init__(self):

        self._channel = None
        self._connection = None

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

        params = pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'),
                                           port=os.environ.get('RABBIT_PORT', '5672'),
                                           virtual_host='/',
                                           heartbeat=3600,
                                           connection_attempts=3,
                                           credentials=credentials)

        self._connection = pika.BlockingConnection(parameters=params)

        self._channel = self._connection.channel()

    def publish(self, body):

        self._channel.basic_publish(exchange=self.EXCHANGE_NAME,
                                    routing_key=f"{self.QUEUE_NAME}-{self.EXCHANGE_NAME}",
                                    body=body)

        logger.info(f'Сообщение опубликовано в очереди: {self.QUEUE_NAME}')

    def disconnect(self):

        logger.info("Отключение от очереди..")

        self._connection.close()

    def run(self):

        configure_logging()

        logger.info("Подключение к RabbitMQ..")

        self.connect_to_channel()
        self.setup_exchange()
        self.setup_queue()
        self.queue_bind()

        logger.info("Подключение к RabbitMQ выполнено")
