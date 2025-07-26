# AIDH-SSD-_404
This is a repo for our project for All India Developer Challenge 2025 
# This is team "404 not founders"

# GrowWise API

A comprehensive Smart Farming Assistant API built with FastAPI, featuring plant disease detection, weather information, market prices, and voice assistance.

## 🌟 Features

- **🔬 Plant Disease Detection**: AI-powered CNN model for identifying plant diseases from images
- **🌤️ Weather Information**: Real-time weather data integration with OpenWeatherMap
- **💰 Market Prices**: Live market price scraping for vegetables and fruits
- **🎤 Voice Assistant**: Natural language query processing for farming assistance
- **📊 Analytics**: Usage statistics and historical data tracking
- **🗄️ Database**: SQLite database for data persistence

## 🏗️ Architecture

The application follows a clean, modular architecture:

```
src/
├── api/           # API routes and endpoints
├── database/      # Database operations and models
├── models/        # Pydantic schemas and CNN model
├── services/      # Business logic services
├── config.py      # Configuration settings
└── main.py        # Application entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Chrome/Chromium browser (for web scraping)
- OpenWeatherMap API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd growwise-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"
   export MODEL_PATH="path/to/your/model.pt"
   ```

4. **Run the application**
   ```bash
   python -m src.main
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

#### Health Check
```http
GET /health
```

#### Weather Information
```http
POST /weather
Content-Type: application/json

{
  "city": "Chennai",
  "lat": 13.0827,
  "lon": 80.2707
}
```

#### Market Prices
```http
GET /prices
```

#### Disease Detection
```http
POST /predict
Content-Type: multipart/form-data

file: <image_file>
```

#### Voice Query
```http
POST /voice-query
Content-Type: application/json

{
  "query": "What's the weather like today?"
}
```

## 🧠 AI Model

The disease detection uses a custom CNN architecture trained on plant disease datasets:

- **Input**: 224x224 RGB images
- **Architecture**: 4-layer CNN with batch normalization and dropout
- **Classes**: 39 different plant diseases and healthy states
- **Accuracy**: Optimized for agricultural use cases

## 🗄️ Database Schema

The application uses SQLite with the following tables:

- `predictions`: Disease detection history
- `weather_cache`: Weather query cache
- `market_prices`: Market price data
- `user_queries`: Voice query logs

## 🔧 Configuration

Key configuration options in `src/config.py`:

```python
class Settings:
    OPENWEATHER_API_KEY = "your_api_key"
    MODEL_PATH = "plant_disease_model.pt"
    DATABASE_PATH = "growwise_app.db"
    # ... other settings
```

## 🛡️ Security Features

- CORS middleware for cross-origin requests
- Trusted host middleware
- Input validation with Pydantic
- Error handling and logging
- SQL injection prevention

## 📊 Monitoring & Analytics

The API provides built-in analytics:

- Usage statistics
- Prediction history
- Weather query logs
- Common disease patterns

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 8000

CMD ["python", "-m", "src.main"]
```

### Production Considerations

1. **Environment Variables**: Set proper API keys and paths
2. **Database**: Consider PostgreSQL for production
3. **Caching**: Implement Redis for better performance
4. **Load Balancing**: Use nginx or similar
5. **Monitoring**: Add application monitoring tools


## 🔄 Version History

- **v1.0.0**: Initial release with core features
- Disease detection, weather, market prices, voice assistant

## Note

- This is not the final product there are still some bugs and issue which will be resolved soon 
