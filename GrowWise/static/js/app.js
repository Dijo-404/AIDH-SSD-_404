// GrowWise JavaScript Application

// Global variables
let isRecording = false;
let recognition = null;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize event listeners
    setupEventListeners();
    
    // Setup speech recognition
    setupSpeechRecognition();
    
    // Add smooth scroll animations
    setupScrollAnimations();
    
    // Add entry animations
    setupEntryAnimations();
    
    // Load initial data
    loadMarketPrices('all');
    
    console.log('GrowWise app initialized');
}

function setupEventListeners() {
    // Weather form
    const weatherForm = document.getElementById('weather-form');
    if (weatherForm) {
        weatherForm.addEventListener('submit', handleWeatherSubmit);
    }
    
    // Disease detection form
    const diseaseForm = document.getElementById('disease-form');
    if (diseaseForm) {
        diseaseForm.addEventListener('submit', handleDiseaseSubmit);
    }
    
    // Voice query form
    const voiceForm = document.getElementById('voice-form');
    if (voiceForm) {
        voiceForm.addEventListener('submit', handleVoiceSubmit);
    }
    
    // Image input preview
    const imageInput = document.getElementById('image');
    if (imageInput) {
        imageInput.addEventListener('change', previewImage);
    }
}

// Weather functionality
async function handleWeatherSubmit(e) {
    e.preventDefault();
    
    const city = document.getElementById('city').value.trim();
    if (!city) return;
    
    showLoading('weather-results');
    
    try {
        const response = await fetch('/api/weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city: city })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayWeatherResults(data.data);
        } else {
            showError('weather-results', data.error || 'Failed to fetch weather data');
        }
    } catch (error) {
        console.error('Weather API error:', error);
        showError('weather-results', 'Network error. Please try again.');
    }
}

function displayWeatherResults(weather) {
    const resultsDiv = document.getElementById('weather-results');
    resultsDiv.innerHTML = `
        <div class="weather-card">
            <h5 class="mb-3">
                <i class="fas fa-map-marker-alt me-2"></i>
                ${weather.city}, ${weather.country}
            </h5>
            <div class="row">
                <div class="col-md-6">
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-thermometer-half fa-lg me-3"></i>
                        <div>
                            <h3 class="mb-0">${weather.temperature}°C</h3>
                            <small>${weather.description}</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-2">
                        <i class="fas fa-tint me-2"></i>
                        <strong>Humidity:</strong> ${weather.humidity}%
                    </div>
                    <div>
                        <i class="fas fa-wind me-2"></i>
                        <strong>Wind:</strong> ${weather.wind_speed} m/s
                    </div>
                </div>
            </div>
        </div>
    `;
}

async function getLocationWeather() {
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by this browser.');
        return;
    }
    
    showLoading('weather-results');
    
    navigator.geolocation.getCurrentPosition(async (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        
        try {
            const response = await fetch('/api/weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ lat: lat, lon: lon })
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayWeatherResults(data.data);
            } else {
                showError('weather-results', data.error || 'Failed to fetch weather data');
            }
        } catch (error) {
            console.error('Weather API error:', error);
            showError('weather-results', 'Network error. Please try again.');
        }
    }, (error) => {
        console.error('Geolocation error:', error);
        showError('weather-results', 'Unable to get your location. Please enter city manually.');
    });
}

// Disease detection functionality
async function handleDiseaseSubmit(e) {
    e.preventDefault();
    
    const imageInput = document.getElementById('image');
    const file = imageInput.files[0];
    
    if (!file) {
        alert('Please select an image file.');
        return;
    }
    
    showLoading('disease-results');
    
    const formData = new FormData();
    formData.append('image', file);
    
    try {
        const response = await fetch('/api/disease-detection', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayDiseaseResults(data.data);
        } else {
            showError('disease-results', data.error || 'Failed to analyze image');
        }
    } catch (error) {
        console.error('Disease detection error:', error);
        showError('disease-results', 'Network error. Please try again.');
    }
}

function displayDiseaseResults(result) {
    const resultsDiv = document.getElementById('disease-results');
    
    const confidenceColor = result.confidence > 70 ? 'success' : result.confidence > 50 ? 'warning' : 'danger';
    
    resultsDiv.innerHTML = `
        <div class="disease-result">
            <h5 class="text-${result.disease === 'healthy' ? 'success' : 'danger'} mb-3">
                <i class="fas fa-${result.disease === 'healthy' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                ${result.formatted_name}
            </h5>
            
            <div class="mb-3">
                <label class="form-label">Confidence Level</label>
                <div class="progress">
                    <div class="progress-bar bg-${confidenceColor}" role="progressbar" 
                         style="width: ${result.confidence}%" 
                         aria-valuenow="${result.confidence}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        ${result.confidence.toFixed(1)}%
                    </div>
                </div>
            </div>
            
            <div class="alert alert-info">
                <h6 class="alert-heading">
                    <i class="fas fa-lightbulb me-2"></i>Treatment Recommendation
                </h6>
                <p class="mb-0">${result.treatment}</p>
            </div>
        </div>
    `;
}

