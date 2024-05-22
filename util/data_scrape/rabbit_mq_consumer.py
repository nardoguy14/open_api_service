import asyncio
from util.data_scrape.data_scrape_consumer import DataScrapeRabbitMqConsumer
from repositories.postgres_repository import postgres_base_repo





async def main():
    await postgres_base_repo.connect()
    patients_consumer = DataScrapeRabbitMqConsumer()
    await patients_consumer.consume_data_scrape_messages()



# Run the event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()