"""API route definitions."""

import logging
from datetime import datetime
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from ..models.schemas import (
    WeatherRequest, WeatherResponse, VoiceQueryRequest, VoiceQueryResponse,
    PredictionResponse, MarketPriceItem, PredictionHistory, WeatherHistory,
    AppStats, HealthResponse, APIInfo
)
from ..services.weather_service import weather_service
from ..services.market_service import market_service
from ..services.disease_service import disease_service
from ..services.voice_service import voice_service
from ..database.database import db_manager
from ..config import settings

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

@router.get("/", response_model=APIInfo)
async def root():
    """Root endpoint with API information."""
    return APIInfo(
        message='GrowWise API is running',
        version=settings.VERSION,
        features=['Disease Detection', 'Weather Data', 'Market Prices', 'Voice Assistant'],
        health={
            'model_loaded': disease_service.is_model_available(),
            'database_exists': db_manager is not None
        }
    )

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status='healthy',
        timestamp=datetime.now(),
        model_loaded=disease_service.is_model_available(),
        database_exists=db_manager is not None
    )

@router.post("/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest, background_tasks: BackgroundTasks):
    """Get weather data for a location."""
    try:
        weather_data = weather_service.get_weather_data(
            city=request.city,
            lat=request.lat,
            lon=request.lon
        )
        
        # Save to database in background
        background_tasks.add_task(db_manager.save_weather_data, weather_data)
        
        return WeatherResponse(**weather_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in weather endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/prices", response_model=List[MarketPriceItem])
async def get_market_prices(background_tasks: BackgroundTasks):
    """Get current market prices."""
    try:
        prices = market_service.get_market_prices()
        
        # Save to database in background
        background_tasks.add_task(db_manager.save_market_prices, prices)
        
        return [MarketPriceItem(**price) for price in prices]
        
    except Exception as e:
        logger.error(f"Error fetching market prices: {e}")
        raise HTTPException(status_code=500, detail="Error fetching market prices")

@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(...), 
    background_tasks: BackgroundTasks = None
):
    """Predict plant disease from uploaded image."""
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Make prediction
        result = disease_service.predict_disease(image_bytes)
        
        # Save to database in background
        if background_tasks:
            background_tasks.add_task(
                db_manager.save_prediction,
                result['disease'],
                result['confidence'],
                result['treatment']
            )
        
        return PredictionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in prediction endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error processing image")

@router.post("/voice-query", response_model=VoiceQueryResponse)
async def handle_voice_query(
    request: VoiceQueryRequest, 
    background_tasks: BackgroundTasks
):
    """Handle voice query from user."""
    try:
        response = voice_service.process_query(request.query)
        
        # Save query to database in background
        background_tasks.add_task(
            db_manager.save_voice_query,
            request.query,
            response
        )
        
        return VoiceQueryResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error processing voice query: {e}")
        raise HTTPException(status_code=500, detail="Error processing voice query")

@router.get("/history/predictions", response_model=List[PredictionHistory])
async def get_prediction_history(limit: int = 10):
    """Get recent disease prediction history."""
    try:
        history = db_manager.get_prediction_history(limit)
        return [PredictionHistory(**item) for item in history]
        
    except Exception as e:
        logger.error(f"Error fetching prediction history: {e}")
        return []

@router.get("/history/weather", response_model=List[WeatherHistory])
async def get_weather_history(limit: int = 10):
    """Get recent weather queries history."""
    try:
        history = db_manager.get_weather_history(limit)
        return [WeatherHistory(**item) for item in history]
        
    except Exception as e:
        logger.error(f"Error fetching weather history: {e}")
        return []

@router.get("/stats", response_model=AppStats)
async def get_app_stats():
    """Get application usage statistics."""
    try:
        stats = db_manager.get_app_stats()
        return AppStats(**stats)
        
    except Exception as e:
        logger.error(f"Error fetching app stats: {e}")
        return AppStats(
            total_predictions=0,
            weather_queries=0,
            voice_queries=0,
            common_diseases=[]
        )

@router.get("/help")
async def get_help():
    """Get help information about the API."""
    return voice_service.get_help_response()