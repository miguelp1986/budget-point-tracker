#!/usr/bin/env python

"""
ONLY TO BE USED IN DEVELOPMENT!

This script deletes the databases of this applicatoin if they exist.
"""

import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.utils.config import Config
from src.utils.logger import get_logger

config = Config()

# Get or create logger
logger = get_logger()


def delete_database(
    db_name: str, db_user: str, db_password: str, db_host: str, db_port: str
):
    """
    Delete a PostgreSQL database if it exists.
    """
    conn_info = f"dbname='postgres' user='{db_user}' password='{db_password}' host='{db_host}' port='{db_port}'"

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(conn_info)
        conn.set_isolation_level(
            ISOLATION_LEVEL_AUTOCOMMIT
        )  # set isolation level to autocommit so we can create a database
        cur = conn.cursor()

        # check if database exists
        cur.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,)
        )
        exists = cur.fetchone()  # returns None if database does not exist
        if exists:
            # execute SQL query to delete a database if it exists
            cur.execute(f"DROP DATABASE {db_name}")
            logger.info(f"Database {db_name} deleted successfully.")
        else:
            logger.info(f"Database {db_name} does not exist.")

        cur.close()

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # get database info from environment variables
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")

    pytest_db_name = os.getenv("PYTEST_DATABASE_NAME")
    pytest_db_user = os.getenv("PYTEST_DATABASE_USER")
    pytest_db_password = os.getenv("PYTEST_DATABASE_PASSWORD")
    pytest_db_host = os.getenv("PYTEST_DATABASE_HOST")
    pytest_db_port = os.getenv("PYTEST_DATABASE_PORT")

    # delete databases if they exist
    delete_database(db_name, db_user, db_password, db_host, db_port)
    delete_database(
        pytest_db_name,
        pytest_db_user,
        pytest_db_password,
        pytest_db_host,
        pytest_db_port,
    )
