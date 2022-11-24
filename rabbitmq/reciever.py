#!/usr/bin/env python
import pika, sys, os, time

credentials = pika.PlainCredentials('rabbit', 'mypassword')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)


def main():
    time.sleep(1)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f"[x] Received: {body}")

# тут меняем название очереди на свое
    channel.basic_consume(queue='queues-test', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
