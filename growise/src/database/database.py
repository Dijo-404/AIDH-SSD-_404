"""Database operations and management."""

import sqlite3
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from contextlib import contextmanager

from ..config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database operations for the GrowWise application."""
    
    def __init__(self, db_path: str = settings.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self) -> None:
        """Initialize database tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Predictions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disease TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    treatment TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Weather cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    temperature REAL,
                    description TEXT,
                    humidity INTEGER,
                    wind_speed REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Market prices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    name TEXT NOT NULL,
                    price TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User queries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def save_prediction(self, disease: str, confidence: float, treatment: str) -> None:
        """Save disease prediction to database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO predictions (disease, confidence, treatment) VALUES (?, ?, ?)",
                (disease, confidence, treatment)
            )
            conn.commit()
    
    def save_weather_data(self, weather_data: Dict[str, Any]) -> None:
        """Save weather data to database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO weather_cache 
                   (city, temperature, description, humidity, wind_speed) 
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    weather_data['city'],
                    weather_data['temperature'],
                    weather_data['description'],
                    weather_data['humidity'],
                    weather_data['wind_speed']
                )
            )
            conn.commit()
    
    def save_market_prices(self, prices: List[Dict[str, str]]) -> None:
        """Save market prices to database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Clear old prices (older than 1 day)
            cursor.execute(
                "DELETE FROM market_prices WHERE datetime(timestamp) < datetime('now', '-1 day')"
            )
            
            # Insert new prices
            for item in prices:
                cursor.execute(
                    "INSERT INTO market_prices (category, name, price) VALUES (?, ?, ?)",
                    (item['category'], item['name'], item['price'])
                )
            
            conn.commit()
    
    def save_voice_query(self, query: str, response: str) -> None:
        """Save voice query and response to database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_queries (query, response) VALUES (?, ?)",
                (query, response)
            )
            conn.commit()
    
    def get_prediction_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent disease prediction history."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT disease, confidence, treatment, timestamp 
                   FROM predictions 
                   ORDER BY timestamp DESC 
                   LIMIT ?""",
                (limit,)
            )
            rows = cursor.fetchall()
            
            return [
                {
                    'disease': row[0],
                    'confidence': row[1],
                    'treatment': row[2],
                    'timestamp': row[3]
                }
                for row in rows
            ]
    
    def get_weather_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent weather queries history."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT city, temperature, description, timestamp 
                   FROM weather_cache 
                   ORDER BY timestamp DESC 
                   LIMIT ?""",
                (limit,)
            )
            rows = cursor.fetchall()
            
            return [
                {
                    'city': row[0],
                    'temperature': row[1],
                    'description': row[2],
                    'timestamp': row[3]
                }
                for row in rows
            ]
    
    def get_app_stats(self) -> Dict[str, Any]:
        """Get application usage statistics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total predictions
            cursor.execute("SELECT COUNT(*) FROM predictions")
            total_predictions = cursor.fetchone()[0]
            
            # Get total weather queries
            cursor.execute("SELECT COUNT(*) FROM weather_cache")
            weather_queries = cursor.fetchone()[0]
            
            # Get total voice queries
            cursor.execute("SELECT COUNT(*) FROM user_queries")
            voice_queries = cursor.fetchone()[0]
            
            # Get most common diseases
            cursor.execute("""
                SELECT disease, COUNT(*) as count
                FROM predictions
                GROUP BY disease
                ORDER BY count DESC
                LIMIT 5
            """)
            common_diseases = [
                {'disease': row[0], 'count': row[1]} 
                for row in cursor.fetchall()
            ]
            
            return {
                'total_predictions': total_predictions,
                'weather_queries': weather_queries,
                'voice_queries': voice_queries,
                'common_diseases': common_diseases
            }

# Global database instance
db_manager = DatabaseManager()