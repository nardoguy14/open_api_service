from domain.rabbit_mq_routing_keys import RabbitmqRoutingKeys
from util.base_publisher import RabbitMqPublisher


class DataScrapeProducer(RabbitMqPublisher):

    def __init__(self, exchange_name="data_scrape_exchange"):
        super().__init__(exchange_name)

    def send_new_data_scrape_job(self, message):
        self.send_message_to_queue(routing_key=RabbitmqRoutingKeys.CREATE_DATA_SCRAPE.name,
                                   message=message)