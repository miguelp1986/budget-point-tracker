#!/usr/bin/env bash

# Sets GitHub secrets from an .env file
while IFS= read -r line; do
    # Skip empty lines and lines starting with #
    if [[ -z "$line" || "$line" == \#* ]]; then
        continue
    fi

    # Splitting line into key and value
    IFS='=' read -r key value <<< "$line"
    
    # Set the GitHub secret
    gh secret set "$key" --body "$value"
done < .env

