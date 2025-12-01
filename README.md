# Trading API Assignment

A FastAPI application for storing and analyzing stock ticker data with a Moving Average Crossover trading strategy.

## Features

- PostgreSQL database with Prisma ORM
- RESTful API endpoints for CRUD operations
- Moving Average Crossover trading strategy
- Comprehensive unit tests
- Docker containerization
- Input validation with Pydantic

## Project Structure

```
trading-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── database.py          # Database connection
│   └── strategy.py          # Trading strategy
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # API tests
│   └── test_strategy.py     # Strategy tests
├── prisma/
│   └── schema.prisma        # Database schema
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── load_data.py             # Data loading script
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (if running locally)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd trading-api
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. **Using Docker (Recommended)**
```bash
# Build and start containers
docker-compose up -d

# Check logs
docker-compose logs -f api

# The API will be available at http://localhost:8000
```

4. **Manual Setup (Alternative)**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
prisma generate

# Push database schema
prisma db push

# Run the application
uvicorn app.main:app --reload
```

### Loading Data

```bash
# Load data from Google Sheets
python load_data.py
```

## API Endpoints

### 1. Root
```http
GET /
```
Returns API information and available endpoints.

### 2. Get All Data
```http
GET /data
```
Fetches all ticker records from the database.

**Response:**
```json
[
  {
    "id": 1,
    "datetime": "2024-01-01T09:30:00",
    "open": 150.25,
    "high": 152.50,
    "low": 149.75,
    "close": 151.00,
    "volume": 1000000
  }
]
```

### 3. Create Data
```http
POST /data
Content-Type: application/json

{
  "datetime": "2024-01-01T09:30:00",
  "open": 150.25,
  "high": 152.50,
  "low": 149.75,
  "close": 151.00,
  "volume": 1000000
}
```

**Response:**
```json
{
  "id": 1,
  "datetime": "2024-01-01T09:30:00",
  "open": 150.25,
  "high": 152.50,
  "low": 149.75,
  "close": 151.00,
  "volume": 1000000
}
```

### 4. Bulk Create
```http
POST /data/bulk
Content-Type: application/json

{
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
```

### 5. Strategy Performance
```http
GET /strategy/performance?short_window=10&long_window=20
```

**Response:**
```json
{
  "total_trades": 5,
  "winning_trades": 3,
  "losing_trades": 2,
  "win_rate": 60.0,
  "total_return": 25.50,
  "signals": [
    {
      "datetime": "2024-01-15T09:30:00",
      "signal": "BUY",
      "price": 150.25,
      "short_ma": 149.50,
      "long_ma": 148.75
    }
  ]
}
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m unittest tests.test_api
python -m unittest tests.test_strategy
```

## Trading Strategy

The application implements a **Moving Average Crossover Strategy**:

- **Short-term MA**: Default 10 periods
- **Long-term MA**: Default 20 periods

**Signals:**
- **BUY**: When short MA crosses above long MA
- **SELL**: When short MA crosses below long MA

**Performance Metrics:**
- Total number of trades
- Winning/losing trades
- Win rate percentage
- Total return

## Input Validation

The API validates:
- All prices must be positive
- High price must be ≥ Low price
- Volume must be positive
- Datetime must be valid ISO format
- All required fields must be present

## Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f api

# Rebuild containers
docker-compose up -d --build

# Access database
docker-compose exec db psql -U postgres -d trading_db
```

## Testing the API

### Using cURL

```bash
# Get all data
curl http://localhost:8000/data

# Create new record
curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": "2024-01-01T09:30:00",
    "open": 150.25,
    "high": 152.50,
    "low": 149.75,
    "close": 151.00,
    "volume": 1000000
  }'

# Get strategy performance
curl http://localhost:8000/strategy/performance?short_window=10&long_window=20
```

### Using the Interactive API Docs

Visit `http://localhost:8000/docs` for Swagger UI documentation with interactive testing.

## Database Schema

```prisma
model TickerData {
  id       Int      @id @default(autoincrement())
  datetime DateTime
  open     Decimal  @db.Decimal(10, 2)
  high     Decimal  @db.Decimal(10, 2)
  low      Decimal  @db.Decimal(10, 2)
  close    Decimal  @db.Decimal(10, 2)
  volume   Int

  @@index([datetime])
  @@map("ticker_data")
}
```

## Test Coverage

The project includes comprehensive unit tests covering:
- ✅ Input validation for all endpoints
- ✅ Moving average calculations
- ✅ Signal generation logic
- ✅ Performance metrics calculation
- ✅ Error handling
- ✅ Edge cases

Target: **80%+ code coverage**

## Technologies Used

- **FastAPI**: Modern web framework
- **Prisma**: Next-generation ORM
- **PostgreSQL**: Reliable database
- **Pydantic**: Data validation
- **Pandas**: Data analysis
- **Docker**: Containerization
- **Pytest**: Testing framework

## Common Issues & Solutions

### Issue: Database connection failed
```bash
# Check if database is running
docker-compose ps

# Restart database
docker-compose restart db
```

### Issue: Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use different port
```

### Issue: Prisma client not generated
```bash
prisma generate
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
