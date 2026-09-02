from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional, List

class WeatherData(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    wind_speed: float

class WeatherResponse(BaseModel):
    status: str
    data: WeatherData

class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str
    city: str


class NewsArticle(BaseModel):
    title: str  
    description: Optional[str] = None  
    url: str  
    source: str  
    published_at: str  
    author: Optional[str] = None  
class NewsResponse(BaseModel):
    status: str  
    category: str  
    country: str  
    total_results: int  
    articles: List[NewsArticle]  


class CryptoData(BaseModel):
    name: str  
    current_price: float  
    price_change_24h: Optional[float] = None  


class CryptoResponse(BaseModel):
    status: str 
    coins: List[CryptoData] 