#!/usr/bin/env python

import pika
import time

# тут правим логин/пароль пользователя RabbitMQ
credentials = pika.PlainCredentials('rabbit', 'mypassword')

# тут правим IP RabbitMQ и виртуал_хост (/)
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()


# запускаем цикл
number = 0

while number < 50:
    time.sleep(2)

# тут правим exchange на свой
    channel.basic_publish(exchange='test',
                          routing_key='queues-test',
                          body='Rabbitmq from python!')
    print("[x] Sent Message")
    number += 1
connection.close()
