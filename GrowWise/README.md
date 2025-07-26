# GrowWise - Smart Farming Assistant

A comprehensive Flask-based smart farming application that provides AI-powered tools for crop management, featuring plant disease detection, real-time weather information, market price tracking, and voice assistance.

![GrowWise Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)

## 🌟 Features

- **🔬 Plant Disease Detection**: AI-powered image analysis for identifying plant diseases and providing treatment recommendations
- **🌤️ Real-time Weather Data**: Integration with OpenWeatherMap API for accurate weather information
- **📊 Market Price Tracking**: Live market prices for fruits and vegetables
- **🎤 Voice Assistant**: Natural language processing for farming queries and advice
- **📱 Responsive Design**: Modern glassmorphism UI with smooth animations
- **🗄️ PostgreSQL Database**: Scalable data persistence with SQLAlchemy ORM
- **☁️ Vercel Ready**: Optimized for serverless deployment

## 🚀 Live Demo

The application is deployed and ready for use on Vercel.

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: Bootstrap 5, Vanilla JavaScript, Glassmorphism CSS
- **APIs**: OpenWeatherMap API
- **Deployment**: Vercel Serverless
- **Image Processing**: Pillow (PIL)
- **Database**: PostgreSQL with automatic table creation

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenWeatherMap API key

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/growwise.git
cd growwise
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="your_postgresql_connection_string"
export SESSION_SECRET="your_secret_key"
export OPENWEATHER_API_KEY="your_openweather_api_key"
```

4. Run the application:
```bash
python main.py
```

## 🌐 Deployment

### Vercel Deployment

The application is configured for Vercel deployment:

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard:
   - `DATABASE_URL`
   - `SESSION_SECRET`
   - `OPENWEATHER_API_KEY`

## 📊 Database Schema

The application uses PostgreSQL with the following tables:

- **predictions**: Plant disease detection results
- **weather_queries**: Weather data cache
- **voice_queries**: Voice assistant conversation history
- **market_prices**: Market price data

## 🎨 UI Features

- **Glassmorphism Design**: Modern glass effect with backdrop blur
- **Smooth Animations**: CSS transitions and hover effects
- **Responsive Layout**: Mobile-first design approach
- **Dark Theme**: Optimized for low-light environments
- **Enhanced Readability**: Improved font colors and contrast

## 🔊 Voice Assistant

The voice assistant supports queries about:
- Crop management and farming techniques
- Pest control and disease prevention
- Weather conditions and forecasts
- Market prices and selling strategies

## 📈 Features Overview

### Disease Detection
- Upload plant images for analysis
- AI-powered disease identification
- Treatment recommendations
- Confidence scoring

### Weather Integration
- Current weather conditions
- Location-based forecasts
- Humidity and wind speed data
- Weather history tracking

### Market Prices
- Real-time price updates
- Category-based filtering
- Historical price trends
- Market insights

## 🔒 Security

- Environment variable management
- Secure file upload handling
- SQL injection prevention via SQLAlchemy ORM
- Input validation and sanitization

## 📚 API Endpoints

- `GET /` - Main dashboard
- `POST /api/weather` - Weather data
- `POST /api/disease-detection` - Disease analysis
- `GET /api/market-prices` - Market prices
- `POST /api/voice-query` - Voice assistant

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Bootstrap team for the UI framework
- Flask community for the web framework
- PostgreSQL for reliable database management

## 📞 Support

For support, email support@growwise.com or open an issue on GitHub.

---

**Built with ❤️ for farmers worldwide**