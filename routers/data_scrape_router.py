
from fastapi import APIRouter

from domain.data_scrape import DataScrapeJob, DataScrapeResult
from services.data_scrape_service import DataScrapeService

data_scrapper_router = APIRouter()


@data_scrapper_router.post("/job/data_scrape")
def create_data_scrape_job(data_scrape_job: DataScrapeJob):
    base_url = data_scrape_job.url.split(".")[1]
    data_scrape_service = DataScrapeService(data_scrape_job.url, base_url, max_depth=data_scrape_job.max_depth)
    data_scrape_service.handle_data_scrape_job(data_scrape_job)

