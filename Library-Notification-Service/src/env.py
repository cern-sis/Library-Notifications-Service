"""Module to retreive/declare the environment variables."""

import os

MAX_NOTIFICATION_RESULTS_COUNT = os.environ["MAX_NOTIFICATION_RESULTS_COUNT"]

LIBRARY_CATALOGUE_SITE_API = os.environ["LIBRARY_CATALOGUE_SITE_API"]
LIBRARY_CATALOGUE_SITE_URL = os.environ["LIBRARY_CATALOGUE_SITE_URL"]
LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API = os.environ[
    "LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API"
]
LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API = os.environ[
    "LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API"
]
LIBRARY_CATALOGUE_BACKOFFICE_API_TOKEN = os.environ[
    "LIBRARY_CATALOGUE_BACKOFFICE_API_TOKEN"
]

NOTIFICATIONS_API_URL = os.environ["NOTIFICATIONS_API_URL"]
NOTIFICATIONS_API_SECRET = os.environ["NOTIFICATIONS_API_SECRET"]
NOTIFICATIONS_CHANNEL_ID = os.environ["NOTIFICATIONS_CHANNEL_ID"]


"""
export MAX_NOTIFICATION_RESULTS_COUNT=20
export LIBRARY_CATALOGUE_SITE_API="https://catalogue.library.cern/api/literature/?q="
export LIBRARY_CATALOGUE_SITE_URL="https://catalogue.library.cern/search?q="
export LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API="https://catalogue.library.cern/api/items/?q="
export LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API="https://catalogue.library.cern/api/eitems/?q="
export NOTIFICATIONS_API_URL="https://notifications.web.cern.ch/api/notifications"
export NOTIFICATIONS_CHANNEL_ID="4e383ca0-7df0-421f-a062-741d5d459cd8"
"""