function previewImage(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Remove existing preview
            const existingPreview = document.querySelector('.image-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            
            // Create new preview
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'image-preview';
            img.alt = 'Selected image preview';
            
            // Insert after the file input
            const fileInput = document.getElementById('image');
            fileInput.parentNode.insertBefore(img, fileInput.nextSibling);
        };
        reader.readAsDataURL(file);
    }
}

// Market prices functionality
async function loadMarketPrices(category = 'all') {
    showLoading('market-prices-results');
    
    try {
        const response = await fetch(`/api/market-prices?category=${category}`);
        const data = await response.json();
        
        if (data.success) {
            displayMarketPrices(data.data);
        } else {
            showError('market-prices-results', data.error || 'Failed to load market prices');
        }
    } catch (error) {
        console.error('Market prices error:', error);
        showError('market-prices-results', 'Network error. Please try again.');
    }
}

function displayMarketPrices(prices) {
    const resultsDiv = document.getElementById('market-prices-results');
    
    if (prices.length === 0) {
        resultsDiv.innerHTML = '<p class="text-muted">No price data available.</p>';
        return;
    }
    
    const groupedPrices = groupBy(prices, 'category');
    
    let html = '';
    for (const [category, items] of Object.entries(groupedPrices)) {
        html += `
            <div class="mb-4">
                <h5 class="text-${category.toLowerCase() === 'vegetable' ? 'success' : 'warning'} mb-3">
                    <i class="fas fa-${category.toLowerCase() === 'vegetable' ? 'carrot' : 'apple-alt'} me-2"></i>
                    ${category}s
                </h5>
                <div class="row">
        `;
        
        items.forEach(item => {
            html += `
                <div class="col-md-6 col-lg-4 mb-2">
                    <div class="market-price-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <strong>${item.name}</strong>
                            <span class="text-primary fw-bold">${item.price}</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div></div>';
    }
    
    resultsDiv.innerHTML = html;
}

// Voice assistant functionality
async function handleVoiceSubmit(e) {
    e.preventDefault();
    
    const query = document.getElementById('voice-query').value.trim();
    if (!query) return;
    
    showLoading('voice-results');
    document.getElementById('voice-results').style.display = 'block';
    
    try {
        const response = await fetch('/api/voice-query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayVoiceResponse(data.data.response);
        } else {
            showError('voice-response', data.error || 'Failed to process query');
        }
    } catch (error) {
        console.error('Voice query error:', error);
        showError('voice-response', 'Network error. Please try again.');
    }
}

function displayVoiceResponse(response) {
    const responseDiv = document.getElementById('voice-response');
    responseDiv.innerHTML = `
        <i class="fas fa-robot me-2"></i>
        ${response}
    `;
    document.getElementById('voice-results').style.display = 'block';
}

function setVoiceQuery(query) {
    document.getElementById('voice-query').value = query;
    document.getElementById('voice-query').focus();
}

// Speech recognition functionality
function setupSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isRecording = true;
            const btn = document.querySelector('[onclick="startVoiceRecognition()"]');
            if (btn) {
                btn.innerHTML = '<i class="fas fa-stop me-2"></i>Stop Recording';
                btn.classList.add('voice-recording');
            }
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('voice-query').value = transcript;
        };
        
        recognition.onend = function() {
            isRecording = false;
            const btn = document.querySelector('[onclick="startVoiceRecognition()"]');
            if (btn) {
                btn.innerHTML = '<i class="fas fa-microphone me-2"></i>Voice Input';
                btn.classList.remove('voice-recording');
            }
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            alert('Speech recognition error: ' + event.error);
        };
    }
}

function startVoiceRecognition() {
    if (!recognition) {
        alert('Speech recognition is not supported in your browser.');
        return;
    }
    
    if (isRecording) {
        recognition.stop();
    } else {
        recognition.start();
    }
}

// Utility functions
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2 text-muted">Processing...</p>
        </div>
    `;
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-circle me-2"></i>
            <strong>Error:</strong> ${message}
        </div>
    `;
}

function groupBy(array, key) {
    return array.reduce((result, currentValue) => {
        (result[currentValue[key]] = result[currentValue[key]] || []).push(currentValue);
        return result;
    }, {});
}

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Theme management
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
});

// Scroll animations
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards and sections
    document.querySelectorAll('.card, section').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Entry animations
function setupEntryAnimations() {
    // Stagger animation for stat cards
    const statCards = document.querySelectorAll('.card.bg-primary, .card.bg-info, .card.bg-success, .card.bg-warning');
    statCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-fade-in-up');
    });

    // Animate navigation items
    const navItems = document.querySelectorAll('.nav-link');
    navItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.05}s`;
        item.classList.add('animate-fade-in-down');
    });
}

// Add button click effects
function addButtonEffects() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Initialize button effects when DOM is loaded
document.addEventListener('DOMContentLoaded', addButtonEffects);
