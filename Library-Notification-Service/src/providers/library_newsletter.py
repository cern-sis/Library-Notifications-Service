"""The command line module containing all the commands to filter documents."""

import logging
from typing import Tuple

import click

from ..api import (
    get_backoffice_latest_pids,
    get_results_from_pids,
    send_channel_request,
)
from ..utils import create_channel_message

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--subjects",
    type=click.STRING,
    multiple=True,
    required=True,
    help="Subjects domain. For eg. --subjects 005*:UDC --subjects 65*:",
)
@click.option(
    "--title",
    type=click.STRING,
    required=True,
    help="Subject title. For eg. --title 'Information Technology'",
)
@click.option(
    "--target",
    type=click.STRING,
    required=True,
    help="Egroup identifier. For eg. --target 'library-newsletter-notif-it'",
)
def cli(subjects: Tuple[str, ...], title: str, target: str) -> None:
    """A CLI command to send notifications for library updates.

    The created range is last 7 days from running the job.
    The published year is last 5 years from running the job.

    Supported Parameters: subjects, title and target group.
    python -m src.cli newsletter --subjects "005*:UDC" --subjects "65*:"
        --title 'Administration/Management'
        --target 'library-newsletter-notif-admin-management'
    """
    latest_pids = get_backoffice_latest_pids()
    if not latest_pids:
        click.echo("No updates in the backoffice!")
        return

    results, query = get_results_from_pids(latest_pids, list(subjects))
    if not results:
        click.echo(f"No results visible in the catalogue! {subjects}")
        return

    message = create_channel_message(results, title)
    click.echo(
        f"Subject: {subjects} -  Title: {title} - Results: {len(results)} results."
    )
    response = send_channel_request(message, target)
    if response.status_code == 200:
        click.echo("Notification sent successfully!")
    else:
        logger.error(
            f"Notification failed with status code: {response.status_code}:{response.text}"
        )
        click.echo(
            f"Notification failed with status code: {response.status_code}:{response.text}",
            err=True,
        )


if __name__ == "__main__":
    cli()
