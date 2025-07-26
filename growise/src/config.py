"""Configuration settings for the GrowWise API."""

import os
from typing import Dict, Any

class Settings:
    """Application settings and configuration."""
    
    # API Configuration
    TITLE = "GrowWise API"
    DESCRIPTION = "Smart Farming Assistant API with Disease Detection, Weather, and Market Prices"
    VERSION = "1.0.0"
    
    # External API Keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "7a695b51212a8a83fa11b8fab774eb02")
    
    # File Paths
    MODEL_PATH = os.getenv("MODEL_PATH", "/home/dijo/dev_hack/Plant-Disease-Detection/Model/plant_disease_model_1_latest.pt")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "growwise_app.db")
    
    # CORS Settings
    CORS_ORIGINS = ["*"]
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # Selenium Configuration
    CHROME_OPTIONS = [
        '--headless=new',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-extensions',
        '--disable-logging',
        '--silent'
    ]
    
    # Market Price URLs
    MARKET_URLS = {
        'Vegetable': 'https://www.livechennai.com/Vegetable_price_chennai.asp',
        'Fruit': 'https://www.livechennai.com/Fruits_price_chennai.asp'
    }

settings = Settings()