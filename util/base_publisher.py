import pika

from domain.rabbit_mq_routing_keys import RabbitmqRoutingKeys


class RabbitMqPublisher():

    def __init__(self, exchange_name):
        self.exchange = exchange_name

    def send_message_to_queue(self, routing_key: str, message: str):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.basic_publish(exchange=self.exchange,
                              routing_key=f'cmd.{routing_key}',
                              body=message)
        print(f"Sent message to RabbitMQ: {message}")
        connection.close()
