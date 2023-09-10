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

# # Stop container if it is running
# docker stop ${docker_image}:${docker_tag}  # Run only if the container is running

# # Remove previously-ran containers
# docker rm -f ${docker_image}:${docker_tag}  # TODO: check if this exists before running

# # Remove old images
# docker rmi -f $(docker images -q ${docker_image}:${docker_tag})  # TODO: check if this exists before running

# Build Docker images (this will rebuild only if there's a change)
docker compose -f "$full_docker_compose_path" build

# Run the containers
docker compose -f "$full_docker_compose_path" up
