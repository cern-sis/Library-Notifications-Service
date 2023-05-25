"""Module containing methods related to query generator."""


def get_or_join(queries):
    return " OR ".join(queries)


def get_and_join(queries):
    return " AND ".join(queries)


def get_full_query(pid, created, subject, pub_year):
    fields = []
    if pid and (pid_query := get_pid_query(pid)):
        fields.append(pid_query)

    if created and (created_query := get_range_query(created, "_created")):
        fields.append(created_query)

    if subject and (subject_query := get_subject_query(subject)):
        fields.append(subject_query)

    if pub_year and (pub_year_query := get_range_query(pub_year, "publication_year")):
        fields.append(pub_year_query)

    return get_and_join(fields)


def get_range_query(query_list, field, split_char=":"):
    query_strings = []
    for query in query_list:
        start, end = query.split(split_char)
        query_strings.append(f"{field}:[{start} TO {end}]")

    query = get_or_join(query_strings)
    return f"({query})"


def get_subject_query(subjects):
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


def get_pid_query(pid):
    pid_query = get_or_join([f"pid: {_pid}" for _pid in pid])
    return f"({pid_query})"
