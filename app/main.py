import uvicorn
from fastapi import FastAPI

from app.repositories.postgres_repository import postgres_base_repo
from app.routers.open_api_router import open_ai_router
from app.routers.data_scrape_router import data_scrapper_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
postgres_base_repo.db.init_app(app)


app.include_router(open_ai_router)
app.include_router(data_scrapper_router)

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    print("WEEE")
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
