from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal
from typing import List

class TickerDataCreate(BaseModel):
    datetime: datetime
    open: Decimal = Field(gt=0, decimal_places=2)
    high: Decimal = Field(gt=0, decimal_places=2)
    low: Decimal = Field(gt=0, decimal_places=2)
    close: Decimal = Field(gt=0, decimal_places=2)
    volume: int = Field(gt=0)

    @field_validator('high')
    @classmethod
    def high_must_be_highest(cls, v, info):
        if 'low' in info.data and v < info.data['low']:
            raise ValueError('high must be >= low')
        return v

    @field_validator('low')
    @classmethod
    def low_must_be_lowest(cls, v, info):
        if 'high' in info.data and v > info.data['high']:
            raise ValueError('low must be <= high')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "datetime": "2024-01-01T09:30:00",
                "open": 150.25,
                "high": 152.50,
                "low": 149.75,
                "close": 151.00,
                "volume": 1000000
            }
        }

class TickerDataResponse(BaseModel):
    id: int
    datetime: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int

    class Config:
        from_attributes = True

class BulkDataCreate(BaseModel):
    data: List[TickerDataCreate]

class StrategyPerformance(BaseModel):
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_return: float
    signals: List[dict]