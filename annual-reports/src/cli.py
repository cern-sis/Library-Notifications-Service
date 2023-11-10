import click
from api import AnnualReportsAPI


@click.command()
@click.option("--years", "-y", multiple=True, default=[])
def fetch_annual_reports(years):
    annual_reports = AnnualReportsAPI(years=years)

    click.echo("Create tables if missing")
    annual_reports.create_tables()

    click.echo("Fetching subjects")
    annual_reports.get_subjects()

    click.echo("Fetching publications")
    annual_reports.get_publications()

    click.echo("Done")


if __name__ == "__main__":
    fetch_annual_reports()
