"""Data models for GrowWise application."""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class DataManager:
    """Manages JSON-based data storage for serverless deployment."""
    
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Ensure all required JSON files exist."""
        files = {
            "predictions.json": [],
            "weather_cache.json": [],
            "voice_queries.json": [],
            "market_prices.json": []
        }
        
        for filename, default_data in files.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                self.save_json(filepath, default_data)
    
    def load_json(self, filepath: str) -> List[Dict]:
        """Load data from JSON file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_json(self, filepath: str, data: List[Dict]):
        """Save data to JSON file."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving to {filepath}: {e}")
    
    def save_prediction(self, disease: str, confidence: float, treatment: str):
        """Save disease prediction."""
        filepath = os.path.join(self.data_dir, "predictions.json")
        predictions = self.load_json(filepath)
        
        prediction = {
            "disease": disease,
            "confidence": confidence,
            "treatment": treatment,
            "timestamp": datetime.now().isoformat()
        }
        
        predictions.append(prediction)
        # Keep only last 100 predictions
        predictions = predictions[-100:]
        self.save_json(filepath, predictions)
    
    def save_weather_data(self, weather_data: Dict[str, Any]):
        """Save weather data."""
        filepath = os.path.join(self.data_dir, "weather_cache.json")
        cache = self.load_json(filepath)
        
        weather_entry = {
            **weather_data,
            "timestamp": datetime.now().isoformat()
        }
        
        cache.append(weather_entry)
        # Keep only last 50 weather queries
        cache = cache[-50:]
        self.save_json(filepath, cache)
    
    def save_voice_query(self, query: str, response: str):
        """Save voice query and response."""
        filepath = os.path.join(self.data_dir, "voice_queries.json")
        queries = self.load_json(filepath)
        
        query_entry = {
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        
        queries.append(query_entry)
        # Keep only last 100 queries
        queries = queries[-100:]
        self.save_json(filepath, queries)
    
    def get_prediction_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent prediction history."""
        filepath = os.path.join(self.data_dir, "predictions.json")
        predictions = self.load_json(filepath)
        return predictions[-limit:][::-1]  # Return latest first
    
    def get_weather_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent weather queries."""
        filepath = os.path.join(self.data_dir, "weather_cache.json")
        cache = self.load_json(filepath)
        return cache[-limit:][::-1]  # Return latest first
    
    def get_app_stats(self) -> Dict[str, Any]:
        """Get application usage statistics."""
        predictions = self.load_json(os.path.join(self.data_dir, "predictions.json"))
        weather_cache = self.load_json(os.path.join(self.data_dir, "weather_cache.json"))
        voice_queries = self.load_json(os.path.join(self.data_dir, "voice_queries.json"))
        
        # Count diseases
        disease_counts = {}
        for pred in predictions:
            disease = pred.get("disease", "Unknown")
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
        
        common_diseases = [
            {"disease": disease, "count": count}
            for disease, count in sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        return {
            "total_predictions": len(predictions),
            "weather_queries": len(weather_cache),
            "voice_queries": len(voice_queries),
            "common_diseases": common_diseases
        }

# Global data manager instance (legacy)
data_manager = DataManager()