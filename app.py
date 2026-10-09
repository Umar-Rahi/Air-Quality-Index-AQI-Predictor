from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
import logging
import pandas as pd
from datetime import datetime

def log_prediction(data, prediction, category):
    log_file = "aqi_prediction_log.csv"

    # Add AQI and category to input data
    data['Predicted_AQI'] = round(prediction, 1)
    data['Category'] = category
    data['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame([data])  # wrap in list to create 1-row DataFrame

    # Append to CSV
    if not os.path.exists(log_file):
        df.to_csv(log_file, index=False)
    else:
        df.to_csv(log_file, mode='a', index=False, header=False)


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and scaler
model = None
scaler = None

def load_model():
    """Load the trained model and scaler"""
    global model, scaler
    try:
        if os.path.exists('aqi_model.pkl') and os.path.exists('scaler.pkl'):
            model = joblib.load('aqi_model.pkl')
            scaler = joblib.load('scaler.pkl')
            logger.info("Model and scaler loaded successfully")
            return True
        else:
            logger.error("Model files not found. Please run model_train.py first.")
            return False
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def get_aqi_category(aqi):
    """Get AQI category based on AQI value"""
    if aqi <= 50:
        return "Good", "#00E400"
    elif aqi <= 100:
        return "Moderate", "#FFFF00"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "#FF7E00"
    elif aqi <= 200:
        return "Unhealthy", "#FF0000"
    elif aqi <= 300:
        return "Very Unhealthy", "#8F3F97"
    else:
        return "Hazardous", "#7E0023"

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/predict', methods=['POST'])
def predict_aqi():
    """Predict AQI based on input parameters"""
    try:
        # Check if model is loaded
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model not loaded. Please ensure model files exist and restart the server.'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features
        required_features = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'temperature', 'humidity']
        
        # Validate input
        for feature in required_features:
            if feature not in data:
                return jsonify({'error': f'Missing required parameter: {feature}'}), 400
            
            # Convert to float and validate
            try:
                value = float(data[feature])
                if value < 0:
                    return jsonify({'error': f'Invalid value for {feature}: must be non-negative'}), 400
                data[feature] = value
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid value for {feature}: must be a number'}), 400
        
        # Prepare features for prediction
        features = np.array([[
            data['pm25'],
            data['pm10'], 
            data['no2'],
            data['so2'],
            data['co'],
            data['o3'],
            data['temperature'],
            data['humidity']
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        aqi_prediction = model.predict(features_scaled)[0]
        
        # Ensure AQI is within reasonable bounds
        aqi_prediction = max(0, min(500, aqi_prediction))
        
        # Get category and color
        category, color = get_aqi_category(aqi_prediction)
        
        # Prepare response
        response = {
            'aqi': round(aqi_prediction, 1),
            'category': category,
            'color': color,
            'input_data': {
                'PM2.5': data['pm25'],
                'PM10': data['pm10'],
                'NO2': data['no2'],
                'SO2': data['so2'],
                'CO': data['co'],
                'O3': data['o3'],
                'Temperature': data['temperature'],
                'Humidity': data['humidity']
            }
        }
        
        logger.info(f"Prediction made: AQI = {aqi_prediction:.1f}, Category = {category}")
        # Log the prediction
        log_prediction(data, aqi_prediction, category)

        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Get sample air quality data"""
    sample_datasets = [
        {
            'name': 'Good Air Quality',
            'data': {
                'pm25': 8.5,
                'pm10': 15.2,
                'no2': 12.3,
                'so2': 2.1,
                'co': 0.4,
                'o3': 45.2,
                'temperature': 22.5,
                'humidity': 55.0
            }
        },
        {
            'name': 'Moderate Air Quality',
            'data': {
                'pm25': 25.4,
                'pm10': 45.8,
                'no2': 35.6,
                'so2': 8.2,
                'co': 1.2,
                'o3': 85.3,
                'temperature': 28.1,
                'humidity': 68.5
            }
        },
        {
            'name': 'Unhealthy Air Quality',
            'data': {
                'pm25': 95.6,
                'pm10': 155.2,
                'no2': 75.4,
                'so2': 25.1,
                'co': 8.5,
                'o3': 145.8,
                'temperature': 35.2,
                'humidity': 45.3
            }
        },
        {
            'name': 'Very Unhealthy Air Quality',
            'data': {
                'pm25': 185.3,
                'pm10': 285.7,
                'no2': 125.8,
                'so2': 45.6,
                'co': 15.2,
                'o3': 205.4,
                'temperature': 38.7,
                'humidity': 35.8
            }
        }
    ]
    
    return jsonify(sample_datasets)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None and scaler is not None else "not loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load model on startup
    if not load_model():
        print("WARNING: Model files not found. Please run 'python model_train.py' first.")
        print("The server will start but predictions will not work until the model is trained.")
    
    print("Starting Flask server...")
    print("Open http://localhost:5000 in your browser")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)