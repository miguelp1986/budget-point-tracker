#!/usr/bin/env bash

# Create .env file from GitHub secrets using gh CLI

# Fetch the list of all secrets using the GitHub CLI
secrets=$(gh secret list | awk '{print $1}')

# Create the .env file
for secret_name in $secrets; do
    # Use gh CLI to retrieve the secret value
    secret_value=$(gh secret view "$secret_name" --json value -q .value)

    # Write to the .env file
    echo "$secret_name=$secret_value" >> .env
done