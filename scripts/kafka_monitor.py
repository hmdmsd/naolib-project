#!/usr/bin/env python3
"""
Kafka Topic Monitor

This script monitors a Kafka topic and prints messages as they arrive.
Useful for debugging and verification of data ingestion.
"""

import argparse
import json
from kafka import KafkaConsumer
from datetime import datetime

def pretty_print_json(data):
    """Pretty print JSON data"""
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return data
    return json.dumps(data, indent=2)

def monitor_topic(bootstrap_servers, topic, limit=None, pretty=False):
    """Monitor messages on a Kafka topic"""
    print(f"Connecting to Kafka at {bootstrap_servers}...")
    print(f"Monitoring topic: {topic}")
    
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    
    print(f"Connected. Waiting for messages...\n")
    
    count = 0
    try:
        for message in consumer:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            value = message.value
            
            print(f"--- Message received at {timestamp} ---")
            if pretty:
                print(pretty_print_json(value))
            else:
                print(value)
            print()
            
            count += 1
            if limit and count >= limit:
                print(f"Reached limit of {limit} messages.")
                break
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        consumer.close()
        print(f"Received {count} messages in total.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor messages on a Kafka topic")
    parser.add_argument('--bootstrap-servers', default='localhost:9093',
                        help='Kafka bootstrap servers (default: localhost:9093)')
    parser.add_argument('--topic', default='naolib_realtime',
                        help='Kafka topic to monitor (default: naolib_realtime)')
    parser.add_argument('--limit', type=int, default=None,
                        help='Limit number of messages to display (default: unlimited)')
    parser.add_argument('--pretty', action='store_true',
                        help='Pretty print JSON messages')
    
    args = parser.parse_args()
    
    monitor_topic(args.bootstrap_servers, args.topic, args.limit, args.pretty)