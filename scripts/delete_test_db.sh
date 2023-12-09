#!/usr/bin/env bash

# Use environment variables from .env file
DB_USER="${TEST_DATABASE_USER}"
DB_PASSWORD="${TEST_DATABASE_PASSWORD}"
DB_HOST="${TEST_DATABASE_HOST}"
DB_PORT="${TEST_DATABASE_PORT}"
TEST_DB_NAME="${TEST_DATABASE_NAME}"

# Drop the test database
PGPASSWORD=$DB_PASSWORD dropdb -U $DB_USER -h $DB_HOST -p $DB_PORT -e $TEST_DB_NAME
