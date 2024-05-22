import ast

from domain.data_scrape import DataScrapeJob
from domain.open_ai import Embedding
from repositories.data_scrape_repository import DataScrapeRepository
from services.open_ai_service import OpenAiService
from util.base_consumer import RabbitMqConsumer
from domain.rabbit_mq_routing_keys import RabbitmqRoutingKeys

class EmbeddingsRabbitMqConsumer(RabbitMqConsumer):


    async def consume_embeddings_messages(self):
        await self.async_init(exchange_name="data_scrape_exchange",
                           routing_key=f"cmd.*",
                           queue_name="embeddings_queue",
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
            f"cmd.{RabbitmqRoutingKeys.CREATE_EMBEDDINGS.name}": self.handle_embeddings_message
        }
        return commands_to_actions[routing_key]

    async def handle_embeddings_message(self, body):
        body = ast.literal_eval(body)
        print(f"run the job")
        embeddings_type = body['embeddings_type']
        create_embeddings = bool(body['create_embeddings'])
        repo = DataScrapeRepository()
        open_ai_service = OpenAiService()
        documents = await repo.get_data_scrape_job_url(embeddings_type)
        for document in documents:
            try:
                result = open_ai_service.get_embedding_by_url(document.url)
                print(f"Existing vectors found for url: {document.url} total: {len(result)}")
                if len(result) == 0:
                    embedding = Embedding(embeddings_type=embeddings_type,
                                          text=document.text, url=document.url)
                    open_ai_service.create_embedding(embedding, create_embeddings)
            except Exception as e:
                print("Broke on document")
                print(e)