#!/usr/bin/env bash

# Load environment variables
source scripts/load_env.sh

# Build and start the containers
docker compose up -d --build
