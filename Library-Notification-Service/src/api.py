"""Module interacting with library catalogue api"""


import json
import urllib.parse
from typing import List

import requests

from .env import (
    LIBRARY_CATALOGUE_BACKOFFICE_API_TOKEN,
    LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API,
    LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API,
    LIBRARY_CATALOGUE_SITE_API,
    NOTIFICATIONS_API_SECRET,
    NOTIFICATIONS_API_URL,
    NOTIFICATIONS_CHANNEL_ID,
)
from .utils import (
    get_full_query,
    get_last_five_years_range,
    get_last_week_date_range,
    get_pids_from_docs,
)


def get_library_catalogue_backoffice_urls() -> List[str]:
    return [
        LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API,
        LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API,
    ]


def get_backoffice_latest_pids() -> List[str]:
    created = get_last_week_date_range()
    query = get_full_query(created=created, restricted=False)
    query_encoded = urllib.parse.quote(query)

    pids = []
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LIBRARY_CATALOGUE_BACKOFFICE_API_TOKEN}",
    }
    for url in get_library_catalogue_backoffice_urls():
        next_url = f"{url}{query_encoded}"
        while next_url:
            response = requests.get(next_url, headers=headers)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise Exception(f"Request failed with status code: {e}")

            json_response = response.json()
            hits = json_response.get("hits", {}).get("hits", [])
            pids.extend(get_pids_from_docs(hits))
            next_url = json_response.get("links", {}).get("next", None)

    return pids


def get_api_url(query: str) -> str:
    query_encoded = urllib.parse.quote(query)
    return f"{LIBRARY_CATALOGUE_SITE_API}{query_encoded}"


def get_results_from_pids(pids: List[str], subjects: List[str]) -> List[dict]:
    published = get_last_five_years_range()
    results = []

    # divide pids into chunks of 40 to reduce query size
    for i in range(0, len(pids), 40):
        chunked_pids = pids[i : i + 40]
        if not chunked_pids:
            continue
        catalogue_site_query = get_full_query(
            pid=chunked_pids, pub_year=published, subject=subjects
        )
        result = get_site_api_docs(catalogue_site_query)
        results.extend(result)

    return results, catalogue_site_query


def get_site_api_docs(query: str) -> List[dict]:
    url = get_api_url(query)
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Request failed with status code: {e}")

    hits, count = response.json().get("hits", {}).values()
    if count == 0:
        return []

    return hits


def send_channel_request(data: str, target: str) -> int:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTIFICATIONS_API_SECRET}",
    }
    request_data = {
        "target": NOTIFICATIONS_CHANNEL_ID,
        "summary": "Library Updates",
        "priority": "NORMAL",
        "body": data,
        "targetGroups": [{"groupIdentifier": f"{target}"}],
    }

    response = requests.post(
        NOTIFICATIONS_API_URL, headers=headers, data=json.dumps(request_data)
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Request failed with status code: {e}")

    return response.status_code
