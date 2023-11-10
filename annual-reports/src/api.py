import datetime
import os
import xml.etree.ElementTree as ET

import backoff
import requests
import structlog
from models import Base, Categories, Journals, Publications
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

PUBLICATIONS = "https://cds.cern.ch/tools/custom_query_summary.py?start={year}&end={year}&apikey={cds_token}&refresh=1&repeated_values=0"
SUBJECTS = PUBLICATIONS + "&otag=65017a"

LOGGING = structlog.get_logger("Annual_Report_API")


def _backoff_handler(details):
    LOGGING.info(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


class AnnualReportsAPI:
    def __init__(
        self,
        db_user: str = "",
        db_password: str = "",
        db_host: str = "",
        db_name: str = "",
        db_port: str = "",
        years: list = None,
        cds_token: str = "",
    ) -> None:
        self.db_user = db_user or os.environ.get("DB_USER")
        self.db_password = db_password or os.environ.get("DB_PASSWORD")
        self.db_host = db_host or os.environ.get("DB_HOST")
        self.db_name = db_name or os.environ.get("MATOMO_DB_NAME")
        self.db_port = db_port or os.environ.get("DB_PORT")
        self.cds_token = cds_token or os.environ.get("CDS_TOKEN")
        if not all(
            [
                self.db_user,
                self.db_password,
                self.db_host,
                self.db_name,
                self.db_port,
                self.cds_token,
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

    def drop_tables(self):
        Base.metadata.drop_all(self.engine, checkfirst=True)

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_tries=5,
        on_backoff=_backoff_handler,
    )
    def request_publications_from_cds(self, year):
        url = PUBLICATIONS.format(year=year, cds_token=self.cds_token)
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        return root

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_tries=5,
        on_backoff=_backoff_handler,
    )
    def request_subjects_from_cds(self, year):
        url = SUBJECTS.format(year=year, cds_token=self.cds_token)
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        return root

    def get_publications_by_year(self, year):
        """
        Get the number of publications for a given year.

        Parameters
        ----------
        year : int
            The year to get the number of publications for.

        Returns
        -------
        int
            The number of publications for the given year.
        """
        root = self.request_publications_from_cds(year)
        yearly_report = root.find("yearly_report")
        publication_report_count = yearly_report.attrib
        del publication_report_count["year"]
        journals = {}
        for journal in yearly_report.findall("line"):
            name = journal.find("result").text
            if "TOTAL" in name:
                continue
            journals[name] = journal.find("nb").text
        return publication_report_count, journals

    def get_subjects_by_year(self, year):
        root = self.request_subjects_from_cds(year)
        yearly_report = root.find("yearly_report")
        subjects = {}
        for subject in yearly_report.findall("line"):
            name = subject.find("result").text
            if "TOTAL" in name:
                continue
            subjects[name] = subject.find("nb").text
        return subjects

    def get_subjects(self):
        for year in self.years:
            year = int(year)
            LOGGING.info("Getting categories", year=year)
            results = self.get_subjects_by_year(year)
            year_to_date = datetime.date(year, 1, 1)
            with Session(self.engine) as session:
                try:
                    LOGGING.info("Deleting categories", year=year)
                    session.query(Categories).filter_by(year=year_to_date).delete()
                    records = [
                        Categories(year=year_to_date, category=key, count=int(value))
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

    def get_publications(self):
        for year in self.years:
            year = int(year)
            LOGGING.info("Getting publications", year=year)
            publications, journals = self.get_publications_by_year(year)
            year_to_date = datetime.date(year, 1, 1)
            with Session(self.engine) as session:
                try:
                    LOGGING.info("Deleting publications", year=year)
                    session.query(Publications).filter_by(year=year_to_date).delete()
                    LOGGING.info("Populate publications", publications=publications)
                    records = Publications(year=year_to_date, **publications)
                    session.add(records)
                    session.commit()
                except Exception as e:
                    print("ERROR: " + str(e))
                    LOGGING.exception("Populate publications")
                else:
                    LOGGING.info("Populate publications success")
            with Session(self.engine) as session:
                try:
                    LOGGING.info("Deleting journals", year=year)
                    session.query(Journals).filter_by(year=year_to_date).delete()
                    records = [
                        Journals(year=year_to_date, journal=key, count=int(value))
                        for key, value in journals.items()
                    ]
                    LOGGING.info(
                        "Populate journals", count=len(records), journals=journals
                    )
                    session.add_all(records)
                    session.commit()
                except Exception as e:  # noqa: F841
                    LOGGING.exception("Populate journals")
                else:
                    LOGGING.info("Populate journals success")
