"""Disease detection service using CNN model."""

import torch
import logging
from torchvision import transforms
from PIL import Image
import io
import os
from typing import Dict
from fastapi import HTTPException

from ..config import settings
from ..models.cnn_model import PlantDiseaseCNN, DISEASE_CLASSES, TREATMENT_RECOMMENDATIONS

logger = logging.getLogger(__name__)

class DiseaseDetectionService:
    """Service for plant disease detection using CNN model."""
    
    def __init__(self):
        self.model = None
        self.transform = None
        self.num_classes = len(DISEASE_CLASSES)
        self._load_model()
        self._setup_transforms()
    
    def _load_model(self) -> None:
        """Load the pre-trained CNN model."""
        try:
            self.model = PlantDiseaseCNN(self.num_classes)
            
            if os.path.exists(settings.MODEL_PATH):
                state_dict = torch.load(settings.MODEL_PATH, map_location='cpu')
                self.model.load_state_dict(state_dict)
                self.model.eval()
                logger.info("Disease detection model loaded successfully")
            else:
                logger.warning(f"Model file not found at {settings.MODEL_PATH}. Disease detection will use fallback mode.")
                self.model = None
                
        except Exception as e:
            logger.error(f"Error loading disease model: {e}")
            self.model = None
    
    def _setup_transforms(self) -> None:
        """Setup image preprocessing transforms."""
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], 
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def is_model_available(self) -> bool:
        """Check if the model is loaded and available."""
        return self.model is not None and self.transform is not None
    
    def predict_disease(self, image_bytes: bytes) -> Dict[str, any]:
        """
        Predict plant disease from image bytes.
        
        Args:
            image_bytes: Raw image data
            
        Returns:
            Dictionary containing prediction results
            
        Raises:
            HTTPException: If model is unavailable or prediction fails
        """
        if not self.is_model_available():
            # Return fallback response when model is not available
            logger.warning("Model not available, returning fallback response")
            return {
                'disease': 'model_unavailable',
                'confidence': 0.0,
                'treatment': 'Disease detection model is currently unavailable. Please ensure the model file is present and try again.',
                'formatted_name': 'Model Unavailable'
            }

        try:
            # Load and preprocess image
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            tensor = self.transform(image).unsqueeze(0)

            # Make prediction
            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)

            # Get results
            disease_key = DISEASE_CLASSES[predicted_idx.item()]
            confidence_score = float(confidence.item() * 100)

            # Format disease name for display
            formatted_name = self._format_disease_name(disease_key)

            # Get treatment recommendation
            treatment = TREATMENT_RECOMMENDATIONS.get(
                disease_key,
                'Consult with local agricultural extension officer for specific treatment'
            )

            return {
                'disease': disease_key,
                'confidence': confidence_score,
                'treatment': treatment,
                'formatted_name': formatted_name
            }

        except Exception as e:
            logger.error(f"Disease prediction error: {e}")
            raise HTTPException(
                status_code=500, 
                detail="Error processing image for disease detection"
            )
    
    def _format_disease_name(self, disease_key: str) -> str:
        """
        Format disease name for human-readable display.
        
        Args:
            disease_key: Raw disease class name
            
        Returns:
            Formatted disease name
        """
        return disease_key.replace('___', ' - ').replace('_', ' ')

# Global disease service instance
disease_service = DiseaseDetectionService()