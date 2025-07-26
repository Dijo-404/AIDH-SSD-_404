"""Market price service with cached data."""

import json
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class MarketPriceService:
    """Service for providing market price data."""
    
    def __init__(self):
        self.cache_file = "data/market_prices.json"
        self._initialize_prices()
    
    def _initialize_prices(self):
        """Initialize market prices with default data."""
        default_prices = [
            {'category': 'Vegetable', 'name': 'Onion', 'price': '₹30-40/kg'},
            {'category': 'Vegetable', 'name': 'Tomato', 'price': '₹25-35/kg'},
            {'category': 'Vegetable', 'name': 'Potato', 'price': '₹20-25/kg'},
            {'category': 'Vegetable', 'name': 'Carrot', 'price': '₹35-45/kg'},
            {'category': 'Vegetable', 'name': 'Cabbage', 'price': '₹15-20/kg'},
            {'category': 'Vegetable', 'name': 'Cauliflower', 'price': '₹25-30/kg'},
            {'category': 'Vegetable', 'name': 'Green Beans', 'price': '₹40-50/kg'},
            {'category': 'Vegetable', 'name': 'Okra (Ladyfinger)', 'price': '₹30-40/kg'},
            {'category': 'Vegetable', 'name': 'Brinjal (Eggplant)', 'price': '₹25-35/kg'},
            {'category': 'Vegetable', 'name': 'Bell Pepper', 'price': '₹50-60/kg'},
            {'category': 'Fruit', 'name': 'Apple', 'price': '₹120-150/kg'},
            {'category': 'Fruit', 'name': 'Banana', 'price': '₹40-50/dozen'},
            {'category': 'Fruit', 'name': 'Orange', 'price': '₹60-80/kg'},
            {'category': 'Fruit', 'name': 'Mango', 'price': '₹80-120/kg'},
            {'category': 'Fruit', 'name': 'Grapes', 'price': '₹100-140/kg'},
            {'category': 'Fruit', 'name': 'Papaya', 'price': '₹25-35/kg'},
            {'category': 'Fruit', 'name': 'Watermelon', 'price': '₹15-20/kg'},
            {'category': 'Fruit', 'name': 'Pineapple', 'price': '₹30-40/piece'},
            {'category': 'Fruit', 'name': 'Pomegranate', 'price': '₹150-200/kg'},
            {'category': 'Fruit', 'name': 'Guava', 'price': '₹40-60/kg'}
        ]
        
        # Create the cache file if it doesn't exist
        if not os.path.exists(self.cache_file):
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            try:
                with open(self.cache_file, 'w') as f:
                    json.dump(default_prices, f, indent=2)
                logger.info("Market prices cache initialized")
            except Exception as e:
                logger.error(f"Error initializing market prices: {e}")
    
    def get_market_prices(self, category: str = 'all') -> List[Dict[str, str]]:
        """
        Get market prices, optionally filtered by category.
        
        Args:
            category: Filter by category ('Vegetable', 'Fruit', or 'all')
            
        Returns:
            List of price dictionaries
        """
        try:
            with open(self.cache_file, 'r') as f:
                prices = json.load(f)
            
            if category.lower() == 'all':
                return prices
            else:
                return [p for p in prices if p['category'].lower() == category.lower()]
                
        except Exception as e:
            logger.error(f"Error loading market prices: {e}")
            # Return fallback data
            return [
                {'category': 'Vegetable', 'name': 'Onion', 'price': '₹30-40/kg'},
                {'category': 'Vegetable', 'name': 'Tomato', 'price': '₹25-35/kg'},
                {'category': 'Fruit', 'name': 'Apple', 'price': '₹120-150/kg'},
                {'category': 'Fruit', 'name': 'Banana', 'price': '₹40-50/dozen'}
            ]

# Global market service instance
market_service = MarketPriceService()
