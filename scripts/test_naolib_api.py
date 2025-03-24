#!/usr/bin/env python3
"""
Naolib API Tester

This script tests connectivity to the Naolib API and explores the data structure.
Useful for initial exploration and verification before starting the full pipeline.
"""

import argparse
import json
import requests
from tabulate import tabulate

def test_stop_data(stop_code, num_passages=5):
    """Test retrieving data for a specific stop"""
    url = f"https://open.tan.fr/ewp/tempsattentelieu.json/{stop_code}/{num_passages}"
    
    print(f"Testing API endpoint: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        data = response.json()
        print("\n✅ Successfully retrieved data!")
        print(f"Number of arrivals: {len(data)}")
        
        # Extract useful information for display
        arrivals = []
        for item in data:
            line_num = item.get('ligne', {}).get('numLigne', 'Unknown')
            terminus = item.get('terminus', 'Unknown')
            wait_time = item.get('temps', 'Unknown')
            is_real_time = item.get('tempsReel', False)
            
            arrivals.append([line_num, terminus, wait_time, 'Yes' if is_real_time else 'No'])
        
        # Display arrivals in a table
        print("\nNext arrivals:")
        print(tabulate(arrivals, 
                      headers=['Line', 'Destination', 'Wait Time', 'Real-time?'],
                      tablefmt='grid'))
        
        # Show full JSON for the first arrival
        if data:
            print("\nSample data structure (first arrival):")
            print(json.dumps(data[0], indent=2))
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error accessing API: {str(e)}")
        return False

def list_nearby_stops(latitude, longitude):
    """List stops near a specific location"""
    url = f"https://open.tan.fr/ewp/arrets.json/{latitude}/{longitude}"
    
    print(f"Finding stops near coordinates {latitude}, {longitude}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        print(f"\n✅ Found {len(data)} stops nearby!")
        
        # Extract stop information
        stops = []
        for item in data:
            code = item.get('codeLieu', 'Unknown')
            name = item.get('libelle', 'Unknown')
            distance = item.get('distance', 'Unknown')
            lines = [line.get('numLigne', '') for line in item.get('ligne', [])]
            lines_str = ', '.join(lines)
            
            stops.append([code, name, distance, lines_str])
        
        # Display stops in a table
        print("\nNearby stops:")
        print(tabulate(stops, 
                      headers=['Code', 'Name', 'Distance', 'Lines'],
                      tablefmt='grid'))
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error accessing API: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Naolib API")
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Stop data parser
    stop_parser = subparsers.add_parser('stop', help='Get data for a specific stop')
    stop_parser.add_argument('stop_code', help='Stop code (e.g., COMM, CRQU)')
    stop_parser.add_argument('--passages', type=int, default=5,
                          help='Number of passages to retrieve (default: 5)')
    
    # Nearby stops parser
    nearby_parser = subparsers.add_parser('nearby', help='Find stops near coordinates')
    nearby_parser.add_argument('latitude', help='Latitude (e.g., 47.21661)')
    nearby_parser.add_argument('longitude', help='Longitude (e.g., -1.556754)')
    
    args = parser.parse_args()
    
    if args.command == 'stop':
        test_stop_data(args.stop_code, args.passages)
    elif args.command == 'nearby':
        list_nearby_stops(args.latitude, args.longitude)
    else:
        parser.print_help()