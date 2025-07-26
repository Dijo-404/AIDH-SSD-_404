"""Weather service for fetching weather data."""

import requests
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "7a695b51212a8a83fa11b8fab774eb02")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_data(
        self, 
        city: Optional[str] = None, 
        lat: Optional[float] = None, 
        lon: Optional[float] = None
    ) -> Dict:
        """
        Get weather data from OpenWeatherMap API.
        
        Args:
            city: City name
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            Dictionary containing weather data
        """
        if lat is not None and lon is not None:
            params = {
                'lat': lat, 
                'lon': lon, 
                'appid': self.api_key, 
                'units': 'metric'
            }
        elif city:
            params = {
                'q': city, 
                'appid': self.api_key, 
                'units': 'metric'
            }
        else:
            raise ValueError("Either city name or coordinates are required")

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].title(),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'country': data['sys']['country']
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API request error: {e}")
            raise Exception("Weather service is currently unavailable")
        except KeyError as e:
            logger.error(f"Weather data parsing error: {e}")
            raise Exception("Weather data not found for the specified location")
        except Exception as e:
            logger.error(f"Unexpected weather service error: {e}")
            raise Exception("Internal server error while fetching weather data")

# Global weather service instance
weather_service = WeatherService()
