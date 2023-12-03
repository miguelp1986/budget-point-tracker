#!/usr/bin/env bash

# Use environment variables from .env file
DB_USER="${DATABASE_USER}"
DB_PASSWORD="${DATABASE_PASSWORD}"
DB_HOST="${DATABASE_HOST}"
DB_PORT="${DATABASE_PORT}"
TEST_DB_NAME="${TEST_DATABASE_NAME}"

# Drop the test database
PGPASSWORD=$DB_PASSWORD dropdb -U $DB_USER -h $DB_HOST -p $DB_PORT -e $TEST_DB_NAME
