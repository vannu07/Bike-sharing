from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')
import logging
app = Flask(__name__)

class BikeSharingPredictor:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.feature_columns = [
            'yr', 'temp', 'hum', 'windspeed', 'Spring', 'Winter', 
            'Jul', 'Jun', 'Aug', 'Light_rainfall', 'Thunderstrom'
        ]
        self.load_model()
    
    def load_model(self):
        """Load the trained model coefficients"""
        # Model coefficients from the notebook analysis
        self.coefficients = {
            'const': 0.3535,
            'yr': 0.228,
            'temp': 0.526,
            'hum': -0.189,
            'windspeed': -0.165,
            'Spring': -0.113,
            'Winter': 0.045,
            'Aug': -0.59,
            'Jul': -0.124,
            'Jun': -0.05,
            'Light_rainfall': -0.045,
            'Thunderstrom': -0.203
        }
    
    def preprocess_input(self, data):
        """Preprocess input data to match model requirements"""
        # Create a DataFrame with all possible features
        features = pd.DataFrame({
            'yr': [data.get('year', 0)],
            'temp': [data.get('temperature', 0)],
            'atemp': [data.get('temperature', 0)],  # Using temp as atemp
            'hum': [data.get('humidity', 0)],
            'windspeed': [data.get('windspeed', 0)],
            'holiday': [data.get('holiday', 0)],
            'workingday': [data.get('workingday', 1)],
            'Spring': [1 if data.get('season') == 'Spring' else 0],
            'Summer': [1 if data.get('season') == 'Summer' else 0],
            'Winter': [1 if data.get('season') == 'Winter' else 0],
            'Jan': [1 if data.get('month') == 'Jan' else 0],
            'Feb': [1 if data.get('month') == 'Feb' else 0],
            'Mar': [1 if data.get('month') == 'Mar' else 0],
            'Apr': [1 if data.get('month') == 'Apr' else 0],
            'May': [1 if data.get('month') == 'May' else 0],
            'Jun': [1 if data.get('month') == 'Jun' else 0],
            'Jul': [1 if data.get('month') == 'Jul' else 0],
            'Aug': [1 if data.get('month') == 'Aug' else 0],
            'Sep': [1 if data.get('month') == 'Sep' else 0],
            'Oct': [1 if data.get('month') == 'Oct' else 0],
            'Nov': [1 if data.get('month') == 'Nov' else 0],
            'Dec': [1 if data.get('month') == 'Dec' else 0],
            'Light_rainfall': [1 if data.get('weather') == 'Light_rainfall' else 0],
            'Thunderstrom': [1 if data.get('weather') == 'Thunderstrom' else 0],
            'Mon': [1 if data.get('weekday') == 'Mon' else 0],
            'Tue': [1 if data.get('weekday') == 'Tue' else 0],
            'Wed': [1 if data.get('weekday') == 'Wed' else 0],
            'Thurs': [1 if data.get('weekday') == 'Thurs' else 0],
            'Fri': [1 if data.get('weekday') == 'Fri' else 0],
            'Sat': [1 if data.get('weekday') == 'Sat' else 0],
            'Sun': [1 if data.get('weekday') == 'Sun' else 0]
        })
        
        # Scale numeric features (using approximate scaling based on dataset ranges)
        numeric_features = ['temp', 'atemp', 'hum', 'windspeed']
        for feature in numeric_features:
            if feature == 'temp' or feature == 'atemp':
                # Temperature is typically normalized between 0-1 (assuming 0-40°C range)
                features[feature] = features[feature] / 40.0
            elif feature == 'hum':
                # Humidity is already in 0-1 range
                features[feature] = features[feature] / 100.0
            elif feature == 'windspeed':
                # Windspeed normalized (assuming 0-50 km/h range)
                features[feature] = features[feature] / 50.0
        
        return features
    
    def predict(self, data):
        """Make prediction using the linear regression model"""
        try:
            # Preprocess input
            features = self.preprocess_input(data)
            
            # Calculate prediction using the linear equation
            prediction = self.coefficients['const']
            
            for feature in self.feature_columns:
                if feature in features.columns:
                    prediction += self.coefficients[feature] * features[feature].iloc[0]
            
            # Convert back to actual bike count (denormalize)
            # Assuming the model predicts normalized values, we need to scale back
            # This is an approximation - in real scenario, you'd save the scaler
            prediction = max(0, prediction * 1000)  # Scale factor approximation
            
            return round(prediction)
        
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return 0

# Initialize predictor
predictor = BikeSharingPredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        try:
            data = request.get_json()
        except Exception:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Check if data is None (invalid JSON)
        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Validate required fields
        required_fields = ['year', 'temperature', 'humidity', 'windspeed', 'season', 'month', 'weather', 'weekday']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Make prediction
        prediction = predictor.predict(data)
        
        return jsonify({
            'prediction': prediction,
            'status': 'success'
        })
    
    except Exception as e:
        # Log actual exception and stack trace server-side
        logging.error("Error in /predict: %s", e, exc_info=True)
        return jsonify({'error': 'An internal error has occurred.'}), 500
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
