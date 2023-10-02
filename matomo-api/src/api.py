import os
from datetime import date

import requests
from models import MatomoData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MatomoAPI:
    def __init__(
        self,
        base_url: str = None,
        auth_token: str = None,
        site_id: int = None,
        db_user: str = None,
        db_password: str = None,
        db_host: str = None,
        db_name: str = None,
    ) -> None:
        self.base_url = base_url or os.environ.get("MATOMO_BASE_URL")
        self.auth_token = auth_token or os.environ.get("MATOMO_AUTH_TOKEN")
        self.site_id = site_id or os.environ.get("MATOMO_SITE_ID")
        self.db_user = db_user or os.environ.get("DB_USER")
        self.db_password = db_password or os.environ.get("DB_PASSWORD")
        self.db_host = db_host or os.environ.get("DB_HOST")
        self.db_name = db_name or os.environ.get("DB_NAME")
        if not all(
            [
                self.base_url,
                self.auth_token,
                self.site_id,
                self.db_user,
                self.db_password,
                self.db_host,
                self.db_name,
            ]
        ):
            raise ValueError("All the required attributes must be passed!")

    def create_session(self):
        database_url = f"postgresql://{self.db_name}:{self.db_password}@{self.db_host}:5432/{self.db_name}"  # noqa: E501
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    @property
    def endpoint_map(self):
        return {
            "visits_per_day": "VisitsSummary.getVisits",
            "unique_visitors": "VisitsSummary.getUniqueVisitors",
        }

    def _get_request_params(self, date, period):
        params = {
            "module": "API",
            "token_auth": self.auth_token,
            "idSite": self.site_id,
            "date": str(date),
            "period": period,
        }
        return params

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        url = f"{self.base_url}/index.php"
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
        }
        params = params or {}
        params.update({"module": "API", "format": "json", "method": endpoint})

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_visits_per_day(self, date: date, period="day") -> dict:
        endpoint = self.endpoint_map["visits_per_day"]
        params = self._get_request_params(date, period)
        response = self._make_request(endpoint, params)
        return response["value"]

    def get_unique_visitors(self, date: date, period="day") -> dict:
        endpoint = self.endpoint_map["visits_per_day"]
        params = self._get_request_params(date, period)
        response = self._make_request(endpoint, params)
        return response["value"]

    def fetch_inspire_statistics(self, date: date) -> None:
        visits_per_day = self.get_visits_per_day(date)
        unique_visitors = self.get_unique_visitors(date)

        session = self.create_session()
        data_entry = MatomoData(
            date=date, visits=visits_per_day, unique_visitors=unique_visitors
        )

        session.add(data_entry)
        session.commit()
        session.close()
