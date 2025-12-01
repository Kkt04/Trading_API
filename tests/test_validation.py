import unittest
from decimal import Decimal
from datetime import datetime
from pydantic import ValidationError
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import TickerDataCreate

class TestDataValidation(unittest.TestCase):
    """Test input validation for ticker data"""
    
    def test_valid_data(self):
        """Test creation with valid data"""
        data = TickerDataCreate(
            datetime=datetime(2024, 1, 1, 9, 30),
            open=Decimal("150.25"),
            high=Decimal("152.50"),
            low=Decimal("149.75"),
            close=Decimal("151.00"),
            volume=1000000
        )
        self.assertEqual(data.open, Decimal("150.25"))
        self.assertEqual(data.volume, 1000000)
    
    def test_negative_open_price(self):
        """Test validation fails for negative open price"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("-150.25"),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=1000000
            )
    
    def test_negative_high_price(self):
        """Test validation fails for negative high price"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("150.25"),
                high=Decimal("-152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=1000000
            )
    
    def test_negative_low_price(self):
        """Test validation fails for negative low price"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("150.25"),
                high=Decimal("152.50"),
                low=Decimal("-149.75"),
                close=Decimal("151.00"),
                volume=1000000
            )
    
    def test_negative_close_price(self):
        """Test validation fails for negative close price"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("150.25"),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("-151.00"),
                volume=1000000
            )
    
    def test_zero_price(self):
        """Test validation fails for zero price"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("0"),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=1000000
            )
    
    def test_negative_volume(self):
        """Test validation fails for negative volume"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("150.25"),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=-1000000
            )
    
    def test_zero_volume(self):
        """Test validation fails for zero volume"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("150.25"),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=0
            )
    
    def test_high_less_than_low(self):
        """Test validation fails when high < low"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("150.25"),
                high=Decimal("149.00"),  # Lower than low
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=1000000
            )
    
    def test_missing_datetime(self):
        """Test validation fails for missing datetime"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                open=Decimal("150.25"),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=1000000
            )
    
    def test_missing_open(self):
        """Test validation fails for missing open"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=1000000
            )
    
    def test_invalid_decimal_places(self):
        """Test price with correct decimal places"""
        # Should work with 2 decimal places
        data = TickerDataCreate(
            datetime=datetime(2024, 1, 1),
            open=Decimal("150.25"),
            high=Decimal("152.50"),
            low=Decimal("149.75"),
            close=Decimal("151.00"),
            volume=1000000
        )
        self.assertEqual(data.open, Decimal("150.25"))
    
    def test_valid_high_equals_low(self):
        """Test validation passes when high equals low"""
        data = TickerDataCreate(
            datetime=datetime(2024, 1, 1),
            open=Decimal("150.00"),
            high=Decimal("150.00"),
            low=Decimal("150.00"),
            close=Decimal("150.00"),
            volume=1000000
        )
        self.assertEqual(data.high, data.low)
    
    def test_volume_as_integer(self):
        """Test volume must be integer"""
        with self.assertRaises(ValidationError):
            TickerDataCreate(
                datetime=datetime(2024, 1, 1),
                open=Decimal("150.25"),
                high=Decimal("152.50"),
                low=Decimal("149.75"),
                close=Decimal("151.00"),
                volume=1000000.5  # Float not allowed
            )
    
    def test_large_volume(self):
        """Test validation with very large volume"""
        data = TickerDataCreate(
            datetime=datetime(2024, 1, 1),
            open=Decimal("150.25"),
            high=Decimal("152.50"),
            low=Decimal("149.75"),
            close=Decimal("151.00"),
            volume=999999999
        )
        self.assertEqual(data.volume, 999999999)
    
    def test_very_small_prices(self):
        """Test validation with very small but positive prices"""
        data = TickerDataCreate(
            datetime=datetime(2024, 1, 1),
            open=Decimal("0.01"),
            high=Decimal("0.02"),
            low=Decimal("0.01"),
            close=Decimal("0.01"),
            volume=1000000
        )
        self.assertEqual(data.open, Decimal("0.01"))

if __name__ == '__main__':
    unittest.main()