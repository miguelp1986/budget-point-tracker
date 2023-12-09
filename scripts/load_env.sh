#!/usr/bin/env bash

# TODO: Add functionality to check the type of environment and load the appropriate .env file

# Check if the .env file exists
if [ ! -f .env ]; then
  echo ".env file not found"
  exit 1
fi

# Load the .env file
source .env
