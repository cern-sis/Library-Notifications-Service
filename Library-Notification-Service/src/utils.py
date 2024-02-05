"""Module containing methods related to query generator."""

import urllib.parse
from datetime import datetime, timedelta
from typing import List, Optional

from .env import LIBRARY_CATALOGUE_SITE_URL


def get_full_query(
    pid: Optional[List[str]] = None,
    created: Optional[List[str]] = None,
    subject: Optional[List[str]] = None,
    pub_year: Optional[List[str]] = None,
    restricted: bool = True,
) -> str:
    fields = []

    if pub_year and (pub_year_query := get_range_query(pub_year, "publication_year")):
        fields.append(pub_year_query)

    if created and (created_query := get_range_query(created, "_created")):
        fields.append(created_query)

    if pid and (pid_query := get_pid_query(pid)):
        fields.append(pid_query)

    if subject and (subject_query := get_subject_query(subject)):
        fields.append(subject_query)

    # Show only non restricted results
    if restricted is False:
        fields.append("NOT restricted: true")

    return get_and_join(fields)


def get_or_join(queries: List[str]) -> str:
    return " OR ".join(queries)


def get_and_join(queries: List[str]) -> str:
    return " AND ".join(queries)


def get_last_week_date_range() -> List[str]:
    today = datetime.today().date()
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = last_week_start + timedelta(days=6)
    date_range = f"[{last_week_start.isoformat()}:{last_week_end.isoformat()}]"
    return [date_range]


def get_last_five_years_range() -> List[str]:
    current_year = datetime.today().year
    last_five_years_start = current_year - 4
    last_five_years_end = current_year
    year_range = f"[{last_five_years_start}:{last_five_years_end}]"
    return [year_range]


def get_range_query(query_list: List[str], field: str, split_char: str = ":") -> str:
    query_strings = []
    for query in query_list:
        start, end = query.split(split_char)
        query_strings.append(f"{field}:{start} TO {end}")

    query = get_or_join(query_strings)
    return f"({query})"


def get_subject_query(subjects: List[str]) -> str:
    subject_queries = []

    for subject in subjects:
        subject_value, subject_scheme = subject.split(":")
        if subject_scheme:
            subject_queries.append(
                f"(subjects.value:{subject_value} AND subject.scheme:{subject_scheme})"
            )
        else:
            subject_queries.append(f"subjects.value:{subject_value}")

    subject_query = get_or_join(subject_queries)
    return f"({subject_query})"


def get_pid_query(pid: List[str]) -> str:
    pid_query = get_or_join([f"pid: {_pid}" for _pid in pid])
    return f"({pid_query})"


def get_pids_from_docs(docs: List[dict]) -> List[str]:
    pids = []
    for doc in docs:
        metadata = doc.get("metadata")
        if metadata and "document_pid" in metadata:
            pids.append(metadata["document_pid"])
    return pids


def create_channel_message(message: List[dict], title: str, url: str) -> str:
    html_string = f"<h1>Latest books/e-books for {title}</h1>\n<ul>\n"
    for doc in message:
        doc_id = doc.get("id", "")
        if doc_id:
            doc_query = urllib.parse.quote(f"pid: {doc_id}")  # exact match
            doc_url = f"{LIBRARY_CATALOGUE_SITE_URL}{doc_query}"
            doc_title = doc.get("metadata", {}).get("title", "")
            html_string += f"<li><a href='{doc_url}'>{doc_title}</a></li>\n"
    html_string += "</ul>"
    html_string += f"<p><a href='{url}'>View all</a></p>"

    return html_string
