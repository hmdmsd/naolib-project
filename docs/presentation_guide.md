# Naolib Project Presentation Guide

## Presentation Duration: 15 minutes

### Introduction (2 minutes) - Messaoud HAMDI

- Brief overview of the project goals and objectives
- Introduction to the Naolib API and its importance
- Explain the transportation context in Nantes
- Show the API structure and key endpoints

### Data Collection Process (3 minutes) - Mohamed Amine DAHECH

- Explain how we collect data from the Naolib API
- Show the `naolib_data_collector.ipynb` notebook
- Explain the data ingestion process with Kafka
- Highlight the key stops we monitor and why they were chosen
- Show a sample of the raw data structure

### Batch Analysis Results (5 minutes) - Yahia Heni

- Present the main findings from the historical analysis
- Show the `naolib_batch_analysis.ipynb` notebook
- Present key visualizations:
  - Average wait times by line and stop
  - Wait time patterns by time of day
  - Day of week analysis
  - Destination/terminus analysis
- Explain the implications of these findings for transportation planning

### Streaming Analysis Demonstration (4 minutes) - Messaoud HAMDI

- Show the `naolib_streaming_analysis.ipynb` notebook
- Demonstrate real-time monitoring capabilities
- Explain the time window concepts used in streaming analytics
- Show how the system detects delays and service disruptions
- Highlight the real-time dashboards and alerts

### Conclusion (1 minute) - Mohamed Amine DAHECH

- Summarize the project's achievements
- Discuss potential future enhancements
- Highlight the value provided to transportation users and planners
- Thank the audience and open for questions

## Presentation Tips

- Practice your section to ensure it fits within the time limit
- Focus on the most interesting insights rather than technical details
- Have screenshots ready in case of technical issues during the demo
- Keep explanations simple and focus on the value of the analysis
- Be prepared to explain how this project meets the course requirements
