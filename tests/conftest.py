import pytest
from fastapi.testclient import TestClient
from src.__main__ import app, cache
from src.settings.settings import Settings
import pandas as pd
from unittest.mock import patch

@pytest.fixture(autouse=True)
def setup_cache():
    # Clear cache before each test
    cache.clear()
    yield
    # Clear cache after each test
    cache.clear()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_settings():
    settings = Settings(
        google_sheets_api_key="test_key",
        google_sheets_spreadsheet_url="test_url",
        google_sheets_worksheet_name="test_sheet",
        cache_update_interval=1  # 1 second TTL for testing
    )
    return settings

@pytest.fixture
def sample_bond_data():
    return pd.DataFrame({
        "simbolo": ["BONAR24", "BONAR25"],
        "precio": [100.5, 101.2],
        "tasa": [0.05, 0.06],
        "fecha_vencimiento": ["2024-12-31", "2025-12-31"]
    })

@pytest.fixture
def mock_google_client(mock_settings, sample_bond_data):
    with patch('src.google_client.google_client.GoogleClient') as mock:
        instance = mock.return_value
        instance.get_worksheet_data.return_value = sample_bond_data
        instance.normalize_data_columns.return_value = sample_bond_data
        
        # Initialize cache with sample data
        data_map = {f"{row['simbolo']}": row for _, row in sample_bond_data.iterrows()}
        cache["data"] = data_map
        
        yield instance 