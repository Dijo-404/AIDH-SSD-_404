"""Flask routes for GrowWise application."""

import os
import logging
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime

from services.weather_service import weather_service
from services.disease_service import disease_service
from services.market_service import market_service
from services.voice_service import voice_service
from db_models import db_manager

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    """Main dashboard page."""
    try:
        stats = db_manager.get_app_stats()
        recent_predictions = db_manager.get_prediction_history(5)
        recent_weather = db_manager.get_weather_history(5)
        
        return render_template('index.html', 
                             stats=stats,
                             recent_predictions=recent_predictions,
                             recent_weather=recent_weather)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return render_template('index.html', 
                             stats={},
                             recent_predictions=[],
                             recent_weather=[])

@main_bp.route('/api/weather', methods=['POST'])
def get_weather():
    """Get weather data."""
    try:
        data = request.get_json()
        city = data.get('city')
        lat = data.get('lat')
        lon = data.get('lon')
        
        weather_data = weather_service.get_weather_data(city=city, lat=lat, lon=lon)
        db_manager.save_weather_data(weather_data)
        
        return jsonify({
            'success': True,
            'data': weather_data
        })
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/disease-detection', methods=['POST'])
def detect_disease():
    """Detect plant disease from uploaded image."""
    try:
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if file and allowed_file(file.filename):
            # Read image data
            image_data = file.read()
            
            # Analyze image
            result = disease_service.analyze_image(image_data)
            
            # Save prediction
            db_manager.save_prediction(
                result['disease'],
                result['confidence'],
                result['treatment']
            )
            
            return jsonify({
                'success': True,
                'data': result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.'
            }), 400
            
    except Exception as e:
        logger.error(f"Disease detection error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/market-prices')
def get_market_prices():
    """Get market prices."""
    try:
        category = request.args.get('category', 'all')
        prices = market_service.get_market_prices(category)
        
        return jsonify({
            'success': True,
            'data': prices
        })
    except Exception as e:
        logger.error(f"Market prices error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/voice-query', methods=['POST'])
def process_voice_query():
    """Process voice query."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        response = voice_service.process_query(query)
        db_manager.save_voice_query(query, response)
        
        return jsonify({
            'success': True,
            'data': {
                'query': query,
                'response': response
            }
        })
    except Exception as e:
        logger.error(f"Voice query error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/stats')
def get_stats():
    """Get application statistics."""
    try:
        stats = db_manager.get_app_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'GrowWise API'
    })
