#!/bin/bash

# Pull latest django app image
docker compose pull

# Stop existing build
docker compose down

# Start containers
docker compose up -d

# Remove dangling images
docker image prune -f