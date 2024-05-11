import uvicorn
from fastapi import FastAPI

from routers.open_api_router import open_ai_router
from routers.data_scrape_router import data_scrapper_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)