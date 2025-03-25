# Naolib Project Architecture

This document outlines the architecture of the Naolib Real-time Transportation Analysis project, including our implementation choices and adaptations.

## System Architecture (Text Description)

Our system architecture follows a modular design with five main components:

```
[Naolib API] → [Data Collector] → [Kafka Message Broker] → [Analysis Layer] → [Visualization]
                     ↑                      ↑                       ↓
                  Requests               Topics                     ↓
                     ↑                      ↑                       ↓
                     └──────────────────────┴───────────────────────┘
                                     Data Flow
```

1. **Data Source**: Naolib API
2. **Data Collection**: Python script in Jupyter notebook
3. **Message Broker**: Apache Kafka
4. **Processing**: Batch & simulated streaming analysis
5. **Visualization**: Pandas, Seaborn, Matplotlib

Data flows from the Naolib API through our collector, into Kafka, then to our analysis notebooks, with results displayed through visualizations.

### Components

1. **Data Source**:

   - Naolib API provides real-time data about public transportation in Nantes
   - REST API endpoints return JSON data about bus/tram wait times
   - Example endpoint: `https://open.tan.fr/ewp/tempsattentelieu.json/{stop_code}/{num_passages}`

2. **Data Collection Layer**:

   - Python script (`naolib_data_collector.ipynb`) pulls data from the API at regular intervals
   - Uses Python's `requests` library for API interaction
   - Enriches data with timestamps and metadata
   - Implements Kafka producer to send data to messaging layer

3. **Messaging Layer**:

   - Apache Kafka serves as the message broker
   - Topic: `naolib_realtime` stores all transportation data
   - Benefits:
     - Decouples data collection from processing
     - Provides persistent storage of messages
     - Enables both batch and streaming analysis from the same data

4. **Processing Layer**:

   - Initially designed to use PySpark for both batch and streaming analysis
   - Due to integration challenges between Spark and Kafka in our environment, we adapted to:
     - `naolib_batch_analysis_simple.ipynb`: Uses Python Kafka client for direct reading from Kafka, with Pandas for analysis
     - `naolib_streaming_analysis_simple.ipynb`: Simulates streaming with periodic polling of Kafka, implements time windows in application code

5. **Visualization Layer**:
   - Pandas and Seaborn for data visualization
   - Matplotlib for interactive charts
   - Displays results directly in Jupyter notebooks

### Data Flow

1. **Collection Flow**:

   - Data collector polls Naolib API every 30 seconds
   - Extracts wait time data for key transportation stops in Nantes
   - Enriches data with collection timestamps and metadata
   - Serializes to JSON and sends to Kafka topic `naolib_realtime`

2. **Batch Analysis Flow**:

   - Batch analysis notebook consumes all historical messages from Kafka topic
   - Expands nested arrival data into flat structure
   - Performs two key analyses:
     - Average wait times by line and stop
     - Wait time distribution by hour of day
   - Visualizes results using Seaborn and Matplotlib
   - Generates summary of key findings

3. **Streaming Analysis Flow**:
   - Streaming analysis notebook continuously polls for new messages
   - Implements a simulated sliding window approach using timestamps
   - Performs two real-time analyses:
     - Real-time average wait times (10-minute window)
     - Delay detection and alerting (15-minute window)
   - Updates visualizations in real-time as new data arrives

## Time Windows

Our project uses time windowing for streaming analysis:

1. **10-minute sliding windows** for average wait times

   - Implementation: Filter data collected in the last 10 minutes
   - Updates every polling cycle
   - Provides a smoothed view of current wait times

2. **15-minute sliding windows** for delay detection
   - Longer window to improve reliability of delay detection
   - Identifies patterns suggesting service disruptions
   - Allows classification of delay severity

## Implementation Details

### Kafka Integration

- **Producer**: KafkaProducer in `naolib_data_collector.ipynb`

  - Configuration: `bootstrap_servers='kafka:9092'`
  - JSON serialization: `value_serializer=lambda v: json.dumps(v).encode('utf-8')`
  - Topic: `naolib_realtime`

- **Consumer**: KafkaConsumer in batch and streaming notebooks
  - Direct Python client used instead of Spark-Kafka integration
  - Configuration: `bootstrap_servers='kafka:9092', auto_offset_reset='earliest'`
  - JSON deserialization: `message.value.decode('utf-8')`

### Data Schema

The main data schema in our Kafka messages:

```
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "stop_code": "XXXX",
  "stop_name": "Stop Name",
  "arrivals": [
    {
      "sens": 1,
      "terminus": "Destination Name",
      "infotrafic": false,
      "temps": "X min",
      "dernierDepart": "...",
      "tempsReel": "...",
      "ligne": {
        "numLigne": "C6",
        "typeLigne": "..."
      },
      "arret": {
        "codeArret": "XXXX"
      }
    },
    ...
  ]
}
```

After processing, we expand this nested structure to create a flattened dataframe with one row per arrival:

```
- timestamp: When the data was collected
- stop_code: Code of the stop (e.g., "COMM")
- stop_name: Name of the stop (e.g., "Commerce")
- direction: Direction code
- terminus: Final destination
- wait_time_text: Original wait time text (e.g., "5 min", "proche")
- wait_time_minutes: Converted numeric wait time
- is_real_time: Whether the time is based on real-time data
- line_number: Bus/tram line number (e.g., "C6")
- processing_time: When the data was processed
```

### Adaptation Challenges

Our project faced several integration challenges that required adaptations:

1. **Spark-Kafka Integration**: We encountered issues with the Spark-Kafka connector in our environment. Rather than spending excessive time on configuration, we adapted by:

   - Using the direct Python Kafka client
   - Implementing data processing in Pandas
   - Creating a simulated streaming approach with periodic polling

2. **Time Windows**: Without native Spark Streaming windows, we implemented time windowing by:
   - Adding processing_time timestamps to all data
   - Filtering based on these timestamps to simulate windows
   - Recalculating aggregations on each polling cycle

These adaptations demonstrate our ability to problem-solve while still achieving the project objectives.

## Environment

The project environment runs in Docker containers:

- Kafka for messaging
- Zookeeper for Kafka coordination
- Spark for processing (though we adapted to use less of Spark's features)
- Jupyter notebook for interactive analysis

## Future Improvements

With more time, our architecture could be enhanced with:

1. **Proper Spark Streaming**: Resolve Spark-Kafka integration for true streaming
2. **Persistent Storage**: Add a time-series database for long-term storage
3. **Interactive Dashboard**: Create a real-time web dashboard
4. **Alert System**: Implement email or SMS notifications for severe delays
5. **Machine Learning**: Add predictive models for wait time forecasting
