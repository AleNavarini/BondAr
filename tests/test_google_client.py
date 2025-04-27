from src.google_client.google_client import GoogleClient
import pandas as pd
from unittest.mock import patch, MagicMock

def test_google_client_initialization(mock_settings):
    client = GoogleClient(mock_settings.google_sheets_api_key)
    assert client is not None

@patch('gspread.authorize')
@patch('gspread.service_account')
def test_get_worksheet_data(mock_service_account, mock_authorize, mock_settings):
    # Setup mocks
    mock_worksheet = MagicMock()
    # Mock the get_all_records to return a simple dictionary
    mock_worksheet.get_all_records.return_value = [
        {
            "simbolo": "BONAR24",
            "precio": 100.5,
            "tasa": 0.05,
            "fecha_vencimiento": "2024-12-31"
        },
        {
            "simbolo": "BONAR25",
            "precio": 101.0,
            "tasa": 0.06,
            "fecha_vencimiento": "2025-12-31"
        }
    ]
    
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    
    mock_client = MagicMock()
    mock_client.open_by_url.return_value = mock_spreadsheet
    mock_service_account.return_value = mock_client
    mock_authorize.return_value = mock_client

    # Test with a valid API key
    with patch('gspread.api_key') as mock_api_key:
        mock_api_key.return_value = mock_client
        client = GoogleClient("valid_api_key")
        result = client.get_worksheet_data(
            sheet_url="https://docs.google.com/spreadsheets/d/1234567890abcdefghijklmnopqrstuvwxyz",
            worksheet_name="Test Sheet"
        )

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "simbolo" in result.columns
    assert "precio" in result.columns
    assert "tasa" in result.columns
    assert "fecha_vencimiento" in result.columns

def test_normalize_data_columns(mock_settings, sample_bond_data):
    client = GoogleClient(mock_settings.google_sheets_api_key)
    result = client.normalize_data_columns(sample_bond_data)
    
    assert isinstance(result, pd.DataFrame)
    assert "simbolo" in result.columns
    assert "precio" in result.columns
    assert "tasa" in result.columns
    assert "fecha_vencimiento" in result.columns 