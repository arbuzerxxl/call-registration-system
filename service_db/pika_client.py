import pika
import uuid
from logger import logger
import os
import json
from aio_pika import connect_robust


class PikaClient:

    LOGIN = 'rabbit'
    PASSWORD = 'mypassword'

    def __init__(self, process_callable):
        self.publish_queue_name = os.environ.get('PUBLISH_QUEUE', 'foo_publish_queue')
        credentials = pika.PlainCredentials(self.LOGIN, self.PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'), credentials=credentials, port=5672, virtual_host='/')
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        logger.info('Pika connection initialized')

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(host=os.environ.get('RABBIT_HOST', 'localhost'),
                                          login=self.LOGIN,
                                          password=self.PASSWORD,
                                          port=5672,
                                          loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(os.environ.get('CONSUME_QUEUE', 'foo_consume_queue'))
        await queue.consume(self.process_incoming_message, no_ack=False)
        logger.info('Established pika async listener')
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        await message.ack()
        body = message.body
        logger.info('Received message')
        if body:
            self.process_callable(json.loads(body))

    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
