from sqlalchemy import distinct

from app.domain.data_scrape import DataScrapeJob, DataScrapeResult
from app.domain.sql_alchemy_models.data_scrape_model import DataScrapeJob as DataScrapeJobSql
from app.domain.sql_alchemy_models.data_scrape_model import DataScrapeJobUrl as DataScrapeJobUrlSql
from app.repositories.postgres_repository import postgres_base_repo

class DataScrapeRepository():

    async def create_data_scrape_job(self, job: DataScrapeJob):
        result = await DataScrapeJobSql.create(url=job.url, max_depth=job.max_depth, embeddings_type=job.embeddings_type,
                                         status="CREATED")
        return result

    async def create_data_scrape_job_url(self, job_url: DataScrapeResult, embeddings_type: str):
        result = await DataScrapeJobUrlSql.create(main_url=job_url.main_url, url=job_url.url,
                                         text=job_url.content, embeddings_type=embeddings_type)
        return result

    async def update_data_scrape_job(self, id, queue_size: int, sites_seen: int, status: str):
        job = await DataScrapeJobSql.get(id)
        if job:
            await job.update(queue_size=queue_size, sites_seen=sites_seen, status=status).apply()

    async def update_data_scrape_job_status(self, id, status: str):
        job = await DataScrapeJobSql.get(id)
        if job:
            await job.update(status=status).apply()

    async def get_data_scrape_job(self, id):
        return await DataScrapeJobSql.get(id)

    async def get_data_scrap_job(self, embeddings_type: str):
        jobs = await DataScrapeJobSql.query.where((DataScrapeJobSql.embeddings_type == embeddings_type)).gino.all()
        return jobs

    async def get_data_scrape_job_url(self, embeddings_type: str):
        urls = await (DataScrapeJobUrlSql.query
                      .where((DataScrapeJobUrlSql.embeddings_type == embeddings_type)).gino.all())
        return urls

    async def get_embedding_types(self):
        values = await postgres_base_repo.db.select([distinct(DataScrapeJobUrlSql.embeddings_type)]).gino.all()
        results = set()
        for value in values:
            results.add(value[0])
        return {'embedding_types': list(results)}