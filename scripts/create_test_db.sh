#!/usr/bin/env bash

# Use environment variables from .env file
DB_USER="${DATABASE_USER}"
DB_PASSWORD="${DATABASE_PASSWORD}"
DB_HOST="${DATABASE_HOST}"
DB_PORT="${DATABASE_PORT}"
TEST_DB_NAME="${TEST_DATABASE_NAME}"

# Create a new test database
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -e -c "CREATE DATABASE $TEST_DB_NAME;"
