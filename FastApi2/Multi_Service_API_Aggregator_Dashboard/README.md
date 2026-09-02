# Multi-Service API Aggregator Dashboard

A FastAPI backend with frontend dashboard aggregating data from Weather, Crypto, and News APIs.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

## Access
- Dashboard: http://localhost:8000/static/index.html
- API Docs: http://localhost:8000/docs

## Endpoints
- `GET /weather/{city}` - Weather data
- `GET /crypto?coins=bitcoin,ethereum` - Crypto prices
- `GET /news?category=general&country=us` - News headlines

## Environment Variables
Create `.env` file:
```
OPENWEATHER_API_KEY=your_key
NEWS_API_KEY=your_key
```
