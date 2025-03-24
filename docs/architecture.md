# Naolib Project Architecture

This document outlines the architecture of the Naolib Real-time Transportation Analysis project.

## System Architecture

![Architecture Diagram](https://mermaid.ink/img/pako:eNqFk01v2zAMhv8K4VMLOLbj2HYQYEDRYYcBKdpedgx0OLbYWKIr0SiKIP99tN2mbYIum2GIZL_Pw48UbrlRChfcuK2y8BHJzn2lGdZ8r0Bw_o0i5YV0kqJLlUvF92qQxPrWsGr5HcLV5Xy23CyX14vrf5Iojb-oWIeIoGh7l1cUtfLQNgS35OJG2VSSQzDzTkVj7MQw-3l3t359fHrYbNfPm8fr2w_fPn79_PFmf3g95J1X1YrXeIYWvVQIbZ-8t-UrKw6WvwYJUL13UDIrUTgYNFLgDnYLMtOYXEpKKW28-wO8lcrxKj4VQIIyIlUpGGmfHjyapFqGFKSzrJRYuJRTIGmJQqjOMhOVLXcPrgQq2k9cPrtYn_rMf5dBqw3LtMg13SYWolC70p6vHgOqFPLRsZ-Gw06adKf7nnunBYqD5tqR3ydLvWRWKgdoE3nGttx2QIX2nQDhxBLpGV1z-F6kPVPCsM5SnRqqHO97Cg_KOqZoCvRSK3OU18tBa3Qp-qvfYvJT6qlLTtvG5sDK-1IlZXGbU3ygTnJNYWEcqgLk5JpNwQrTZZMV9PG5pRrSu81wKcCdYd8gqDrFHxnVcm1Y84yfaBsdBkavobw1xMtIJ0n9vPMLnWROQp9J0AxZEBnPuYJ3PsVFl3fKwC2U5lQf5Z6hkBKe2L6LcOGZyiKFbEYv4i-xmvPaD5J5PBELHvZXQ2PHjIYlUJrhwrf-7h8w4hEp)

### Components

1. **Data Source**:

   - Naolib API provides real-time data about public transportation in Nantes
   - REST API endpoints return JSON data

2. **Data Collection Layer**:

   - Python script pulls data from the API at regular intervals
   - Jupyter notebook environment for interactive data collection
   - Data is enriched with timestamps and metadata

3. **Messaging Layer**:

   - Apache Kafka serves as the message broker
   - Topic: `naolib_realtime` stores all transportation data
   - Ensures reliable delivery and persistence of data

4. **Processing Layer**:

   - Apache Spark (PySpark) for both batch and streaming analysis
   - Batch processing for historical analysis
   - Structured streaming for real-time analysis with time windows

5. **Visualization Layer**:
   - Pandas and Seaborn for batch analysis visualization
   - Console output for streaming analysis results

### Data Flow

1. **Collection Flow**:

   - The `naolib_data_collector.ipynb` notebook polls the Naolib API every 30 seconds
   - Data is enriched with collection timestamps and metadata
   - The enriched data is sent to Kafka topic `naolib_realtime`

2. **Batch Analysis Flow**:

   - The `naolib_batch_analysis.ipynb` notebook reads all historical data from Kafka
   - Data is processed using Spark SQL
   - Results are converted to Pandas DataFrames for visualization
   - Visualizations show patterns and statistics about wait times

3. **Streaming Analysis Flow**:
   - The `naolib_streaming_analysis.ipynb` notebook connects to Kafka
   - Structured streaming processes data in real-time using time windows
   - Results are continuously updated and displayed in the console

## Time Windows

This project employs various time windows for streaming analysis:

1. **10-minute sliding windows** with 2-minute slides

   - Used for calculating real-time average wait times
   - Provides a smoothed view that updates frequently

2. **15-minute sliding windows** with 5-minute slides

   - Used for delay detection
   - Balances responsiveness with stability in alerts

3. **30-minute tumbling windows**
   - Used for service disruption pattern detection
   - Provides a more comprehensive view for identifying systemic issues

## Schema

The main data schema includes:

```
message
├── timestamp (string)
├── stop_code (string)
├── stop_name (string)
└── arrivals (array)
    ├── sens (string)
    ├── terminus (string)
    ├── infotrafic (boolean)
    ├── temps (string)
    ├── dernierDepart (string)
    ├── tempsReel (string)
    ├── ligne
    │   ├── numLigne (string)
    │   └── typeLigne (string)
    └── arret
        └── codeArret (string)
```

After processing, the key fields for analysis are:

- `collection_timestamp`: When the data was collected
- `stop_name`: Name of the stop
- `line_number`: Bus/tram line number
- `terminus`: Final destination
- `wait_time_minutes`: Wait time in minutes
- `is_real_time`: Whether the time is based on real-time data

## Environment

The entire solution runs in Docker containers:

- Kafka and Zookeeper for messaging
- Spark master and worker for processing
- Jupyter notebook for interactive analysis

## Future Enhancements

Potential enhancements to this architecture include:

1. Persistent storage with a time-series database
2. Web-based dashboards for real-time monitoring
3. Notifications via email or messaging for severe delays
4. Machine learning models for predictive analytics
5. Integration with other data sources (weather, events, etc.)
