import ast

from app.domain.open_ai import Embedding
from app.repositories.data_scrape_repository import DataScrapeRepository
from app.services.open_ai_service import OpenAiService
from app.util.base_consumer import RabbitMqConsumer
from app.domain.rabbit_mq_routing_keys import RabbitmqRoutingKeys

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
            if fcn:
                await fcn(message.body.decode())
            else:
                print("no fcn to run")

    def get_action(self, routing_key):
        print(f'getting action for {routing_key}')
        commands_to_actions = {
            f"cmd.{RabbitmqRoutingKeys.CREATE_EMBEDDINGS.name}": self.handle_embeddings_message
        }
        print(f"keys available: {commands_to_actions.keys()}")
        action = commands_to_actions.get(routing_key, None)
        return action


    async def handle_embeddings_message(self, body):
        body = ast.literal_eval(body)
        print(f"run the job")
        embeddings_type = body['embeddings_type']
        create_embeddings = bool(body['create_embeddings'])
        repo = DataScrapeRepository()
        open_ai_service = OpenAiService()
        documents = await repo.get_data_scrape_job_url(embeddings_type)
        print(f"processing {len(documents)} documents")
        count = 0
        for document in documents:
            print(count)
            try:
                result = open_ai_service.get_embedding_by_url(document.url)
                if len(result) == 0:
                    embedding = Embedding(embeddings_type=embeddings_type,
                                          text=document.text, url=document.url)
                    embedding = open_ai_service.generate_embeddings_from_openai(embedding, create_embeddings)
                    open_ai_service.create_embedding(embedding, create_embeddings)
                else:
                    print(f"Existing vectors found for url: {document.url} total: {len(result)}")
                    embedding = Embedding(embeddings_type=embeddings_type,
                                          text=document.text, url=document.url,
                                          vector=result[0]["vector"])
                    open_ai_service.create_embedding(embedding, create_embeddings)
                count += 1
            except Exception as e:
                count += 1
                print("Broke on document")
                print(e)