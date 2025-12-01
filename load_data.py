#!/usr/bin/env python3
"""
Script to load data from Google Sheets into the database
Usage: python load_data.py
"""

import asyncio
import pandas as pd
from datetime import datetime
from prisma import Prisma
import httpx

async def load_data_from_csv():
    """Load data from Google Sheets CSV export"""
    
    # Initialize Prisma client
    db = Prisma()
    await db.connect()
    
    try:
        # Download the CSV from Google Sheets
        # Convert the sharing link to export format
        sheet_url = "https://docs.google.com/spreadsheets/d/1-rIkEb94tZ69FvsjXnfkVETYu6rftF-8/export?format=csv"
        
        print("Downloading data from Google Sheets...")
        async with httpx.AsyncClient() as client:
            response = await client.get(sheet_url)
            
        # Save to temporary file
        with open('temp_data.csv', 'wb') as f:
            f.write(response.content)
        
        # Read CSV
        df = pd.read_csv('temp_data.csv')
        print(f"Loaded {len(df)} rows from CSV")
        
        # Display first few rows
        print("\nFirst few rows:")
        print(df.head())
        
        # Convert and insert data
        print("\nInserting data into database...")
        for idx, row in df.iterrows():
            try:
                # Parse datetime - adjust column name based on actual CSV
                # Common column names: 'datetime', 'timestamp', 'date', 'time'
                dt = pd.to_datetime(row['datetime'])  # Adjust column name if needed
                
                await db.tickerdata.create(
                    data={
                        'datetime': dt,
                        'open': float(row['open']),
                        'high': float(row['high']),
                        'low': float(row['low']),
                        'close': float(row['close']),
                        'volume': int(row['volume'])
                    }
                )
                
                if (idx + 1) % 100 == 0:
                    print(f"Inserted {idx + 1} records...")
                    
            except Exception as e:
                print(f"Error inserting row {idx}: {e}")
                print(f"Row data: {row}")
                continue
        
        print(f"\nSuccessfully loaded {len(df)} records into database")
        
        # Verify data
        count = await db.tickerdata.count()
        print(f"Total records in database: {count}")
        
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(load_data_from_csv())