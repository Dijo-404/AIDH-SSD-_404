"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class WeatherRequest(BaseModel):
    """Request model for weather data."""
    lat: Optional[float] = Field(None, description="Latitude coordinate")
    lon: Optional[float] = Field(None, description="Longitude coordinate")
    city: Optional[str] = Field(None, description="City name")

class WeatherResponse(BaseModel):
    """Response model for weather data."""
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    country: str

class VoiceQueryRequest(BaseModel):
    """Request model for voice queries."""
    query: str = Field(..., description="User's voice query")

class VoiceQueryResponse(BaseModel):
    """Response model for voice queries."""
    response: str = Field(..., description="AI assistant response")

class PredictionResponse(BaseModel):
    """Response model for disease predictions."""
    disease: str = Field(..., description="Detected disease class")
    confidence: float = Field(..., description="Prediction confidence percentage")
    treatment: str = Field(..., description="Treatment recommendation")
    formatted_name: str = Field(..., description="Human-readable disease name")

class MarketPriceItem(BaseModel):
    """Model for individual market price item."""
    category: str = Field(..., description="Product category (Vegetable/Fruit)")
    name: str = Field(..., description="Product name")
    price: str = Field(..., description="Price range or value")

class HistoryItem(BaseModel):
    """Base model for history items."""
    timestamp: datetime

class PredictionHistory(HistoryItem):
    """Model for prediction history."""
    disease: str
    confidence: float
    treatment: str

class WeatherHistory(HistoryItem):
    """Model for weather history."""
    city: str
    temperature: float
    description: str

class AppStats(BaseModel):
    """Model for application statistics."""
    total_predictions: int
    weather_queries: int
    voice_queries: int
    common_diseases: List[Dict[str, Any]]

class HealthResponse(BaseModel):
    """Model for health check response."""
    model_config = {"protected_namespaces": ()}
    
    status: str
    timestamp: datetime
    model_loaded: bool
    database_exists: bool

class APIInfo(BaseModel):
    """Model for API information."""
    model_config = {"protected_namespaces": ()}
    
    message: str
    version: str
    features: List[str]
    health: Dict[str, bool]