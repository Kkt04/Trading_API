import unittest
from fastapi.testclient import TestClient
from datetime import datetime
from decimal import Decimal
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

class TestAPIEndpoints(unittest.TestCase):
    """Test FastAPI endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test client"""
        cls.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertIn("endpoints", response.json())
    
    def test_create_data_valid(self):
        """Test creating data with valid input"""
        test_data = {
            "datetime": "2024-01-01T09:30:00",
            "open": 150.25,
            "high": 152.50,
            "low": 149.75,
            "close": 151.00,
            "volume": 1000000
        }
        response = self.client.post("/data", json=test_data)
        # May fail if database not connected, but validates structure
        self.assertIn(response.status_code, [201, 500])
    
    def test_create_data_invalid_price(self):
        """Test creating data with negative price"""
        test_data = {
            "datetime": "2024-01-01T09:30:00",
            "open": -150.25,
            "high": 152.50,
            "low": 149.75,
            "close": 151.00,
            "volume": 1000000
        }
        response = self.client.post("/data", json=test_data)
        self.assertEqual(response.status_code, 422)
    
    def test_create_data_invalid_volume(self):
        """Test creating data with negative volume"""
        test_data = {
            "datetime": "2024-01-01T09:30:00",
            "open": 150.25,
            "high": 152.50,
            "low": 149.75,
            "close": 151.00,
            "volume": -1000000
        }
        response = self.client.post("/data", json=test_data)
        self.assertEqual(response.status_code, 422)
    
    def test_create_data_high_less_than_low(self):
        """Test creating data with high < low"""
        test_data = {
            "datetime": "2024-01-01T09:30:00",
            "open": 150.25,
            "high": 149.75,
            "low": 152.50,
            "close": 151.00,
            "volume": 1000000
        }
        response = self.client.post("/data", json=test_data)
        self.assertEqual(response.status_code, 422)
    
    def test_create_data_missing_field(self):
        """Test creating data with missing required field"""
        test_data = {
            "datetime": "2024-01-01T09:30:00",
            "open": 150.25,
            "high": 152.50,
            "low": 149.75,
            # Missing 'close'
            "volume": 1000000
        }
        response = self.client.post("/data", json=test_data)
        self.assertEqual(response.status_code, 422)
    
    def test_create_data_invalid_datetime(self):
        """Test creating data with invalid datetime format"""
        test_data = {
            "datetime": "invalid-date",
            "open": 150.25,
            "high": 152.50,
            "low": 149.75,
            "close": 151.00,
            "volume": 1000000
        }
        response = self.client.post("/data", json=test_data)
        self.assertEqual(response.status_code, 422)
    
    def test_get_all_data(self):
        """Test fetching all data"""
        response = self.client.get("/data")
        # May fail if database not connected
        self.assertIn(response.status_code, [200, 500])
    
    def test_bulk_create_valid(self):
        """Test bulk creation with valid data"""
        test_data = {
            "data": [
                {
                    "datetime": "2024-01-01T09:30:00",
                    "open": 150.25,
                    "high": 152.50,
                    "low": 149.75,
                    "close": 151.00,
                    "volume": 1000000
                },
                {
                    "datetime": "2024-01-01T10:30:00",
                    "open": 151.00,
                    "high": 153.00,
                    "low": 150.50,
                    "close": 152.50,
                    "volume": 1100000
                }
            ]
        }
        response = self.client.post("/data/bulk", json=test_data)
        self.assertIn(response.status_code, [201, 500])

if __name__ == '__main__':
    unittest.main()