# GrowWise - Smart Farming Assistant

## Overview

GrowWise is a Flask-based smart farming assistant application that provides farmers with AI-powered tools for crop management. The application integrates weather data, plant disease detection using image analysis, market price information, and voice-based farming assistance.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with Blueprint-based routing
- **Database**: PostgreSQL with SQLAlchemy ORM for scalable data persistence
- **Deployment**: Configured for Vercel serverless deployment with vercel.json
- **Data Storage**: PostgreSQL database with structured models for predictions, weather queries, voice queries, and market prices
- **API Integration**: RESTful endpoints for weather data, disease detection, market prices, and voice queries

### Frontend Architecture
- **Templates**: Jinja2 templating with Bootstrap for responsive UI
- **Styling**: Custom CSS with dark theme support
- **JavaScript**: Vanilla JavaScript for interactive features including speech recognition
- **Icons**: Font Awesome for consistent iconography

### Service-Oriented Design
The application follows a modular service architecture with separate services for:
- Disease detection and image analysis
- Weather data fetching from OpenWeatherMap API
- Market price management with cached data
- Voice query processing and AI responses

## Key Components

### Core Application (`app.py`, `main.py`)
- Flask application factory pattern
- CORS enabled for cross-origin requests
- ProxyFix middleware for proper header handling
- Debug mode for development

### Data Management (`db_models.py`)
- PostgreSQL-based DatabaseManager class for scalable data persistence
- SQLAlchemy ORM models for structured data storage
- Automatic table creation and database initialization
- Database models for predictions, weather queries, voice queries, and market prices
- Migration from JSON file-based storage to PostgreSQL completed

### Routing System (`routes.py`)
- Blueprint-based route organization
- File upload handling for disease detection images
- API endpoints for weather, disease detection, market prices, and voice queries
- Error handling and logging

### Service Layer (`/services`)
- **Disease Service**: Basic image analysis using PIL for plant health assessment
- **Weather Service**: OpenWeatherMap API integration with error handling
- **Market Service**: Static market price data with JSON caching
- **Voice Service**: Pattern-matching voice query processor with farming-specific responses

## Data Flow

1. **User Interaction**: Users interact through web interface or API endpoints
2. **Request Processing**: Flask routes handle requests and delegate to appropriate services
3. **Service Execution**: Services process data (weather API calls, image analysis, etc.)
4. **Data Storage**: Results cached in JSON files for future reference
5. **Response Generation**: Formatted responses returned to user interface

## External Dependencies

### APIs and Services
- **OpenWeatherMap API**: Real-time weather data fetching
- **Vercel Platform**: Serverless deployment and hosting

### Python Libraries
- **Flask**: Web framework and application structure
- **Pillow (PIL)**: Image processing for disease detection
- **Requests**: HTTP client for external API calls
- **Werkzeug**: WSGI utilities and secure filename handling

### Frontend Libraries
- **Bootstrap**: Responsive CSS framework with dark theme
- **Font Awesome**: Icon library for UI components
- **Web Speech API**: Browser-based speech recognition

## Deployment Strategy

### Serverless Architecture
- **Platform**: Vercel for Python serverless functions
- **Configuration**: vercel.json defines build and routing rules
- **Static Assets**: Served directly through Vercel's CDN
- **Environment**: Production environment with 30-second function timeout

### Data Persistence
- **PostgreSQL Database**: Production-ready database with automatic table creation
- **SQLAlchemy ORM**: Object-relational mapping for structured data operations
- **Auto-initialization**: Database tables created automatically on startup
- **Migration Completed**: Successfully migrated from JSON file storage to PostgreSQL

### Scalability Considerations
- Stateless design suitable for serverless scaling
- PostgreSQL database supports enterprise-scale data volumes
- SQLAlchemy ORM provides efficient query optimization and connection pooling

The application is designed as a comprehensive farming assistant that balances functionality with simplicity, making it accessible to farmers while providing valuable AI-powered insights for crop management decisions.