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

export MAX_NOTIFICATION_RESULTS_COUNT=20
export LIBRARY_CATALOGUE_SITE_API="https://catalogue.library.cern/api/literature/?q="
export LIBRARY_CATALOGUE_SITE_URL="https://catalogue.library.cern/search?q="
export LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API="https://catalogue.library.cern/api/items/?q="
export LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API="https://catalogue.library.cern/api/eitems/?q="
export NOTIFICATIONS_API_URL="https://notifications.web.cern.ch/api/notifications"
export NOTIFICATIONS_CHANNEL_ID="4e383ca0-7df0-421f-a062-741d5d459cd8"


# Set the entrypoint to execute the CLI using Poetry
ENTRYPOINT ["python", "-m", "src.cli", "newsletter"]
