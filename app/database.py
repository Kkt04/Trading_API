from prisma import Prisma
from contextlib import asynccontextmanager
import os

# Database instance
db = Prisma()

async def connect_db():
    """Connect to the database"""
    if not db.is_connected():
        await db.connect()
    return db

async def disconnect_db():
    """Disconnect from the database"""
    if db.is_connected():
        await db.disconnect()

@asynccontextmanager
async def get_db():
    """Get database session"""
    await connect_db()
    try:
        yield db
    finally:
        pass  # Keep connection alive for app lifecycle