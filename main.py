import uvicorn
from fastapi import FastAPI

from routers.open_api_router import open_ai_router
from routers.data_scrape_router import data_scrapper_router

app = FastAPI()

app.include_router(open_ai_router)
app.include_router(data_scrapper_router)

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8009)