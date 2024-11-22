from app.domain.rabbit_mq_routing_keys import RabbitmqRoutingKeys
from app.util.base_publisher import RabbitMqPublisher


class EmbeddingsProducer(RabbitMqPublisher):

    def __init__(self, exchange_name="data_scrape_exchange"):
        super().__init__(exchange_name)

    def send_embeddings_job(self, message):
        self.send_message_to_queue(routing_key=RabbitmqRoutingKeys.CREATE_EMBEDDINGS.name,
                                   message=message)