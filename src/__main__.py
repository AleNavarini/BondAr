from contextlib import asynccontextmanager
from fastapi import FastAPI
from cachetools import TTLCache
import schedule
import time
import threading
import uvicorn
import pandas as pd

from src.settings.settings import Settings
from src.google_client.google_client import GoogleClient

settings = Settings()

# Initialize cache with TTL from settings
cache = TTLCache(maxsize=1, ttl=settings.cache_update_interval)


def fetch_data():
    """
    Fetches data from Google Sheets and populates the cache.
    """
    client = GoogleClient(settings.google_sheets_api_key)
    data: pd.DataFrame = client.get_worksheet_data(
        sheet_url=settings.google_sheets_spreadsheet_url,
        worksheet_name=settings.google_sheets_worksheet_name,
    )
    data = client.normalize_data_columns(data)
    data["simbolo"] = data["simbolo"].str.replace("*", "").str.strip()
    data.to_csv("data.csv", index=False)

    map = {f"{row['simbolo']}": row for index, row in data.iterrows()}
    cache["data"] = map


def run_scheduler():
    """Run the scheduler in a background thread."""
    schedule.every(5).minutes.do(fetch_data)
    while True:
        schedule.run_pending()
        time.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    fetch_data()
    threading.Thread(target=run_scheduler, daemon=True).start()
    yield
    # Stop the scheduler when the app stops
    schedule.clear()


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "App is running", "status": "OK"}


@app.get("/bond/{symbol}")
async def bond(symbol: str):
    symbol = symbol.replace("*", "")
    if symbol in cache["data"]:
        return cache["data"][symbol]
    return {"message": "Symbol not found", "status": "ERROR"}


if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
