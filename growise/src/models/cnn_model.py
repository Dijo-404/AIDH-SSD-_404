"""CNN Model for plant disease detection."""

import torch
import torch.nn as nn
from typing import Dict

class PlantDiseaseCNN(nn.Module):
    """Convolutional Neural Network for plant disease classification."""
    
    def __init__(self, num_classes: int):
        super(PlantDiseaseCNN, self).__init__()
        
        self.conv_layers = nn.Sequential(
            # First convolutional block
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(32),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Second convolutional block
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(64),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Third convolutional block
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(128),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Fourth convolutional block
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(256),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.classifier = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(50176, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(1024, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network."""
        features = self.conv_layers(x)
        features = features.view(features.size(0), -1)
        output = self.classifier(features)
        return output

# Disease class mappings
DISEASE_CLASSES: Dict[int, str] = {
    0: 'Apple___Apple_scab', 1: 'Apple___Black_rot', 2: 'Apple___Cedar_apple_rust',
    3: 'Apple___healthy', 4: 'Background_without_leaves', 5: 'Blueberry___healthy',
    6: 'Cherry___Powdery_mildew', 7: 'Cherry___healthy', 8: 'Corn___Cercospora_leaf_spot Gray_leaf_spot',
    9: 'Corn___Common_rust', 10: 'Corn___Northern_Leaf_Blight', 11: 'Corn___healthy',
    12: 'Grape___Black_rot', 13: 'Grape___Esca_(Black_Measles)', 14: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    15: 'Grape___healthy', 16: 'Orange___Haunglongbing_(Citrus_greening)', 17: 'Peach___Bacterial_spot',
    18: 'Peach___healthy', 19: 'Pepper,_bell___Bacterial_spot', 20: 'Pepper,_bell___healthy',
    21: 'Potato___Early_blight', 22: 'Potato___Late_blight', 23: 'Potato___healthy',
    24: 'Raspberry___healthy', 25: 'Soybean___healthy', 26: 'Squash___Powdery_mildew',
    27: 'Strawberry___Leaf_scorch', 28: 'Strawberry___healthy', 29: 'Tomato___Bacterial_spot',
    30: 'Tomato___Early_blight', 31: 'Tomato___Late_blight', 32: 'Tomato___Leaf_Mold',
    33: 'Tomato___Septoria_leaf_spot', 34: 'Tomato___Spider_mites Two-spotted_spider_mite',
    35: 'Tomato___Target_Spot', 36: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    37: 'Tomato___Tomato_mosaic_virus', 38: 'Tomato___healthy'
}

# Treatment recommendations for each disease
TREATMENT_RECOMMENDATIONS: Dict[str, str] = {
    'Apple___Apple_scab': 'Apply fungicide spray during wet weather. Remove fallen leaves and improve air circulation.',
    'Apple___Black_rot': 'Prune infected branches, apply copper-based fungicide, and remove mummified fruits.',
    'Apple___Cedar_apple_rust': 'Remove nearby cedar trees if possible, apply preventive fungicide sprays.',
    'Tomato___Late_blight': 'Remove affected leaves immediately, apply copper fungicide, ensure good drainage.',
    'Tomato___Early_blight': 'Apply fungicide spray, remove lower leaves, and ensure proper spacing for air circulation.',
    'Tomato___Bacterial_spot': 'Use copper-based bactericide, avoid overhead watering, remove infected plants.',
    'Corn___Common_rust': 'Use resistant varieties, apply fungicide if infection is severe, remove crop residues.',
    'Corn___Northern_Leaf_Blight': 'Rotate crops, use resistant varieties, apply fungicide if needed.',
    'Grape___Black_rot': 'Prune for air circulation, apply preventive fungicide sprays, remove infected berries.',
    'Potato___Late_blight': 'Apply copper-based fungicide, avoid overhead watering, harvest early if needed.',
    'Potato___Early_blight': 'Rotate crops, apply fungicide, remove infected foliage.',
    'healthy': 'Plant appears healthy! Continue with regular care and monitoring.',
    'Background_without_leaves': 'Please take a clearer photo showing plant leaves for accurate diagnosis.'
}