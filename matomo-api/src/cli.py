from datetime import date, datetime

import click
from api import MatomoAPI


@click.command()
@click.option("--date", "-d", default=date.today())
def fetch_matomo_inspire_data(date: str):
    click.echo(f"Fetching data for date {date}")
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%M-%d")
        except ValueError:
            click.echo("Wrong date format! Aborting.")
            return

    matomo = MatomoAPI()
    matomo.fetch_inspire_statistics(date)


if __name__ == "__main__":
    fetch_matomo_inspire_data()
