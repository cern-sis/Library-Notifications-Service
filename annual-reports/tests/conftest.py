import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_query_parameters": ["apikey"],
        "ignore_localhost": True,
        "decode_compressed_response": True,
        "record_mode": "once",
    }
