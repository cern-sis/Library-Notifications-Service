from datetime import datetime

import pytest
from api import MatomoAPI

matomo_api = MatomoAPI(
    base_url="https://webanalytics.web.cern.ch",
    auth_token="change-me",
    site_id=1,
    db_host="127.0.0.1",
    db_name="matomo",
    db_password="matomo",
    db_user="matomo",
)

TEST_DAY = day = datetime.strptime("2023-10-02", "%Y-%m-%d")


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    filter_query_parameters=["token_auth", "idSite"],
)
def test_matomo_api_get_unique_visitors():
    visitors = matomo_api.get_unique_visitors(date=TEST_DAY)
    assert visitors > 0


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    filter_query_parameters=["token_auth", "idSite"],
)
def test_matomo_api_get_visits_per_day():
    visitors = matomo_api.get_visits_per_day(date=TEST_DAY)
    assert visitors > 0


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    filter_query_parameters=["token_auth", "idSite"],
)
def test_matomo_fetch_inspire_statistics(db):
    _, db_cursor = db
    matomo_api.fetch_inspire_statistics(date=TEST_DAY)

    db_cursor.execute("select * from inspire_matomo_data")
    results = db_cursor.fetchall()
    assert len(results) == 1
