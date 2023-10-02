FROM python:3.11-slim

# Install Poetry
RUN pip install --no-cache-dir poetry

COPY . /code
WORKDIR /code

# Set environment variable to avoid Python's buffering of the output
ENV PYTHONUNBUFFERED 1

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Set the entrypoint to execute the CLI using Poetry
ENTRYPOINT ["python", "-m", "src.cli"]
