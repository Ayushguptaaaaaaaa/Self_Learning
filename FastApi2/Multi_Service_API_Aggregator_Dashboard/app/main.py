from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
from app.config import settings
from app.schemas import WeatherResponse, WeatherData, CryptoResponse, CryptoData, NewsResponse, NewsArticle

app = FastAPI()

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    """
    Get current weather for a city
    """
    # OpenWeatherMap API URL
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request
    params = {
        "q": city,
        "appid": settings.openweather_api_key,
        "units": "metric"  # Celsius
    }
    
    # Make HTTP request to external API
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise error if status code is 4xx or 5xx
            
            # Parse JSON response
            data = response.json()
            
            # Extract relevant weather data
            weather_data = WeatherData(
                city=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                description=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"]
            )
            
            return WeatherResponse(
                status="success",
                data=weather_data
            )
            # Catch timeout - API doesn't respond within 10 seconds
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,  # Gateway Timeout
                detail="Weather service is taking too long to respond. Please try again later."
            )
    
        except httpx.RequestError:
            raise HTTPException(
                status_code=502,  # Bad Gateway
                detail="Unable to reach weather service. Check your internet connection."
            )
    
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPException(
                    status_code=500,  # Internal - your API key misconfiguration
                    detail="Invalid API key. Please check your OpenWeather API key."
                )
            elif e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,  # Not Found
                    detail=f"City '{city}' not found. Please check the spelling."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Weather service returned error: {e.response.status_code}"
                )
    
    # Catch KeyError - unexpected response structure
        except KeyError as e:
            raise HTTPException(
                status_code=500,  # Internal Server Error
                detail=f"Unexpected data structure from weather service: missing {str(e)}"
            )


@app.get("/crypto", response_model=CryptoResponse)
async def get_crypto_prices(coins: str = "bitcoin,ethereum"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coins,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            crypto_list = [
                CryptoData(
                    name=coin_name,
                    current_price=coin_data["usd"],
                    price_change_24h=coin_data.get("usd_24h_change")
                )
                for coin_name, coin_data in data.items()
            ]

            return CryptoResponse(status="success", coins=crypto_list)

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Crypto service is taking too long to respond.")
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Unable to reach crypto service.")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise HTTPException(status_code=429, detail="CoinGecko rate limit reached. Try again later.")
            else:
                raise HTTPException(status_code=500, detail=f"Crypto service error: {e.response.status_code}")
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected data from crypto service: missing {str(e)}")


@app.get("/news", response_model=NewsResponse)
async def get_news(category: str = "general", country: str = "us"):
    """
    Get top news headlines by category and country
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "country": country,
        "apiKey": settings.news_api_key
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            articles = [
                NewsArticle(
                    title=article["title"],
                    description=article.get("description"),
                    url=article["url"],
                    source=article["source"]["name"],
                    published_at=article["publishedAt"],
                    author=article.get("author")
                )
                for article in data.get("articles", [])
            ]

            return NewsResponse(
                status="success",
                category=category,
                country=country,
                total_results=data.get("totalResults", 0),
                articles=articles
            )

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="News service is taking too long to respond.")
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Unable to reach news service.")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPException(status_code=500, detail="Invalid News API key.")
            elif e.response.status_code == 429:
                raise HTTPException(status_code=429, detail="News API rate limit reached. Try again later.")
            else:
                raise HTTPException(status_code=500, detail=f"News service error: {e.response.status_code}")
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected data from news service: missing {str(e)}")