import psycopg2
import pytest


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
