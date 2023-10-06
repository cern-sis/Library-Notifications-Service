from datetime import datetime, timedelta

import click
from api import MatomoAPI


def _get_yesterday_date_string():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    return formatted_yesterday


@click.command()
@click.option("--date", "-d", default=_get_yesterday_date_string())
def fetch_matomo_inspire_data(date: str):
    click.echo(f"Fetching data for date {date}")
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            click.echo("Wrong date format! Aborting.")
            return

    matomo = MatomoAPI()
    matomo.fetch_inspire_statistics(date)


if __name__ == "__main__":
    fetch_matomo_inspire_data()
