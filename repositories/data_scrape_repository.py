from domain.data_scrape import DataScrapeJob
from domain.sql_alchemy_models.data_scrape_model import DataScrapeJob as DataScrapeJobSql


class DataScrapeRepository():

    async def create_data_scrape_job(self, job: DataScrapeJob):
        result = await DataScrapeJobSql.create(url=job.url, max_depth=job.max_depth, embeddings_type=job.embeddings_type,
                                         status="CREATED")
        return result

    async def update_data_scrape_job(self, id, queue_size: int, sites_seen: int, status: str):
        job = await DataScrapeJobSql.get(id)
        if job:
            await job.update(queue_size=queue_size, sites_seen=sites_seen, status=status).apply()

    async def update_data_scrape_job_status(self, id, status: str):
        job = await DataScrapeJobSql.get(id)
        if job:
            await job.update(status=status).apply()