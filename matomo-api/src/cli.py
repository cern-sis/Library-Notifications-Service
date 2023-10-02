from datetime import date, datetime

import click
from api import MatomoAPI


@click.command()
@click.option("--date", "-d", default=date.today())
def fetch_matomo_inspire_data(date: str):
    if isinstance(date, str):
        try:
            date_datetime = datetime.strptime(date, "%Y-%M-%d")
        except ValueError:
            click.echo("Wrong date format! Aborting.")

    matomo = MatomoAPI()
    matomo.fetch_inspire_statistics(date_datetime)


if __name__ == "__main__":
    fetch_matomo_inspire_data()
