#!/usr/bin/env bash

# Load environment variables and run the containers
source scripts/run.sh

# Run tests
docker compose -f "$full_docker_compose_path" exec web flake8 /app
docker compose -f "$full_docker_compose_path" exec web black /app --check
docker compose -f "$full_docker_compose_path" exec pg_client /scripts/create_test_db.sh
docker compose -f "$full_docker_compose_path" exec web pytest /app/tests
docker compose -f "$full_docker_compose_path" exec pg_client /scripts/delete_test_db.sh
