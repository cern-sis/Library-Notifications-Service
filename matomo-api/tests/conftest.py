import psycopg2
import pytest
from api import MatomoAPI


@pytest.fixture(scope="module")
def db():
    db_config = {
        "host": "127.0.0.1",
        "database": "matomo",
        "user": "matomo",
        "password": "matomo",
        "port": 5432,
    }
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS inspire_matomo_data (
        id SERIAL PRIMARY KEY,
        date DATE,
        visits INT,
        unique_visitors INT
    )
    """
    cursor.execute(create_table_sql)
    connection.commit()
    yield connection, cursor

    drop_table_sql = "DROP TABLE IF EXISTS inspire_matomo_data"
    cursor.execute(drop_table_sql)
    connection.commit()
    cursor.close()
    connection.close()


@pytest.fixture(autouse=True)
def updated_env(monkeypatch):
    matomo_api_kwargs = dict(
        MATOMO_BASE_URL="https://webanalytics.web.cern.ch",
        MATOMO_AUTH_TOKEN="change-me",
        MATOMO_SITE_ID=1,
        DB_HOST="127.0.0.1",
        MATOMO_DB_NAME="matomo",
        DB_PASSWORD="matomo",
        DB_USER="matomo",
        DB_PORT=5432,
    )
    for env_name, env_value in matomo_api_kwargs.items():
        monkeypatch.setenv(env_name, env_value)


@pytest.fixture(scope="function")
def matomo_api():
    yield MatomoAPI()
