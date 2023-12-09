#!/usr/bin/env bash

# Load environment variables and run the containers
source scripts/run.sh

# Run tests
docker compose exec web flake8 /app
docker compose exec web black /app --check
docker compose exec pg_client /scripts/create_test_db.sh
docker compose exec web pytest /app/tests
docker compose exec pg_client /scripts/delete_test_db.sh
