"""Voice query processing service."""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class VoiceAssistantService:
    """Service for processing voice queries and generating responses."""
    
    def __init__(self):
        self.query_patterns = {
            'weather': ['weather', 'temperature', 'rain', 'climate', 'forecast', 'sunny', 'cloudy'],
            'prices': ['price', 'cost', 'market', 'sell', 'buy', 'rate', 'expensive', 'cheap'],
            'disease': ['disease', 'sick', 'problem', 'leaf', 'plant', 'crop', 'infection', 'pest'],
            'fertilizer': ['fertilizer', 'nutrient', 'soil', 'compost', 'manure', 'nitrogen'],
            'cultivation': ['seed', 'planting', 'growing', 'cultivation', 'harvest', 'farming']
        }
        
        self.responses = {
            'weather': "To get weather information, please provide your city name or enable location access in the Weather tab.",
            'prices': "Check the Market Prices tab for current rates of vegetables and fruits in your area.",
            'disease': "For plant disease detection, please take a clear photo of the affected plant leaves and upload it in the Disease Detection tab.",
            'fertilizer': "For soil and fertilizer advice, consider getting a soil test and consult with local agricultural experts. Organic compost is generally recommended for most crops.",
            'cultivation': "For seed and cultivation advice, check with your local agricultural extension office for region-specific recommendations based on your soil type and climate.",
            'greeting': "Hello! I'm your GrowWise assistant. I can help you with weather information, market prices, plant disease detection, and general farming queries.",
            'default': "I can help you with weather information, market prices, plant disease detection, and general farming queries. Please be more specific about what you'd like to know!"
        }
    
    def process_query(self, query: str) -> str:
        """
        Process voice query and return appropriate response.
        
        Args:
            query: User's voice query
            
        Returns:
            AI assistant response
        """
        query_lower = query.lower().strip()
        
        # Handle greetings
        if self._is_greeting(query_lower):
            return self.responses['greeting']
        
        # Check for specific query types
        for category, keywords in self.query_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                return self.responses[category]
        
        # Default response
        return self.responses['default']
    
    def _is_greeting(self, query: str) -> bool:
        """Check if the query is a greeting."""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(greeting in query for greeting in greetings)
    
    def get_help_response(self) -> Dict[str, List[str]]:
        """Get structured help information."""
        return {
            'features': [
                'Weather Information - Get current weather for any location',
                'Market Prices - Check latest vegetable and fruit prices',
                'Disease Detection - Upload plant photos for disease diagnosis',
                'Voice Assistant - Ask questions about farming'
            ],
            'sample_queries': [
                'What is the weather like today?',
                'Show me tomato prices',
                'My plant leaves are turning yellow',
                'What fertilizer should I use for corn?'
            ]
        }

# Global voice service instance
voice_service = VoiceAssistantService()