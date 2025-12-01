from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List
import logging

from app.database import db, connect_db, disconnect_db
from app.models import (
    TickerDataCreate, 
    TickerDataResponse, 
    BulkDataCreate,
    StrategyPerformance
)
from app.strategy import MovingAverageCrossoverStrategy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Connecting to database...")
    await connect_db()
    logger.info("Database connected successfully")
    yield
    # Shutdown
    logger.info("Disconnecting from database...")
    await disconnect_db()
    logger.info("Database disconnected")

app = FastAPI(
    title="Trading API",
    description="API for storing and analyzing ticker data with moving average strategy",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Trading API",
        "endpoints": {
            "GET /data": "Fetch all ticker records",
            "POST /data": "Add new ticker record",
            "POST /data/bulk": "Add multiple ticker records",
            "GET /strategy/performance": "Get trading strategy performance"
        }
    }

@app.get("/data", response_model=List[TickerDataResponse])
async def get_all_data():
    """
    Fetch all ticker data from the database.
    
    Returns:
        List of all ticker records
    """
    try:
        records = await db.tickerdata.find_many(
            order={'datetime': 'asc'}
        )
        return records
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching data: {str(e)}"
        )

@app.post("/data", response_model=TickerDataResponse, status_code=status.HTTP_201_CREATED)
async def create_data(data: TickerDataCreate):
    """
    Add a new ticker record to the database.
    
    Args:
        data: Ticker data to be added
        
    Returns:
        Created ticker record
    """
    try:
        record = await db.tickerdata.create(
            data={
                'datetime': data.datetime,
                'open': data.open,
                'high': data.high,
                'low': data.low,
                'close': data.close,
                'volume': data.volume
            }
        )
        return record
    except Exception as e:
        logger.error(f"Error creating data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating data: {str(e)}"
        )

@app.post("/data/bulk", status_code=status.HTTP_201_CREATED)
async def create_bulk_data(bulk_data: BulkDataCreate):
    """
    Add multiple ticker records to the database.
    
    Args:
        bulk_data: List of ticker data to be added
        
    Returns:
        Success message with count
    """
    try:
        created_records = []
        for data in bulk_data.data:
            record = await db.tickerdata.create(
                data={
                    'datetime': data.datetime,
                    'open': data.open,
                    'high': data.high,
                    'low': data.low,
                    'close': data.close,
                    'volume': data.volume
                }
            )
            created_records.append(record)
        
        return {
            "message": f"Successfully created {len(created_records)} records",
            "count": len(created_records)
        }
    except Exception as e:
        logger.error(f"Error creating bulk data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating bulk data: {str(e)}"
        )

@app.get("/strategy/performance", response_model=StrategyPerformance)
async def get_strategy_performance(short_window: int = 10, long_window: int = 20):
    """
    Calculate and return Moving Average Crossover Strategy performance.
    
    Args:
        short_window: Period for short moving average (default: 10)
        long_window: Period for long moving average (default: 20)
        
    Returns:
        Strategy performance metrics and signals
    """
    try:
        # Fetch all data
        records = await db.tickerdata.find_many(
            order={'datetime': 'asc'}
        )
        
        if len(records) < long_window:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient data. Need at least {long_window} records."
            )
        
        # Convert to list of dicts
        data = [
            {
                'datetime': record.datetime,
                'close': float(record.close)
            }
            for record in records
        ]
        
        # Initialize strategy
        strategy = MovingAverageCrossoverStrategy(short_window, long_window)
        
        # Generate signals
        signals = strategy.generate_signals(data)
        
        # Calculate performance
        performance = strategy.calculate_performance(signals)
        
        return {
            **performance,
            'signals': signals
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating strategy performance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating strategy: {str(e)}"
        )

@app.delete("/data", status_code=status.HTTP_200_OK)
async def delete_all_data():
    """
    Delete all ticker data (useful for testing).
    
    Returns:
        Success message with count
    """
    try:
        result = await db.tickerdata.delete_many()
        return {
            "message": f"Successfully deleted {result} records",
            "count": result
        }
    except Exception as e:
        logger.error(f"Error deleting data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting data: {str(e)}"
        )