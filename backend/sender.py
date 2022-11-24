#!/usr/bin/env python

import pika
import os
from pika.exchange_type import ExchangeType


class SenderToRabbit:

    QUEUE_NAME = "appeal2"
    EXCHANGE_NAME = "test2"
    EXCHANGE_TYPE = ExchangeType.fanout
    LOGIN = 'rabbit'
    PASSWORD = 'mypassword'

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

        parameters = pika.ConnectionParameters(host='localhost',
                                               port=5672,
                                               virtual_host='/',
                                               credentials=credentials)

        connection = pika.BlockingConnection(parameters)

        self._connection = connection

        channel = connection.channel()

        self._channel = channel

    def publish(self, body):

        self._channel.basic_publish(exchange=self.EXCHANGE_NAME,
                                    routing_key=f'{self.QUEUE_NAME}-{self.EXCHANGE_NAME}',
                                    body=body)
        print("[x] Sent Message")

    def disconnect_from_channel(connection: object):

        connection.close()


def main():

    # logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    sender = SenderToRabbit()
    try:
        sender.connect_to_channel()
    except KeyboardInterrupt:
        sender.stop()


if __name__ == '__main__':
    main()
