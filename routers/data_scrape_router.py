
from fastapi import APIRouter, Query

from domain.data_scrape import DataScrapeJob
from repositories.data_scrape_repository import DataScrapeRepository
from util.data_scrape_producer import DataScrapeProducer

data_scrapper_router = APIRouter()


@data_scrapper_router.post("/job/data_scrape")
def create_data_scrape_job(data_scrape_job: DataScrapeJob, create_embeddings: bool = Query(False)):
    producer = DataScrapeProducer()
    producer.send_new_data_scrape_job({
        'data_scrape_job': data_scrape_job.__dict__,
        'create_embeddings': create_embeddings
    })


@data_scrapper_router.get("/job/data_scrape/{id}")
async def get_data_scrape_job_by_id(id: int):
    data_scrape_service = DataScrapeRepository()
    return await data_scrape_service.get_data_scrape_job(id)


@data_scrapper_router.get("/job/data_scrape")
async def get_data_scrap_job(data_scrape_job: DataScrapeJob):
    data_scrape_service = DataScrapeRepository()
    return await data_scrape_service.get_data_scrap_job(data_scrape_job)
