"""Voice query processing service."""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class VoiceAssistantService:
    """Service for processing voice queries and generating responses."""
    
    def __init__(self):
        self.query_patterns = {
            'weather': ['weather', 'temperature', 'rain', 'climate', 'forecast', 'sunny', 'cloudy', 'humidity'],
            'prices': ['price', 'cost', 'market', 'sell', 'buy', 'rate', 'expensive', 'cheap', 'rupees'],
            'disease': ['disease', 'sick', 'problem', 'leaf', 'plant', 'crop', 'infection', 'pest', 'spots', 'yellow'],
            'fertilizer': ['fertilizer', 'nutrient', 'soil', 'compost', 'manure', 'nitrogen', 'phosphorus', 'potassium'],
            'cultivation': ['seed', 'planting', 'growing', 'cultivation', 'harvest', 'farming', 'irrigation', 'water'],
            'pest': ['pest', 'insect', 'bug', 'caterpillar', 'aphid', 'mite', 'larvae'],
            'soil': ['soil', 'ph', 'acidity', 'alkaline', 'drainage', 'clay', 'sand', 'loam'],
            'season': ['season', 'monsoon', 'winter', 'summer', 'sowing', 'timing']
        }
        
        self.responses = {
            'weather': "🌤️ To get current weather information, use the Weather tab. Enter your city name or allow location access to get real-time weather data including temperature, humidity, and wind speed.",
            
            'prices': "💰 Check the Market Prices section for current rates of vegetables and fruits. You can filter by category to see specific produce prices in your area.",
            
            'disease': "🔬 For plant disease detection, use the Disease Detection tab. Take a clear photo of the affected plant leaves and upload it for AI-powered analysis and treatment recommendations.",
            
            'fertilizer': "🌱 For fertilizer recommendations: Use nitrogen-rich fertilizers for leafy growth, phosphorus for root development, and potassium for flowering. Consider organic compost and get soil testing for specific nutrient needs.",
            
            'cultivation': "🚜 Cultivation tips: Choose seeds based on your local climate and soil type. Ensure proper spacing, watering schedule, and crop rotation. Consult your local agricultural extension office for region-specific advice.",
            
            'pest': "🐛 For pest management: Use integrated pest management (IPM) approaches. Try neem oil, companion planting, and beneficial insects before chemical pesticides. Regular monitoring is key to early detection.",
            
            'soil': "🏔️ Soil health tips: Test your soil pH (6.0-7.0 is ideal for most crops). Improve drainage with organic matter. Add compost regularly to maintain soil structure and fertility.",
            
            'season': "📅 Seasonal farming: Plan crops according to local seasons. Monsoon is ideal for rice and sugarcane. Winter is good for wheat and vegetables. Summer crops include cotton and pulses.",
            
            'greeting': "👋 Hello! I'm your GrowWise farming assistant. I can help you with weather information, market prices, plant disease detection, and general farming guidance. What would you like to know?",
            
            'default': "🌾 I'm here to help with farming! I can assist with:\n• Weather information\n• Market prices\n• Plant disease detection\n• Soil and fertilizer advice\n• Pest management\n• Cultivation tips\n\nPlease ask me something specific about farming!"
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
        
        # Check for specific query types with confidence scoring
        matches = {}
        for category, keywords in self.query_patterns.items():
            match_count = sum(1 for keyword in keywords if keyword in query_lower)
            if match_count > 0:
                matches[category] = match_count
        
        # Return response for category with most matches
        if matches:
            best_category = max(matches, key=matches.get)
            return self.responses[best_category]
        
        # Default response
        return self.responses['default']
    
    def _is_greeting(self, query: str) -> bool:
        """Check if the query is a greeting."""
        greetings = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 
            'good evening', 'namaste', 'greetings', 'howdy'
        ]
        return any(greeting in query for greeting in greetings)
    
    def get_help_response(self) -> Dict[str, List[str]]:
        """Get structured help information."""
        return {
            'features': [
                '🌤️ Weather Information - Get current weather for any location',
                '💰 Market Prices - Check latest vegetable and fruit prices',
                '🔬 Disease Detection - Upload plant photos for disease diagnosis',
                '🎤 Voice Assistant - Ask questions about farming',
                '📊 Analytics - View usage statistics and history'
            ],
            'sample_queries': [
                'What is the weather like today?',
                'Show me tomato prices',
                'My plant leaves are turning yellow',
                'What fertilizer should I use for corn?',
                'How to manage pests in my crop?',
                'What is the best soil pH for vegetables?'
            ]
        }

# Global voice service instance
voice_service = VoiceAssistantService()
