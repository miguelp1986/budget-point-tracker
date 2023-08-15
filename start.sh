#!/usr/bin/env bash

# Get the directory path of this file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the name of your .env file
ENV_FILE=".env" 
FULL_ENV_PATH="$SCRIPT_DIR/$ENV_FILE"

# Check if the .env file exists
if [ ! -f "$FULL_ENV_PATH" ]; then
  echo ".env file not found: $FULL_ENV_PATH"
  exit 1
fi

# Load the .env file
source "$FULL_ENV_PATH"

# Construct the full path to the Docker compose file
DOCKER_COMPOSE_FILE="docker-compose.yml"
FULL_DOCKER_COMPOSE_PATH="$SCRIPT_DIR/$DOCKER_COMPOSE_FILE"

# Check if the Docker Compose file exists
if [ ! -f "$FULL_DOCKER_COMPOSE_PATH" ]; then
  echo "Docker Compose file not found: $FULL_DOCKER_COMPOSE_PATH"
  exit 1
fi

# Stop container if it is running
docker stop ${DOCKER_IMAGE}:${DOCKER_TAG}  # Run only if the container is running

# Remove previously-ran containers
docker rm -f ${DOCKER_IMAGE}:${DOCKER_TAG}  # TODO: check if this exists before running

# Remove old images
docker rmi -f $(docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG})  # TODO: check if this exists before running

# Build Docker images and start the containers
docker compose -f "$FULL_DOCKER_COMPOSE_PATH" up --build

# Run tests in Docker container
# docker compose -f "$FULL_DOCKER_COMPOSE_PATH" exec -T <container_name> <command>

