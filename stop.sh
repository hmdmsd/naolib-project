#!/bin/bash

# Stop script for Naolib Transportation Analysis Project

echo "Stopping Naolib Transportation Analysis Environment..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose >/dev/null 2>&1; then
    echo "Error: docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Stop Docker containers
echo "Stopping Docker containers..."
docker-compose down

echo "Environment stopped successfully."