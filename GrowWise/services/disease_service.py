"""Disease detection service using basic image analysis."""

import logging
from PIL import Image, ImageStat
import io
from typing import Dict

logger = logging.getLogger(__name__)

class DiseaseDetectionService:
    """Service for basic plant analysis and disease detection."""
    
    def __init__(self):
        # Basic disease patterns based on image characteristics
        self.disease_patterns = {
            'brown_spots': {
                'name': 'Possible Brown Spot Disease',
                'treatment': 'Apply copper-based fungicide spray. Remove affected leaves and improve air circulation.'
            },
            'yellow_leaves': {
                'name': 'Possible Yellowing/Chlorosis',
                'treatment': 'Check for nutrient deficiency (nitrogen). Ensure proper watering and fertilization.'
            },
            'dark_patches': {
                'name': 'Possible Blight or Bacterial Infection',
                'treatment': 'Remove infected parts immediately. Apply bactericide and ensure good drainage.'
            },
            'white_patches': {
                'name': 'Possible Powdery Mildew',
                'treatment': 'Improve air circulation. Apply fungicide spray and avoid overhead watering.'
            },
            'healthy': {
                'name': 'Plant Appears Healthy',
                'treatment': 'Continue with regular care and monitoring. Maintain proper watering and fertilization.'
            }
        }
    
    def analyze_image(self, image_data: bytes) -> Dict[str, any]:
        """
        Analyze plant image using basic color and pattern analysis.
        
        Args:
            image_data: Raw image data
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Load and analyze image
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Basic image analysis
            stats = ImageStat.Stat(image)
            avg_r, avg_g, avg_b = stats.mean
            
            # Simple heuristic-based analysis
            disease_type, confidence = self._analyze_colors(avg_r, avg_g, avg_b)
            
            disease_info = self.disease_patterns[disease_type]
            
            return {
                'disease': disease_type,
                'confidence': confidence,
                'treatment': disease_info['treatment'],
                'formatted_name': disease_info['name']
            }
            
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            return {
                'disease': 'analysis_error',
                'confidence': 0.0,
                'treatment': 'Unable to analyze image. Please ensure the image shows clear plant leaves and try again.',
                'formatted_name': 'Analysis Error'
            }
    
    def _analyze_colors(self, avg_r: float, avg_g: float, avg_b: float) -> tuple:
        """
        Analyze average colors to determine possible plant condition.
        
        Args:
            avg_r: Average red value
            avg_g: Average green value
            avg_b: Average blue value
            
        Returns:
            Tuple of (disease_type, confidence)
        """
        # Simple color-based heuristics
        green_ratio = avg_g / (avg_r + avg_g + avg_b)
        red_ratio = avg_r / (avg_r + avg_g + avg_b)
        
        # Determine condition based on color ratios
        if green_ratio > 0.4 and avg_g > avg_r and avg_g > avg_b:
            return 'healthy', 85.0
        elif red_ratio > 0.35 and avg_r > avg_g:
            return 'brown_spots', 75.0
        elif avg_r > 150 and avg_g > 150 and avg_b < 100:
            return 'yellow_leaves', 70.0
        elif avg_r < 100 and avg_g < 100 and avg_b < 100:
            return 'dark_patches', 65.0
        elif avg_r > 200 and avg_g > 200 and avg_b > 200:
            return 'white_patches', 60.0
        else:
            return 'healthy', 50.0

# Global disease service instance
disease_service = DiseaseDetectionService()
