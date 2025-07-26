"""Database models for GrowWise application."""

from datetime import datetime
from extensions import db


class Prediction(db.Model):
    """Model for storing plant disease predictions."""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    treatment = db.Column(db.Text, nullable=True)
    formatted_name = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'disease': self.disease,
            'confidence': self.confidence,
            'treatment': self.treatment,
            'formatted_name': self.formatted_name,
            'timestamp': self.timestamp.isoformat()
        }

class WeatherQuery(db.Model):
    """Model for storing weather query history."""
    __tablename__ = 'weather_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=True)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    humidity = db.Column(db.Integer, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'city': self.city,
            'country': self.country,
            'temperature': self.temperature,
            'description': self.description,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'timestamp': self.timestamp.isoformat()
        }

class VoiceQuery(db.Model):
    """Model for storing voice assistant queries."""
    __tablename__ = 'voice_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'query': self.query,
            'response': self.response,
            'timestamp': self.timestamp.isoformat()
        }

class MarketPrice(db.Model):
    """Model for storing market price data."""
    __tablename__ = 'market_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # 'Vegetable' or 'Fruit'
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'category': self.category,
            'name': self.name,
            'price': self.price,
            'timestamp': self.timestamp.isoformat()
        }

class DatabaseManager:
    """Database manager class for handling operations."""
    
    def save_prediction(self, disease: str, confidence: float, treatment: str, formatted_name: str = None):
        """Save disease prediction to database."""
        try:
            prediction = Prediction(
                disease=disease,
                confidence=confidence,
                treatment=treatment,
                formatted_name=formatted_name
            )
            db.session.add(prediction)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def save_weather_data(self, weather_data: dict):
        """Save weather data to database."""
        try:
            weather_query = WeatherQuery(
                city=weather_data['city'],
                country=weather_data.get('country'),
                temperature=weather_data['temperature'],
                description=weather_data.get('description'),
                humidity=weather_data.get('humidity'),
                wind_speed=weather_data.get('wind_speed')
            )
            db.session.add(weather_query)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def save_voice_query(self, query: str, response: str):
        """Save voice query and response to database."""
        try:
            voice_query = VoiceQuery(
                query=query,
                response=response
            )
            db.session.add(voice_query)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def save_market_prices(self, prices: list):
        """Save market prices to database."""
        try:
            # Clear old prices (older than 1 day)
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=1)
            MarketPrice.query.filter(MarketPrice.timestamp < cutoff_date).delete()
            
            # Add new prices
            for price_data in prices:
                market_price = MarketPrice(
                    category=price_data['category'],
                    name=price_data['name'],
                    price=price_data['price']
                )
                db.session.add(market_price)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_prediction_history(self, limit: int = 10) -> list:
        """Get recent disease prediction history."""
        predictions = Prediction.query.order_by(Prediction.timestamp.desc()).limit(limit).all()
        return [pred.to_dict() for pred in predictions]
    
    def get_weather_history(self, limit: int = 10) -> list:
        """Get recent weather queries."""
        weather_queries = WeatherQuery.query.order_by(WeatherQuery.timestamp.desc()).limit(limit).all()
        return [query.to_dict() for query in weather_queries]
    
    def get_voice_history(self, limit: int = 10) -> list:
        """Get recent voice queries."""
        voice_queries = VoiceQuery.query.order_by(VoiceQuery.timestamp.desc()).limit(limit).all()
        return [query.to_dict() for query in voice_queries]
    
    def get_app_stats(self) -> dict:
        """Get application usage statistics."""
        try:
            total_predictions = Prediction.query.count()
            weather_queries = WeatherQuery.query.count()
            voice_queries = VoiceQuery.query.count()
            
            # Get most common diseases
            from sqlalchemy import func
            common_diseases = db.session.query(
                Prediction.disease,
                func.count(Prediction.disease).label('count')
            ).group_by(Prediction.disease).order_by(
                func.count(Prediction.disease).desc()
            ).limit(5).all()
            
            common_diseases_list = [
                {'disease': disease, 'count': count}
                for disease, count in common_diseases
            ]
            
            return {
                'total_predictions': total_predictions,
                'weather_queries': weather_queries,
                'voice_queries': voice_queries,
                'common_diseases': common_diseases_list
            }
        except Exception as e:
            return {
                'total_predictions': 0,
                'weather_queries': 0,
                'voice_queries': 0,
                'common_diseases': []
            }

# Global database manager instance
db_manager = DatabaseManager()
