import datetime
import os
import re

import backoff
import requests
import structlog
from models import Base, Categories, Journals, Publications
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# noqa: E501
PUBLICATIONS_PER_YEAR = "https://cds.cern.ch/search?p=(980:ARTICLE+or+980:BOOK+or+980:PROCEEDINGS+or+690:'YELLOW+REPORT'+or+980:REPORT)+and+year:{year}+and+(affiliation:CERN+or+260:CERN+or+595:'For+annual+report')+not+595:'Not+for+annual+report'&of=xm&rg=1"  # noqa: E501
JOURNALS_PER_YEAR = "https://cds.cern.ch/search?ln=en&cc=Published+Articles&p=(affiliation:CERN+or+595:'For+annual+report')+and+year:{year}+not+980:ConferencePaper+not+980:BookChapter+not+595:'Not+for+annual+report'&action_search=Search&op1=a&m1=a&p1=&f1=&c=Published+Articles&c=&sf=&so=d&rm=&rg=2000&sc=0&of=tb&ot=773__p"  # noqa: E501
PUBLISHED_ARTICLES_PER_YEAR = "https://cds.cern.ch/search?ln=en&cc=Published+Articles&p=%28affiliation%3ACERN+or+595%3A%27For+annual+report%27%29+and+year%3A{year}+not+980%3AConferencePaper+not+980%3ABookChapter+not+595%3A%27Not+for+annual+report%27&action_search=Search&op1=a&m1=a&p1=&f1=&c=Published+Articles&c=&sf=&so=d&rm=&rg=1&sc=0&of=xm"  # noqa: E501
CONTRIBUTIONS_TO_CONFERENCE_PROCEEDINGS_PER_YEAR = "https://cds.cern.ch/search?wl=0&ln=en&amp;cc=Published+Articles&amp;p=980%3AARTICLE+and+%28affiliation%3ACERN+or+595%3A%27For+annual+report%27%29+and+year%3A{year}+and+980%3AConferencePaper+not+595%3A%27Not+for+annual+report%27&amp;f=&amp;action_search=Search&amp;c=Published+Articles&amp;c=&amp;sf=author&amp;so=a&amp;rm=&amp;rg=1&amp;sc=1&amp;of=xm"  # noqa: E501
REPORTS_BOOKS_AND_BOOK_CHAPTERS_PER_YEAR = "https://cds.cern.ch/search?ln=en&p=affiliation%3ACERN+or+260%3ACERN+and+260%3A{year}++and+%28980%3ABOOK+or+980%3APROCEEDINGS+or+690%3A%27YELLOW+REPORT%27+or+980%3ABookChapter+or+980%3AREPORT%29+not+595%3A%27Not+for+annual+report%27&action_search=Search&op1=a&m1=a&p1=&f1=&c=Articles+%26+Preprints&c=Books+%26+Proceedings&amp;sf=&amp;so=d&amp;rm=&amp;rg=1&amp;sc=1&amp;of=xm"  # noqa: E501
THESES_PER_YEAR = "https://cds.cern.ch/search?wl=0&ln=en&amp;cc=CERN+Theses&amp;p=502%3A%27{year}%27+and+502%3Aphd&amp;f=&amp;action_search=Search&amp;c=CERN+Theses&amp;c=&amp;sf=&amp;so=d&amp;rm=&amp;rg=1&amp;sc=1&amp;of=xm"  # noqa: E501,E261
SUBJECT_CATEGORIES_PER_YEAR = "https://cds.cern.ch/search?ln=en&cc=Published+Articles&p=(affiliation:CERN+or+595:'For+annual+report')+and+year:{year}+not+980:ConferencePaper+not+980:BookChapter+not+595:'Not+for+annual+report'&action_search=Search&op1=a&m1=a&p1=&f1=&c=Published+Articles&c=&sf=&so=d&rm=&rg=2000&sc=0&of=tb&ot=65017"  # noqa: E501


LOGGING = structlog.get_logger("Annual_Report_API")


