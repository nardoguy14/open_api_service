
from fastapi import APIRouter, Query

from domain.data_scrape import DataScrapeJob
from services.open_ai_service import OpenAiService
from repositories.data_scrape_repository import DataScrapeRepository
from util.data_scrape.data_scrape_producer import DataScrapeProducer

data_scrapper_router = APIRouter()
data_scrape_service = DataScrapeRepository()
open_ai_service = OpenAiService()

@data_scrapper_router.post("/job/data_scrape")
def create_data_scrape_job(data_scrape_job: DataScrapeJob, create_embeddings: bool = Query(False)):
    producer = DataScrapeProducer()
    producer.send_new_data_scrape_job({
        'data_scrape_job': data_scrape_job.__dict__,
        'create_embeddings': create_embeddings
    })


@data_scrapper_router.get("/job/data_scrape/{id}")
async def get_data_scrape_job_by_id(id: int):
    return await data_scrape_service.get_data_scrape_job(id)


@data_scrapper_router.get("/job/data_scrape")
async def get_data_scrap_job(embeddings_type: str = Query(None)):
    return await data_scrape_service.get_data_scrap_job(embeddings_type)

@data_scrapper_router.get("/data_scrape/urls")
async def get_data_scrape_job_urls(embeddings_type: str = Query(None)):
    return await data_scrape_service.get_data_scrape_job_url(embeddings_type)

@data_scrapper_router.get("/data_scrape/token-count")
async def get_data_scrape_token_count(embeddings_type: str = Query(None)):
    urls = await data_scrape_service.get_data_scrape_job_url(embeddings_type)
    content = ""
    individual_token_counts = []
    for url in urls:
        content += "\n \n" + url.text
        individual_token_counts.append(open_ai_service.get_num_of_tokens(url.text, open_ai_service.EMBEDDING_MODEL))
    token_count = open_ai_service.get_num_of_tokens(content, open_ai_service.EMBEDDING_MODEL)
    return {
        "token_count": token_count,
        "cost_to_generate_embeddings": token_count * open_ai_service.EMBEDDING_MODEL_COST,
        "unit_of_cost": "cents",
        "individual_token_counts": individual_token_counts
    }
