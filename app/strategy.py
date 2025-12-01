from typing import List, Dict
from decimal import Decimal
import pandas as pd

class MovingAverageCrossoverStrategy:
    """
    Simple Moving Average Crossover Strategy
    - Buy signal: Short MA crosses above Long MA
    - Sell signal: Short MA crosses below Long MA
    """
    
    def __init__(self, short_window: int = 10, long_window: int = 20):
        self.short_window = short_window
        self.long_window = long_window
    
    def calculate_moving_average(self, prices: List[float], window: int) -> List[float]:
        """Calculate simple moving average"""
        if len(prices) < window:
            return [None] * len(prices)
        
        ma = []
        for i in range(len(prices)):
            if i < window - 1:
                ma.append(None)
            else:
                ma.append(sum(prices[i-window+1:i+1]) / window)
        return ma
    
    def generate_signals(self, data: List[Dict]) -> List[Dict]:
        """Generate buy/sell signals based on MA crossover"""
        if len(data) < self.long_window:
            return []
        
        # Convert to pandas for easier calculation
        df = pd.DataFrame(data)
        df['close'] = df['close'].astype(float)
        
        # Calculate moving averages
        df['short_ma'] = df['close'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        signals = []
        position = None  # None, 'long', or 'short'
        
        for i in range(self.long_window, len(df)):
            prev_short = df['short_ma'].iloc[i-1]
            prev_long = df['long_ma'].iloc[i-1]
            curr_short = df['short_ma'].iloc[i]
            curr_long = df['long_ma'].iloc[i]
            
            # Skip if any value is NaN
            if pd.isna(prev_short) or pd.isna(prev_long) or pd.isna(curr_short) or pd.isna(curr_long):
                continue
            
            signal = None
            
            # Buy signal: short MA crosses above long MA
            if prev_short <= prev_long and curr_short > curr_long and position != 'long':
                signal = 'BUY'
                position = 'long'
            
            # Sell signal: short MA crosses below long MA
            elif prev_short >= prev_long and curr_short < curr_long and position == 'long':
                signal = 'SELL'
                position = None
            
            if signal:
                signals.append({
                    'datetime': str(df['datetime'].iloc[i]),
                    'signal': signal,
                    'price': float(df['close'].iloc[i]),
                    'short_ma': float(curr_short),
                    'long_ma': float(curr_long)
                })
        
        return signals
    
    def calculate_performance(self, signals: List[Dict]) -> Dict:
        """Calculate strategy performance metrics"""
        if len(signals) < 2:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_return': 0.0
            }
        
        trades = []
        buy_price = None
        
        for signal in signals:
            if signal['signal'] == 'BUY':
                buy_price = signal['price']
            elif signal['signal'] == 'SELL' and buy_price is not None:
                profit = signal['price'] - buy_price
                trades.append(profit)
                buy_price = None
        
        total_trades = len(trades)
        winning_trades = sum(1 for t in trades if t > 0)
        losing_trades = sum(1 for t in trades if t < 0)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        total_return = sum(trades)
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'total_return': round(total_return, 2)
        }