import pika
import time
import aio_pika
import os

class RabbitMqConsumer():

    async def async_init(self, exchange_name, routing_key, queue_name, callback):
        time.sleep(10)
        username = os.environ.get('RABBITMQ_USERNAME', 'guest')
        password = os.environ.get('RABBITMQ_PASSWORD', 'guest')
        host = os.environ.get('RABBITMQ_HOST', 'docker.for.mac.localhost')
        conn = await aio_pika.connect_robust(f"amqp://{username}:{password}@{host}")
        channel = await conn.channel()
        exchange = await channel.declare_exchange(exchange_name, type="topic")
        queue = await channel.declare_queue(name=queue_name)
        await queue.bind(exchange, routing_key=routing_key)
        print(f"Listening to queue {queue_name}.")
        async def x(message):
            async with message.process():
                # Get the routing key from the message
                routing_key = message.routing_key
                print("Received message with routing key:", routing_key)
                print("Message body:", message.body.decode())
        await queue.consume(callback)

    def callback(self, ch, method, properties, body):
        print(f"Received message: {body}")
