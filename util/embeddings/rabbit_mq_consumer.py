import asyncio
from util.embeddings.embeddings_consumer import EmbeddingsRabbitMqConsumer
from repositories.postgres_repository import postgres_base_repo





async def main():
    await postgres_base_repo.connect()
    embeddings_consumer = EmbeddingsRabbitMqConsumer()
    await embeddings_consumer.consume_embeddings_messages()



# Run the event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()