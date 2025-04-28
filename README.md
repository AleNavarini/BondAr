# BondAr

A FastAPI-based service that provides bond data with up to 5 minutes of delay from Google Sheets with caching capabilities.

## Overview

BondAr is a Python service that:
- Fetches bond data from a Google Sheets spreadsheet
- Caches the data with a 5-minute TTL (Time To Live)
- Provides a REST API to query bond information
- Automatically updates the data every 5 minutes

## Features

- Bond data access with up to 5 minutes of delay
- Automatic data refresh every 5 minutes
- Efficient caching system
- RESTful API endpoints
- Google Sheets integration
- FastAPI-based web service

## Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Google Sheets API credentials

## Installation

1. Clone the repository using either HTTPS or SSH:

```bash
# Using HTTPS
git clone https://github.com/AleNavarini/BondAr
cd bondar

# Or using SSH
git clone git@github.com:AleNavarini/BondAr.git
cd bondar
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file with the following variables:
```
GOOGLE_SHEETS_API_KEY=your_api_key
GOOGLE_SHEETS_SPREADSHEET_URL=your_spreadsheet_url
GOOGLE_SHEETS_WORKSHEET_NAME=your_worksheet_name
```

## Usage

1. Start the service:
```bash
poetry run python -m src
```

2. The service will be available at `http://localhost:8000`

### API Endpoints

- `GET /`: Health check endpoint
  - Returns: `{"message": "App is running", "status": "OK"}`

- `GET /bond/{symbol}`: Get bond information
  - Parameters:
    - `symbol`: The bond symbol to query
  - Returns: Bond data if found, error message if not found

## Project Structure

```
BondAr/
├── src/
│   ├── __main__.py          # Main application entry point
│   ├── settings/            # Configuration settings
│   └── google_client/       # Google Sheets client implementation
├── tests/                   # Test files
├── pyproject.toml           # Project configuration
└── poetry.lock             # Dependency lock file
```

## Dependencies

- FastAPI: Web framework
- schedule: Task scheduling
- cachetools: Caching implementation
- google-auth & gspread: Google Sheets integration
- pandas: Data manipulation
- pydantic-settings: Settings management


## Author

Alejandro - alejandro.navarini@gmail.com


## Deployment

Try this at https://bondar.onrender.com/
