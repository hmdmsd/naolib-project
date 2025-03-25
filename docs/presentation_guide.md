# Naolib Project Presentation Guide

## Project Overview

Duration: 15 minutes total
Team: Messaoud HAMDI, Mohamed Amine DAHECH, Yahia Heni

## Presentation Structure

### 1. Introduction (3 minutes) - Messaoud HAMDI

#### Project Context

- Introduce the team
- Explain what Naolib is (Nantes public transportation system)
- Explain the purpose of our project: analyzing real-time transportation data to derive insights

#### Architecture Overview

- Explain the overall architecture diagram:
  1. Data Source: Naolib API
  2. Data Collection: Python script to fetch data
  3. Message Queue: Kafka for data storage and streaming
  4. Processing: Batch and streaming analysis with Spark/Pandas
  5. Visualization: Using Pandas and Seaborn

#### Technology Stack Overview

- **Apache Kafka**: Distributed event streaming platform

  - Explain how Kafka works at a high level:
    - Topics: Categories for message streams (our "naolib_realtime" topic)
    - Producers: Systems that publish messages (our data collector)
    - Consumers: Systems that subscribe to topics (our analysis notebooks)
  - Why we chose Kafka: Reliable, scalable, handles real-time data streams

- **Apache Spark/Pandas**: Data processing tools
  - Explain the difference between batch and streaming analysis
  - Note that we had to adapt our approach due to integration challenges

### 2. Data Collection (3 minutes) - Mohamed Amine DAHECH

#### Naolib API Exploration

- Explain the structure of the Naolib API
  - Show examples of endpoints (tempsattentelieu.json)
  - Explain the data structure (stops, wait times, lines)
- Demonstrate knowledge of the API documentation
- Explain rate limits and considerations

#### Data Collection Implementation

- Walk through the `naolib_data_collector.ipynb` notebook:
  1. How we connect to the API (requests library)
  2. How we parse the JSON response
  3. How we structure the data for Kafka
  4. The polling frequency and why we chose it

#### Kafka Producer Implementation

- Explain how we send data to Kafka:
  1. Setting up the Kafka producer
  2. Serializing data
  3. Topic organization
  4. Error handling
- Show code snippets that demonstrate the Kafka producer configuration

### 3. Batch Analysis (4 minutes) - Yahia Heni

#### Data Processing

- Explain how we prepare the data for analysis in `naolib_batch_analysis_simple.ipynb`:
  1. Reading from Kafka using the Python client
  2. Parsing and cleaning the data
  3. Converting wait time text to numeric values
  4. Expanding the nested structure (arrivals array)

#### Analysis 1: Wait Times by Line and Stop

- Present the first batch analysis:
  1. How we grouped and aggregated the data
  2. Visualization approach
  3. Key findings (which lines/stops have longest wait times)
  4. Business implications of these findings

#### Analysis 2: Time of Day Patterns

- Present the second batch analysis:
  1. How we extracted time information
  2. Visualization of wait times by hour
  3. Key findings (peak hours, quietest times)
  4. How this information benefits passengers and planners

#### Summary of Batch Findings

- Highlight the most important insights from batch analysis
- Explain how these findings provide value

### 4. Streaming Analysis (4 minutes) - Messaoud HAMDI

#### Streaming Approach

- Explain our approach to streaming analysis in `naolib_streaming_analysis_simple.ipynb`:
  1. Why we simulated streaming using periodic polling
  2. How we implemented time windows
  3. The two streaming analyses we implemented

#### Analysis 1: Real-time Average Wait Times

- Present the first streaming analysis:
  1. Sliding 10-minute window implementation
  2. Real-time aggregation by line
  3. How this could be used for passenger information systems
  4. Demo of the visualization

#### Analysis 2: Delay Detection

- Present the second streaming analysis:
  1. 15-minute window for delay detection
  2. How we classify delay severity (minor, moderate, severe)
  3. How transportation operators can use this for service management
  4. Demo of the alerts system

#### Challenges and Solutions

- Explain the challenges we faced with Spark-Kafka integration
- How we adapted our approach to overcome technical issues
- The value of the solution despite the workarounds

### 5. Conclusion (1 minute) - Mohamed Amine DAHECH

#### Project Summary

- Recap what we accomplished:
  1. Real-time data collection from public API
  2. Kafka integration for message queuing
  3. Two batch analyses with valuable insights
  4. Two streaming analyses for real-time monitoring

#### Future Extensions

- Briefly mention potential improvements:
  1. Dashboard development
  2. Predictive modeling for wait times
  3. Integration with other data sources (weather, events)
  4. Mobile app for real-time alerts

#### Questions

- Open for questions

## Presentation Tips

### Technical Demonstration

- Have screenshots ready in case of live demo issues
- Prepare a recorded demo as backup if time allows
- Highlight the most interesting parts of the code, not every line

### Explaining Kafka

- Use simple analogies for Kafka:
  - "Kafka is like a message queue system - imagine a mailbox where our data collector drops messages that our analysis tools can pick up at their own pace"
  - "Topics are like channels - our project has one channel called 'naolib_realtime' where all transportation data flows"
  - "Producers write messages, Consumers read them - this decouples the systems and makes the architecture more robust"

### Visuals to Include

- Architecture diagram showing data flow
- Sample of the API response
- Key visualizations from both notebooks:
  - Heatmap/bar chart of wait times by line and stop
  - Line chart of wait times by hour of day
  - Real-time monitoring dashboard
  - Delay detection alerts

### Code Highlights

For each notebook, highlight these code sections:

- `naolib_data_collector.ipynb`:

  - API request function
  - Kafka producer configuration
  - Data transformation

- `naolib_batch_analysis_simple.ipynb`:

  - Kafka consumer code
  - Data expansion logic
  - Key aggregations
  - Visualization code

- `naolib_streaming_analysis_simple.ipynb`:
  - Simulated windowing approach
  - Real-time aggregation logic
  - Delay detection algorithm

## Technical Knowledge to Demonstrate

### Kafka Knowledge

- Topics, partitions, consumers, producers
- Serialization/deserialization of messages
- Kafka's role in big data architectures
- Consumer groups concept

### API Knowledge

- RESTful API concepts
- JSON parsing
- Rate limiting considerations
- Error handling

### Data Analysis Knowledge

- Data cleaning and transformation
- Time-based aggregations
- Statistical measures (mean, median, std)
- Proper visualization techniques

### Streaming Concepts

- Time windows (sliding vs. tumbling)
- Real-time aggregations
- Event time vs. processing time
- Handling late data
