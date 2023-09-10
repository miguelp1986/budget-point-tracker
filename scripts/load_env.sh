#!/usr/bin/env bash

current_dir=$(dirname "$0")
parent_dir=$(dirname "$current_dir")
env_file=".env" 
full_env_path="$parent_dir/$env_file"

# Check if the .env file exists
if [ ! -f "$full_env_path" ]; then
  echo ".env file not found: $full_env_path"
  exit 1
fi

# Load the .env file
source "$full_env_path"
