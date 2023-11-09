#!/usr/bin/env bash

# Load environment variables and run the containers
source source scripts/run.sh

# Run tests
docker compose -f "$full_docker_compose_path" exec web flake8 /app
docker compose -f "$full_docker_compose_path" exec web black /app --check
docker compose -f "$full_docker_compose_path" exec web pytest /app/tests