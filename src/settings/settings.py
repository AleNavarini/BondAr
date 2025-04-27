from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_sheets_api_key: str
    google_sheets_spreadsheet_url: str
    google_sheets_worksheet_name: str
    cache_update_interval: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
