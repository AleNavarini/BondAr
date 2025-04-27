import gspread
import pandas as pd
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound
import unicodedata


class GoogleClient:
    """A minimal class to fetch Google Sheets data using an API key."""

    def __init__(self, api_key: str):
        """Initialize with API key and set up gspread client."""
        try:
            # Authenticate using the API key
            self.client = gspread.api_key(api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize gspread client with API key: {e}")

    def get_worksheet_data(self, sheet_url: str, worksheet_name: str) -> pd.DataFrame:
        """Fetch data from a worksheet by name and return as pandas DataFrame."""
        try:
            # Open the spreadsheet by URL
            sheet = self.client.open_by_url(sheet_url)
            # Access the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Fetch all records and convert to DataFrame
            records = worksheet.get_all_records()
            return pd.DataFrame(records)
        except SpreadsheetNotFound:
            raise ValueError(
                "Spreadsheet not found or not accessible. Ensure it is public and the URL is correct."
            )
        except WorksheetNotFound:
            raise ValueError(
                f"Worksheet '{worksheet_name}' not found in the spreadsheet."
            )
        except APIError as e:
            raise ValueError(f"API error occurred: {e}")
        except Exception as e:
            raise ValueError(f"Failed to fetch worksheet data: {e}")

    def normalize_data_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names in the DataFrame by removing diacritics, converting to lowercase,
        replacing spaces and newlines with underscores, and removing backticks."""

        # Function to normalize text by removing diacritics (tildes)
        def normalize_text(text):
            # Decompose accented characters into base character + combining mark
            normalized = unicodedata.normalize("NFD", text)
            # Keep only non-combining characters (remove diacritics)
            return "".join(c for c in normalized if unicodedata.category(c) != "Mn")

        # Normalize column names: remove diacritics, convert to lowercase,
        # replace spaces and newlines with underscores, and remove backticks
        data.columns = [
            normalize_text(col)
            .lower()
            .replace(" ", "_")
            .replace("\n", "_")
            .replace("`", "")
            for col in data.columns
        ]
        return data
