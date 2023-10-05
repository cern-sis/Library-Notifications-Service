import pytest
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


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    filter_query_parameters=["token_auth", "idSite"],
)
def test_cli_default_arguments(db):
    runner = CliRunner()
    result = runner.invoke(fetch_matomo_inspire_data, [])
    assert result.exit_code == 0