from datetime import datetime, timedelta

import mock
import pytest
from api import MatomoAPI
from cli import fetch_matomo_inspire_data
from click.testing import CliRunner


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    filter_query_parameters=["token_auth", "idSite"],
)
def test_cli(db):
    runner = CliRunner()
    result = runner.invoke(fetch_matomo_inspire_data, ["--date", "2022-01-02"])
    assert result.exit_code == 0


@mock.patch.object(MatomoAPI, "fetch_inspire_statistics")
def test_cli_default_arguments(mocked_api, db):
    runner = CliRunner()
    result = runner.invoke(fetch_matomo_inspire_data, [])
    yesterday = datetime.now() - timedelta(days=1)

    assert result.exit_code == 0
    assert mocked_api.call_args[0][0].day == yesterday.day
    assert mocked_api.call_args[0][0].month == yesterday.month
    assert mocked_api.call_args[0][0].year == yesterday.year
