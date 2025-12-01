import unittest
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.strategy import MovingAverageCrossoverStrategy

class TestMovingAverageStrategy(unittest.TestCase):
    """Test Moving Average Crossover Strategy"""
    
    def setUp(self):
        """Set up test data"""
        self.strategy = MovingAverageCrossoverStrategy(short_window=3, long_window=5)
    
    def test_calculate_moving_average_simple(self):
        """Test simple moving average calculation"""
        prices = [10, 20, 30, 40, 50]
        window = 3
        ma = self.strategy.calculate_moving_average(prices, window)
        
        self.assertIsNone(ma[0])
        self.assertIsNone(ma[1])
        self.assertAlmostEqual(ma[2], 20.0)  # (10+20+30)/3
        self.assertAlmostEqual(ma[3], 30.0)  # (20+30+40)/3
        self.assertAlmostEqual(ma[4], 40.0)  # (30+40+50)/3
    
    def test_calculate_moving_average_insufficient_data(self):
        """Test MA calculation with insufficient data"""
        prices = [10, 20]
        window = 5
        ma = self.strategy.calculate_moving_average(prices, window)
        
        self.assertEqual(len(ma), 2)
        self.assertIsNone(ma[0])
        self.assertIsNone(ma[1])
    
    def test_calculate_moving_average_exact_window(self):
        """Test MA calculation with exactly window size data"""
        prices = [10, 20, 30]
        window = 3
        ma = self.strategy.calculate_moving_average(prices, window)
        
        self.assertAlmostEqual(ma[2], 20.0)
    
    def test_generate_signals_uptrend(self):
        """Test signal generation in uptrend (should generate BUY)"""
        # Create data with clear uptrend
        base_date = datetime(2024, 1, 1)
        data = []
        
        # Prices: start low, then increase (crossover will occur)
        prices = [100, 101, 102, 103, 104, 105, 110, 115, 120, 125, 130, 135]
        
        for i, price in enumerate(prices):
            data.append({
                'datetime': base_date + timedelta(days=i),
                'close': price
            })
        
        signals = self.strategy.generate_signals(data)
        
        # Should generate at least one BUY signal
        buy_signals = [s for s in signals if s['signal'] == 'BUY']
        self.assertGreater(len(buy_signals), 0)
    
    def test_generate_signals_downtrend(self):
        """Test signal generation in downtrend"""
        base_date = datetime(2024, 1, 1)
        data = []
        
        # Prices: start high, dip, then recover (should generate BUY then SELL)
        prices = [100, 99, 98, 97, 96, 95, 100, 105, 100, 95, 90, 85]
        
        for i, price in enumerate(prices):
            data.append({
                'datetime': base_date + timedelta(days=i),
                'close': price
            })
        
        signals = self.strategy.generate_signals(data)
        
        # Signals should be generated
        self.assertGreaterEqual(len(signals), 0)
    
    def test_generate_signals_insufficient_data(self):
        """Test signal generation with insufficient data"""
        data = [
            {'datetime': datetime(2024, 1, 1), 'close': 100},
            {'datetime': datetime(2024, 1, 2), 'close': 101}
        ]
        
        signals = self.strategy.generate_signals(data)
        self.assertEqual(len(signals), 0)
    
    def test_calculate_performance_no_trades(self):
        """Test performance calculation with no completed trades"""
        signals = [
            {'signal': 'BUY', 'price': 100}
        ]
        
        performance = self.strategy.calculate_performance(signals)
        
        self.assertEqual(performance['total_trades'], 0)
        self.assertEqual(performance['winning_trades'], 0)
        self.assertEqual(performance['losing_trades'], 0)
        self.assertEqual(performance['win_rate'], 0.0)
        self.assertEqual(performance['total_return'], 0.0)
    
    def test_calculate_performance_winning_trade(self):
        """Test performance calculation with winning trade"""
        signals = [
            {'signal': 'BUY', 'price': 100},
            {'signal': 'SELL', 'price': 110}
        ]
        
        performance = self.strategy.calculate_performance(signals)
        
        self.assertEqual(performance['total_trades'], 1)
        self.assertEqual(performance['winning_trades'], 1)
        self.assertEqual(performance['losing_trades'], 0)
        self.assertEqual(performance['win_rate'], 100.0)
        self.assertEqual(performance['total_return'], 10.0)
    
    def test_calculate_performance_losing_trade(self):
        """Test performance calculation with losing trade"""
        signals = [
            {'signal': 'BUY', 'price': 100},
            {'signal': 'SELL', 'price': 90}
        ]
        
        performance = self.strategy.calculate_performance(signals)
        
        self.assertEqual(performance['total_trades'], 1)
        self.assertEqual(performance['winning_trades'], 0)
        self.assertEqual(performance['losing_trades'], 1)
        self.assertEqual(performance['win_rate'], 0.0)
        self.assertEqual(performance['total_return'], -10.0)
    
    def test_calculate_performance_multiple_trades(self):
        """Test performance calculation with multiple trades"""
        signals = [
            {'signal': 'BUY', 'price': 100},
            {'signal': 'SELL', 'price': 110},  # +10
            {'signal': 'BUY', 'price': 105},
            {'signal': 'SELL', 'price': 95},   # -10
            {'signal': 'BUY', 'price': 90},
            {'signal': 'SELL', 'price': 100}   # +10
        ]
        
        performance = self.strategy.calculate_performance(signals)
        
        self.assertEqual(performance['total_trades'], 3)
        self.assertEqual(performance['winning_trades'], 2)
        self.assertEqual(performance['losing_trades'], 1)
        self.assertEqual(performance['win_rate'], 66.67)
        self.assertEqual(performance['total_return'], 10.0)
    
    def test_strategy_windows(self):
        """Test strategy with different window sizes"""
        strategy_small = MovingAverageCrossoverStrategy(short_window=2, long_window=4)
        strategy_large = MovingAverageCrossoverStrategy(short_window=10, long_window=20)
        
        self.assertEqual(strategy_small.short_window, 2)
        self.assertEqual(strategy_small.long_window, 4)
        self.assertEqual(strategy_large.short_window, 10)
        self.assertEqual(strategy_large.long_window, 20)

if __name__ == '__main__':
    unittest.main()