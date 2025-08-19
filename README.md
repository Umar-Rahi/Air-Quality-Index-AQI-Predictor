# Air Quality Index (AQI) Predictor

## 🌐 Live Demo
[Visit my Portfolio]([https://umar-rahi.github.io](https://umar-rahi.github.io/Air-Quality-Index-AQI-Predictor/)

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)  
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)  
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange.svg)  
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)  
![Status](https://img.shields.io/badge/Status-Active-success.svg)  

A full-stack web application that predicts Air Quality Index using machine learning. The application takes various air pollutant measurements and weather data as input to predict the AQI value and category.

## Features

- **Machine Learning Prediction**: Uses Random Forest Regressor to predict AQI
- **Real-time API**: Flask backend serves predictions via REST API
- **Interactive Frontend**: Modern, responsive UI with Bootstrap
- **Data Visualization**: Chart.js integration for pollutant level visualization
- **Sample Data**: Pre-loaded sample datasets for testing
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Tech Stack

### Backend
- **Python 3.7+**
- **Flask** - Web framework
- **scikit-learn** - Machine learning
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **joblib** - Model serialization
- **flask-cors** - Cross-origin requests

### Frontend
- **HTML5**
- **CSS3** with Bootstrap 5
- **JavaScript (ES6+)**
- **Chart.js** - Data visualization
- **Bootstrap** - UI framework

## Project Structure

```
air-quality-predictor/
├── model_train.py      # ML model training script
├── app.py             # Flask backend server
├── index.html         # Frontend HTML
├── style.css          # Custom styling
├── script.js          # Frontend JavaScript
├── aqi_model.pkl      # Trained ML model (generated)
├── scaler.pkl         # Feature scaler (generated)
└── README.md          # This file
```

## Installation & Setup

### 1. Clone or Download the Project

Create a new directory and save all the provided files:
- `model_train.py`
- `app.py`
- `index.html`
- `style.css`
- `script.js`

### 2. Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install flask flask-cors scikit-learn pandas numpy joblib
```

### 3. Train the Machine Learning Model

```bash
python model_train.py
```

This will:
- Generate synthetic air quality data
- Train a Random Forest model
- Save the model as `aqi_model.pkl`
- Save the feature scaler as `scaler.pkl`
- Display model performance metrics

Expected output:
```
Generating synthetic air quality data...
Dataset shape: (5000, 9)
AQI range: 0.00 - 500.00
Training Random Forest model...
Model Performance:
MSE: 125.45
R2 Score: 0.9234
RMSE: 11.20
...
Model training completed successfully!
```

### 4. Start the Flask Backend

```bash
python app.py
```

The server will start on `http://localhost:5000`

Expected output:
```
Model and scaler loaded successfully
Starting Flask server...
Open http://localhost:5000 in your browser
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[::1]:5000
```

### 5. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Input Parameters

The application accepts the following air quality and weather parameters:

| Parameter | Unit | Description | Range |
|-----------|------|-------------|-------|
| PM2.5 | μg/m³ | Fine particulate matter | 0-500 |
| PM10 | μg/m³ | Coarse particulate matter | 0-600 |
| NO₂ | ppb | Nitrogen dioxide | 0-200 |
| SO₂ | ppb | Sulfur dioxide | 0-100 |
| CO | ppm | Carbon monoxide | 0-50 |
| O₃ | ppb | Ozone | 0-300 |
| Temperature | °C | Ambient temperature | -50 to 60 |
| Humidity | % | Relative humidity | 0-100 |

### AQI Categories

| AQI Range | Category | Color | Description |
|-----------|----------|-------|-------------|
| 0-50 | Good | Green | Satisfactory air quality |
| 51-100 | Moderate | Yellow | Acceptable for most people |
| 101-150 | Unhealthy for Sensitive Groups | Orange | Sensitive groups may be affected |
| 151-200 | Unhealthy | Red | Everyone may be affected |
| 201-300 | Very Unhealthy | Purple | Health alert for everyone |
| 301-500 | Hazardous | Maroon | Emergency conditions |

### How to Use

1. **Enter Values**: Input pollutant concentrations and weather data
2. **Load Sample Data**: Click "Load Sample Data" to try pre-configured examples
3. **Predict AQI**: Click "Predict AQI" to get the prediction
4. **View Results**: See the AQI value, category, and visualization chart
5. **Clear Form**: Use "Clear" to reset all inputs

## API Endpoints

### POST /api/predict

Predict AQI based on input parameters.

**Request Body:**
```json
{
  "pm25": 25.4,
  "pm10": 45.8,
  "no2": 35.6,
  "so2": 8.2,
  "co": 1.2,
  "o3": 85.3,
  "temperature": 28.1,
  "humidity": 68.5
}
```

**Response:**
```json
{
  "aqi": 89.2,
  "category": "Moderate",
  "color": "#FFFF00",
  "input_data": {
    "PM2.5": 25.4,
    "PM10": 45.8,
    ...
  }
}
```

### GET /api/sample-data

Get sample datasets for testing.

**Response:**
```json
[
  {
    "name": "Good Air Quality",
    "data": {
      "pm25": 8.5,
      "pm10": 15.2,
      ...
    }
  },
  ...
]
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_status": "loaded"
}
```

## Troubleshooting

### Common Issues

1. **Model files not found**
   ```
   Error: Model files not found. Please run model_train.py first.
   ```
   **Solution**: Run `python model_train.py` to generate the model files.

2. **CORS errors in browser**
   ```
   Access to fetch at 'http://localhost:5000' from origin 'null' has been blocked
   ```
   **Solution**: Make sure Flask server is running and flask-cors is installed.

3. **Port already in use**
   ```
   OSError: [Errno 48] Address already in use
   ```
   **Solution**: 
   - Kill the process using port 5000: `lsof -ti:5000 | xargs kill -9`
   - Or change the port in app.py: `app.run(debug=True, port=5001)`

4. **Module not found errors**
   ```
   ModuleNotFoundError: No module named 'sklearn'
   ```
   **Solution**: Install missing dependencies:
   ```bash
   pip install scikit-learn pandas numpy flask flask-cors joblib
   ```

5. **Prediction errors**
   ```
   Error: Invalid value for pm25: must be a number
   ```
   **Solution**: Ensure all input values are valid numbers within the specified ranges.

### Performance Issues

- If predictions are slow, consider reducing the number of estimators in the Random Forest model
- For production use, consider using a more efficient model or caching predictions
- Use a production WSGI server like Gunicorn instead of Flask's development server

## Customization

### Modifying the Model

To use a different ML algorithm, edit `model_train.py`:

```python
# Replace RandomForestRegressor with your preferred algorithm
from sklearn.ensemble import GradientBoostingRegressor

model = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    random_state=42
)
```

### Adding New Features

1. **Backend**: Add new parameters to the `/api/predict` endpoint in `app.py`
2. **Frontend**: Add new input fields to `index.html` and update `script.js`
3. **Model**: Retrain with additional features in `model_train.py`

### Styling Changes

Modify `style.css` to customize:
- Color schemes
- Layout and spacing
- Responsive breakpoints
- Animation effects

## Production Deployment

### Environment Setup

```bash
# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False

# Use a production server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python model_train.py

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Security Considerations

- Use HTTPS in production
- Implement rate limiting
- Add input validation and sanitization
- Use environment variables for sensitive configuration
- Regular security updates for dependencies

## Model Information

### Training Data

The model uses synthetic data generated with realistic distributions:
- **PM2.5**: Exponential distribution (λ=15), capped at 500 μg/m³
- **PM10**: Correlated with PM2.5 (1.2-2.5x ratio)
- **Weather**: Normal/uniform distributions with realistic correlations
- **AQI**: Calculated using EPA-style breakpoints (simplified)

### Model Performance

Typical performance metrics:
- **RMSE**: ~11-15 AQI points
- **R² Score**: ~0.92-0.95
- **Feature Importance**: PM2.5 and PM10 typically most important

### Model Limitations

- Trained on synthetic data, not real-world measurements
- Simplified AQI calculation compared to official EPA method
- Limited to 8 input features
- No temporal or spatial dependencies

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black *.py
flake8 *.py
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support and questions:

1. Check the troubleshooting section above
2. Review the API documentation
3. Check browser console for frontend errors
4. Verify Flask server logs for backend issues

## Changelog

### v1.0.0 (Initial Release)
- Basic AQI prediction functionality
- Flask REST API
- Interactive web interface
- Chart visualization
- Sample data integration
- Responsive design
