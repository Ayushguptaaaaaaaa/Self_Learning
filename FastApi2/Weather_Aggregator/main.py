from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
import asyncio

load_dotenv()

app=FastAPI()

API_KEY=os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float

class ForecastDay(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    description: str

class ForecastResponse(BaseModel):
    city: str
    forecast: list[ForecastDay]

@app.get("/weather/{city}", response_model=WeatherResponse)
async  def get_weather(city: str):
    url=f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code==404:
        raise  HTTPException(status_code=404, detail="City not found")
    if response.status_code!=200:
        raise  HTTPException(status_code=500, detail= "Failed to fetch weather Data")

    data=response.json()

    return WeatherResponse(
        city=data["name"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        description=data["weather"][0]["description"],
        wind_speed=data["wind"]["speed"]
    )

@app.get("/forecast/{city}", response_model=ForecastResponse)
async def get_forecast(city: str):
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast data")
    
    data = response.json()
    

    daily_forecasts = {}
    
    for item in data["list"]:

        date = item["dt_txt"].split()[0]
        
        if date not in daily_forecasts:
            daily_forecasts[date] = {
                "temps": [],
                "description": item["weather"][0]["description"]
            }
        
        daily_forecasts[date]["temps"].append(item["main"]["temp"])
    
    forecast_list = []
    for date, info in daily_forecasts.items():
        forecast_list.append(ForecastDay(
            date=date,
            temp_max=max(info["temps"]),
            temp_min=min(info["temps"]),
            description=info["description"]
        ))
    
    # Return ForecastResponse
    return ForecastResponse(
        city=data["city"]["name"],
        forecast=forecast_list
    )

@app.get("/compare")
async def compare_weather(city1: str, city2: str):

    url1 = f"{BASE_URL}/weather?q={city1}&appid={API_KEY}&units=metric"
    url2 = f"{BASE_URL}/weather?q={city2}&appid={API_KEY}&units=metric"
    
    
    async with httpx.AsyncClient() as client:
        response1, response2 = await asyncio.gather(
            client.get(url1),
            client.get(url2)
        )
    
    
    if response1.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city1}' not found")
    if response1.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data for '{city1}'")
    
    
    if response2.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city2}' not found")
    if response2.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data for '{city2}'")
    
    
    data1 = response1.json()
    data2 = response2.json()
    

    return {
        "city1": {
            "city": data1["name"],
            "temperature": data1["main"]["temp"],
            "feels_like": data1["main"]["feels_like"],
            "humidity": data1["main"]["humidity"],
            "description": data1["weather"][0]["description"],
            "wind_speed": data1["wind"]["speed"]
        },
        "city2": {
            "city": data2["name"],
            "temperature": data2["main"]["temp"],
            "feels_like": data2["main"]["feels_like"],
            "humidity": data2["main"]["humidity"],
            "description": data2["weather"][0]["description"],
            "wind_speed": data2["wind"]["speed"]
        }
    }