import pika
import time
import aio_pika


class RabbitMqConsumer():

    async def async_init(self, exchange_name, routing_key, queue_name, callback):
        time.sleep(10)
        conn = await aio_pika.connect_robust("amqp://guest:guest@docker.for.mac.localhost")
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