def _backoff_handler(details):
    LOGGING.info(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


def get_number_of_records(url):
    # Get the response from the URL
    response = requests.get(url)
    # Raise exception if HTTP error
    response.raise_for_status()
    match = re.search(r"Search-Engine-Total-Number-Of-Results: (\d+)", response.text)
    # Return the number of records
    if match:
        return int(match.group(1))
    return None


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    on_backoff=_backoff_handler,
)
def get_publications_per_year(year):
    """
    Get the number of publications for each publication type for a given year.

    Parameters
    ----------
    year : int
        The year to get the number of publications for.

    Returns
    -------
    dict
        The number of publications for each publication type for the given year.
    """
    publications_per_year = get_number_of_records(
        PUBLICATIONS_PER_YEAR.format(year=year)
    )
    published_articles_per_year = get_number_of_records(
        PUBLISHED_ARTICLES_PER_YEAR.format(year=year)
    )
    contributions_to_conference_proceedings_per_year = get_number_of_records(
        CONTRIBUTIONS_TO_CONFERENCE_PROCEEDINGS_PER_YEAR.format(year=year)
    )
    reports_books_and_book_chapters_per_year = get_number_of_records(
        REPORTS_BOOKS_AND_BOOK_CHAPTERS_PER_YEAR.format(year=year)
    )
    theses_per_year = get_number_of_records(THESES_PER_YEAR.format(year=year))

    return {
        "publications": publications_per_year,
        "published_articles": published_articles_per_year,
        "contributions_to_conference_proceedings": contributions_to_conference_proceedings_per_year,  # noqa: E501,E261
        "reports_books_and_book_chapters": reports_books_and_book_chapters_per_year,
        "theses": theses_per_year,
    }


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    on_backoff=_backoff_handler,
)
def get_journals_per_year(year):
    """
    Get the number of publications for each journal for a given year.

    Parameters
    ----------
    year : int
        The year to get the number of publications for.

    Returns
    -------
    dict
        The number of publications for each journal for the given year.
    """
    url = JOURNALS_PER_YEAR.format(year=year)

    response = requests.get(url)

    response.raise_for_status()
    journals = response.text.split("\n")

    journal_to_count = {}
    for journal in journals:
        journal_name = journal
        if journal_name in journal_to_count:
            journal_to_count[journal_name] += 1
        else:
            if journal_name:
                journal_to_count[journal_name] = 1
    return journal_to_count


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    on_backoff=_backoff_handler,
)
def get_subject_categories_per_year(year):
    """
    Get the number of publications for each subject category for a given year.

    Parameters
    ----------
    year : int
        The year to get the number of categories for.

    Returns
    -------
    dict
        The number of categories for the given year.
    """

    url = SUBJECT_CATEGORIES_PER_YEAR.format(year=year)

    response = requests.get(url)
    response.raise_for_status()

    categories = response.text.split("\n")

    categories_to_count = {}

    for category in categories:
        if "SzGeCERN" not in category:
            continue

        try:
            category_name = category.split("$$a")[1].split("$$")[0]
        except IndexError:
            # Skip this category since it's malformed
            continue

        if category_name in categories_to_count:
            categories_to_count[category_name] += 1
        else:
            categories_to_count[category_name] = 1

    return categories_to_count


class AnnualReportsAPI:
    def __init__(
        self,
        db_user: str = "",
        db_password: str = "",
        db_host: str = "",
        db_name: str = "",
        db_port: str = "",
        years: list = None,
    ) -> None:
        self.db_user = db_user or os.environ.get("DB_USER")
        self.db_password = db_password or os.environ.get("DB_PASSWORD")
        self.db_host = db_host or os.environ.get("DB_HOST")
        self.db_name = db_name or os.environ.get("MATOMO_DB_NAME")
        self.db_port = db_port or os.environ.get("DB_PORT")
        if not all(
            [
                self.db_user,
                self.db_password,
                self.db_host,
                self.db_name,
                self.db_port,
            ]
        ):
            raise ValueError("All the required attributes must be passed!")
        self.years = years
        if not self.years:
            current_year = datetime.datetime.now().year
            self.years = list(range(2004, current_year + 1))
        database_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"  # noqa: E501
        self.engine = create_engine(database_url)

    def create_tables(self):
        Base.metadata.create_all(self.engine, checkfirst=True)

    def get_categories(self):
        for year in self.years:
            year = int(year)
            LOGGING.info("Getting categories", year=year)
            results = get_subject_categories_per_year(year)
            year_to_date = datetime.date(year, 1, 1)
            with Session(self.engine) as session:
                try:
                    LOGGING.info("Deleting categories", year=year)
                    session.query(Categories).filter_by(year=year_to_date).delete()
                    records = [
                        Categories(year=year_to_date, category=key, count=value)
                        for key, value in results.items()
                    ]
                    LOGGING.info(
                        "Populate categories", count=len(records), categories=results
                    )
                    session.add_all(records)
                    session.commit()
                except Exception as e:
                    print("ERROR: " + str(e))
                    LOGGING.exception("Populate categories")
                else:
                    LOGGING.info("Populate categories success")

    def get_journals(self):
        for year in self.years:
            year = int(year)
            LOGGING.info("Getting journals", year=year)
            results = get_journals_per_year(year)
            year_to_date = datetime.date(year, 1, 1)
            with Session(self.engine) as session:
                try:
                    LOGGING.info("Deleting journals", year=year)
                    session.query(Journals).filter_by(year=year_to_date).delete()
                    records = [
                        Journals(year=year_to_date, journal=key, count=value)
                        for key, value in results.items()
                    ]
                    LOGGING.info(
                        "Populate journals", count=len(records), journals=results
                    )
                    session.add_all(records)
                    session.commit()
                except Exception as e:  # noqa: F841
                    LOGGING.exception("Populate journals")
                else:
                    LOGGING.info("Populate journals success")

    def get_publications(self):
        for year in self.years:
            year = int(year)
            LOGGING.info("Getting publications", year=year)
            results = get_publications_per_year(year)
            year_to_date = datetime.date(year, 1, 1)
            with Session(self.engine) as session:
                try:
                    LOGGING.info("Deleting publications", year=year)
                    session.query(Publications).filter_by(year=year_to_date).delete()
                    LOGGING.info("Populate publications", publications=results)
                    records = Publications(year=year_to_date, **results)
                    session.add(records)
                    session.commit()
                except Exception as e:
                    print("ERROR: " + str(e))
                    LOGGING.exception("Populate publications")
                else:
                    LOGGING.info("Populate publications success")
