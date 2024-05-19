import ast

from domain.data_scrape import DataScrapeJob
from services.data_scrape_service import DataScrapeService
from util.base_consumer import RabbitMqConsumer
from domain.rabbit_mq_routing_keys import RabbitmqRoutingKeys


class DataScrapeRabbitMqConsumer(RabbitMqConsumer):


    async def consume_data_scrape_messages(self):
        await self.async_init(exchange_name="data_scrape_exchange",
                           routing_key=f"cmd.*",
                           queue_name="data_scrape_queue",
                           callback=self.handle_messages)

    async def handle_messages(self, message):
        async with message.process():
            print(f"handling message {message.body.decode()}")
            full_routing_key = message.routing_key
            fcn = self.get_action(full_routing_key)
            print("sending body to handler")
            await fcn(message.body.decode())

    def get_action(self, routing_key):
        print(f'getting action for {routing_key}')
        commands_to_actions = {
            f"cmd.{RabbitmqRoutingKeys.CREATE_DATA_SCRAPE.name}": self.handle_patient_registration_message
        }
        return commands_to_actions[routing_key]

    async def handle_patient_registration_message(self, body):
        body = ast.literal_eval(body)
        print(f"run the job")
        date_scrape_job_dict = body['data_scrape_job']
        create_embeddings = bool(body['create_embeddings'])
        job = DataScrapeJob.parse_obj(date_scrape_job_dict)
        base_url = job.url.split(".")[1]
        data_scrape_service = DataScrapeService(job.url, base_url, max_depth=job.max_depth)
        await data_scrape_service.handle_data_scrape_job(job, create_embeddings)
