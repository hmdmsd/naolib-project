#!/bin/bash

# Start script for Naolib Transportation Analysis Project

echo "Starting Naolib Transportation Analysis Environment..."

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

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

# Wait for services to initialize
echo "Waiting for services to initialize (this may take a few minutes)..."
sleep 15

# Check if Kafka is ready
echo "Checking if Kafka is ready..."
MAX_ATTEMPTS=10
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if docker-compose exec kafka kafka-topics.sh --list --bootstrap-server kafka:9092 >/dev/null 2>&1; then
        echo "Kafka is ready!"
        break
    fi
    ATTEMPT=$((ATTEMPT+1))
    echo "Waiting for Kafka to be ready... (attempt $ATTEMPT/$MAX_ATTEMPTS)"
    sleep 10
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo "Error: Kafka did not become ready in time. Please check Docker logs."
    exit 1
fi

# Create Kafka topic if it doesn't exist
echo "Creating Kafka topic 'naolib_realtime' if it doesn't exist..."
docker-compose exec kafka kafka-topics.sh --create --if-not-exists --topic naolib_realtime --bootstrap-server kafka:9092 --partitions 3 --replication-factor 1

# Print URLs for services
echo ""
echo "=== Naolib Transportation Analysis Environment Ready ==="
echo "Jupyter Notebook: http://localhost:8888"
echo "Spark Master UI: http://localhost:8080"
echo "Kafka UI: http://localhost:8082"
echo ""
echo "Start your analysis by running the notebooks in the following order:"
echo "1. naolib_data_collector.ipynb - Collect data from Naolib API"
echo "2. naolib_batch_analysis.ipynb - Analyze historical data"
echo "3. naolib_streaming_analysis.ipynb - Monitor data in real-time"
echo ""
echo "To stop the environment, run: docker-compose down"