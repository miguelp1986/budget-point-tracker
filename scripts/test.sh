#!/usr/bin/env bash

# Load environment variables
source scripts/load_env.sh

# Construct the full path to the Docker compose file
docker_compose_file="docker-compose.yml"
full_docker_compose_path="$parent_dir/$docker_compose_file"

# Check if the Docker Compose file exists
if [ ! -f "$full_docker_compose_path" ]; then
  echo "Docker Compose file not found: $full_docker_compose_path"
  exit 1
fi

# Run tests
docker compose -f "$full_docker_compose_path" exec web flake8 /app
docker compose -f "$full_docker_compose_path" exec web black /app --check
docker compose -f "$full_docker_compose_path" exec web pytest /app/tests
