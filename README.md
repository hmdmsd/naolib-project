# Naolib Real-Time Transportation Analysis

## Project Overview

This project performs real-time analysis of Nantes public transportation data using the Naolib API. The project combines batch and streaming analysis to provide insights into wait times, delays, and service disruptions.

## Team Members

- Messaoud HAMDI
- Mohamed Amine DAHECH
- Yahia Heni

## Project Structure

- `docker-compose.yml` - Docker environment setup
- `Dockerfile` - Jupyter notebook environment configuration
- `requirements.txt` - Required Python packages
- `naolib_data_collector.ipynb` - Data collection from Naolib API to Kafka
- `naolib_batch_analysis.ipynb` - Batch analysis with Spark, Pandas, and Seaborn
- `naolib_streaming_analysis.ipynb` - Real-time analysis with Spark Streaming

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd naolib-project

# Start the Docker environment
docker-compose up -d
```

### 2. Access Jupyter Notebooks

Open your browser and navigate to:

- Jupyter Notebook: http://localhost:8888
- Spark Master UI: http://localhost:8080
- Kafka UI: http://localhost:8082

### 3. Running the Analysis

1. Run `naolib_data_collector.ipynb` to start collecting data from the Naolib API
2. Run `naolib_batch_analysis.ipynb` to perform historical analysis on collected data
3. Run `naolib_streaming_analysis.ipynb` to monitor transportation data in real-time

## Data Source

This project uses the Naolib API provided by Nantes Métropole:

- API Documentation: https://data.nantesmetropole.fr/explore/dataset/244400404_api-temps-reel-tan/information/
- Example Endpoint: https://open.tan.fr/ewp/tempsattente.json/CRQU

## Features

- Real-time data collection from multiple transportation stops
- Historical analysis of wait times by line, stop, and time of day
- Real-time detection of delays and service disruptions
- Visualization of transportation patterns

## Technologies Used

- Apache Kafka: Data ingestion and message queue
- Apache Spark: Batch and streaming data processing
- PySpark: Python API for Spark
- Pandas & Seaborn: Data manipulation and visualization
- Docker: Containerization and environment management
