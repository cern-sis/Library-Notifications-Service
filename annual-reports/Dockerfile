FROM python:3.11

WORKDIR /annual-reports

ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONBUFFERED=0 \
  POETRY_VIRTUALENVS_CREATE=false


ARG POETRY_VERSION
ENV POETRY_VERSION="${POETRY_VERSION:-1.6.1}"
RUN curl -sSL https://install.python-poetry.org \
  | python3 - --git https://github.com/python-poetry/poetry.git#{$POETRY_VERSION} \
  && poetry --version


COPY poetry.lock pyproject.toml ./
COPY src ./src

RUN poetry install
CMD poetry run python src/cli.py
