#!/usr/bin/env python3
"""
Manual API testing script
Usage: python test_api_manually.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "TEST: Root Endpoint")

def test_create_single_record():
    """Test creating a single record"""
    data = {
        "datetime": "2024-01-01T09:30:00",
        "open": 150.25,
        "high": 152.50,
        "low": 149.75,
        "close": 151.00,
        "volume": 1000000
    }
    response = requests.post(f"{BASE_URL}/data", json=data)
    print_response(response, "TEST: Create Single Record")

def test_create_bulk_records():
    """Test creating multiple records"""
    base_date = datetime(2024, 1, 1, 9, 30)
    data = {
        "data": []
    }
    
    # Generate 30 days of data
    for i in range(30):
        record = {
            "datetime": (base_date + timedelta(days=i)).isoformat(),
            "open": 150.0 + i * 0.5,
            "high": 152.0 + i * 0.5,
            "low": 149.0 + i * 0.5,
            "close": 151.0 + i * 0.5,
            "volume": 1000000 + i * 10000
        }
        data["data"].append(record)
    
    response = requests.post(f"{BASE_URL}/data/bulk", json=data)
    print_response(response, "TEST: Create Bulk Records")

def test_get_all_data():
    """Test fetching all data"""
    response = requests.get(f"{BASE_URL}/data")
    print_response(response, "TEST: Get All Data")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal records: {len(data)}")

def test_strategy_performance():
    """Test strategy performance endpoint"""
    response = requests.get(f"{BASE_URL}/strategy/performance?short_window=5&long_window=10")
    print_response(response, "TEST: Strategy Performance")

def test_invalid_data():
    """Test creating record with invalid data"""
    # Test 1: Negative price
    data = {
        "datetime": "2024-01-01T09:30:00",
        "open": -150.25,
        "high": 152.50,
        "low": 149.75,
        "close": 151.00,
        "volume": 1000000
    }
    response = requests.post(f"{BASE_URL}/data", json=data)
    print_response(response, "TEST: Invalid Data - Negative Price")
    
    # Test 2: High < Low
    data = {
        "datetime": "2024-01-01T09:30:00",
        "open": 150.25,
        "high": 149.00,
        "low": 151.75,
        "close": 151.00,
        "volume": 1000000
    }
    response = requests.post(f"{BASE_URL}/data", json=data)
    print_response(response, "TEST: Invalid Data - High < Low")
    
    # Test 3: Missing field
    data = {
        "datetime": "2024-01-01T09:30:00",
        "open": 150.25,
        "high": 152.50,
        # Missing 'low'
        "close": 151.00,
        "volume": 1000000
    }
    response = requests.post(f"{BASE_URL}/data", json=data)
    print_response(response, "TEST: Invalid Data - Missing Field")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("STARTING API TESTS")
    print("="*60)
    
    try:
        # Test basic endpoints
        test_root()
        
        # Test data creation
        test_create_single_record()
        test_create_bulk_records()
        
        # Test data retrieval
        test_get_all_data()
        
        # Test strategy
        test_strategy_performance()
        
        # Test validation
        test_invalid_data()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the API is running at", BASE_URL)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()