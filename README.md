# Bondar API

A FastAPI application that periodically fetches and caches data from Google Sheets.

## Features

- FastAPI web server
- Google Sheets integration
- Automatic cache updates every 5 minutes
- Health check endpoint
- Data retrieval endpoint

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up Google Sheets API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Sheets API
   - Create a service account and download the credentials JSON file
   - Place the credentials file in the project root as `credentials.json`

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the following variables in `.env`:
     - `GOOGLE_SHEETS_CREDENTIALS_PATH`: Path to your credentials file
     - `GOOGLE_SHEETS_SPREADSHEET_ID`: ID of your Google Spreadsheet
     - `GOOGLE_SHEETS_WORKSHEET_NAME`: Name of the worksheet to fetch data from
     - `CACHE_UPDATE_INTERVAL`: Cache update interval in seconds (default: 300)

4. Share your Google Sheet with the service account email address

## Running the Application

Start the server:
```bash
poetry run uvicorn src.bondar.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message
- `GET /data`: Get cached data from Google Sheets
- `GET /health`: Health check endpoint

## Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
