from src.__main__ import cache, fetch_data
from unittest.mock import patch

def test_cache_initialization():
    assert cache.maxsize == 1
    assert cache.ttl == 300  # 5 minutes in seconds

@patch('src.__main__.GoogleClient')
def test_fetch_data_updates_cache(mock_google_client, mock_settings, sample_bond_data):
    # Setup mock
    mock_client = mock_google_client.return_value
    mock_client.get_worksheet_data.return_value = sample_bond_data
    mock_client.normalize_data_columns.return_value = sample_bond_data

    # Clear cache and test
    cache.clear()
    fetch_data()

    # Assert cache is populated
    assert "data" in cache
    assert isinstance(cache["data"], dict)
    assert "BONAR24" in cache["data"]
    assert "BONAR25" in cache["data"]

