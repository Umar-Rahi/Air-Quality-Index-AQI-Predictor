# Air Quality Index (AQI) Predictor

A full-stack machine-learning web application that estimates the Air Quality Index (AQI) from pollutant concentrations and basic weather measurements. It combines a Flask API, a Random Forest regression model, and a responsive web interface with pollutant-level visualisation.

<p align="center">
  <a href="https://air-quality-index-aqi-predictor-2-6tr8.onrender.com"><strong>🌐 Open Live Demo</strong></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/Umar-Rahi/Air-Quality-Index-AQI-Predictor"><strong>Source Code</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Deployment-Render-46E3B7?logo=render&logoColor=black" alt="Render">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</p>

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Run Locally](#run-locally)
- [Deploy on Render](#deploy-on-render)
- [Using the Application](#using-the-application)
- [API Reference](#api-reference)
- [AQI Categories](#aqi-categories)
- [Model Details and Limitations](#model-details-and-limitations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **AQI estimation:** Predicts an AQI value and a corresponding air-quality category from eight input features.
- **Machine-learning model:** Uses a Random Forest Regressor with feature scaling.
- **Flask REST API:** Provides prediction, sample-data, and health-check endpoints.
- **Interactive interface:** Enter pollutant and weather values, load sample scenarios, and view prediction results.
- **Data visualisation:** Displays the entered pollutant and weather values in a Chart.js bar chart.
- **Prediction logging:** Appends successful prediction inputs and results to `aqi_prediction_log.csv`.
- **Responsive layout:** Built with Bootstrap and custom CSS for desktop and mobile screens.

## Technology Stack

| Area | Technologies |
|---|---|
| Backend | Python, Flask, Flask-CORS |
| Machine learning | scikit-learn, Random Forest Regressor, StandardScaler |
| Data processing | NumPy, pandas |
| Model persistence | joblib |
| Frontend | HTML5, CSS3, JavaScript |
| UI and charts | Bootstrap 5, Font Awesome, Chart.js |
| Production server | Gunicorn |
| Hosting | Render |

## How It Works

1. The training script generates a synthetic dataset of air-pollution and weather values.
2. It calculates a simplified target AQI for each generated row.
3. A StandardScaler is fitted to the training features.
4. A Random Forest Regressor is trained on the scaled features.
5. The trained model and scaler are saved as `aqi_model.pkl` and `scaler.pkl`.
6. The Flask API loads those files and uses them to make predictions from submitted input values.
7. The frontend displays the returned AQI, category, description, and a chart of the submitted measurements.

## Project Structure

```text
Air-Quality-Index-AQI-Predictor/
├── app.py                    # Flask application and API endpoints
├── model_train.py            # Synthetic data generation and model training
├── requirements.txt          # Python dependencies
├── index.html                # Frontend page
├── style.css                 # Frontend styling
├── script.js                 # Form handling, API calls, and Chart.js
├── LICENSE                   # MIT license
├── README.md                 # Project documentation
├── aqi_model.pkl             # Generated trained model (created during training)
├── scaler.pkl                # Generated feature scaler (created during training)
├── sample_training_data.csv  # Generated sample of training data
├── feature_importance.csv    # Generated feature importance report
├── model_summary.txt         # Generated model metrics and summary
└── aqi_prediction_log.csv    # Created after successful predictions
```

The generated model, scaler, training reports, and prediction log are created when the relevant scripts run; they do not need to be manually added to the repository.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Umar-Rahi/Air-Quality-Index-AQI-Predictor.git
cd Air-Quality-Index-AQI-Predictor
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Train the model

```bash
python model_train.py
```

Training generates the model files used by the API:

- `aqi_model.pkl`
- `scaler.pkl`

It also writes `sample_training_data.csv`, `feature_importance.csv`, and `model_summary.txt`.

### 5. Start the Flask application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

> **Local API note:** The committed frontend is configured to use the deployed Render API. To send requests to your local Flask server during local development, set `this.apiBaseUrl` near the top of `script.js` to `'/api'`.

## Deploy on Render

This repository is configured for deployment as a Python Web Service on Render.

1. Create a new **Web Service** in Render and connect this GitHub repository.
2. Select the `main` branch and **Python 3**.
3. Leave **Root Directory** blank.
4. Use the following build command:

   ```bash
   pip install -r requirements.txt && python model_train.py
   ```

5. Use the following start command:

   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. No application-specific environment variables are required for the current setup.
7. Deploy the service. The build command installs dependencies and trains the model; Gunicorn then starts the Flask application.

**Live service:** [https://air-quality-index-aqi-predictor-2-6tr8.onrender.com](https://air-quality-index-aqi-predictor-2-6tr8.onrender.com)

Render free instances may spin down after inactivity, so the first request after a period of inactivity can take longer while the service starts.

## Using the Application

1. Open the [live application](https://air-quality-index-aqi-predictor-2-6tr8.onrender.com).
2. Enter the pollutant and weather values, or choose **Load Sample Data**.
3. Select **Predict AQI**.
4. Review the AQI estimate, category, explanatory message, and pollutant chart.
5. Use **Clear** to reset the form.

### Input Parameters

| Parameter | Unit | Frontend input range | Description |
|---|---:|---:|---|
| PM2.5 | µg/m³ | 0–500 | Fine particulate matter |
| PM10 | µg/m³ | 0–600 | Coarse particulate matter |
| NO₂ | ppb | 0–200 | Nitrogen dioxide |
| SO₂ | ppb | 0–100 | Sulfur dioxide |
| CO | ppm | 0–50 | Carbon monoxide |
| O₃ | ppb | 0–300 | Ozone |
| Temperature | °C | -50–60 | Ambient temperature |
| Humidity | % | 0–100 | Relative humidity |

> **Validation note:** The current backend rejects negative values for every input, including temperature. Therefore, temperatures below 0°C are displayed as in-range by the form but are rejected by the API. Use a temperature from 0°C to 60°C until backend validation is updated.

## API Reference

The API base URL for the live service is:

```text
https://air-quality-index-aqi-predictor-2-6tr8.onrender.com/api
```

### `POST /api/predict`

Predicts AQI from the eight required input values.

**Request:**

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

**Example response:**

```json
{
  "aqi": 89.2,
  "category": "Moderate",
  "color": "#FFFF00",
  "input_data": {
    "PM2.5": 25.4,
    "PM10": 45.8,
    "NO2": 35.6,
    "SO2": 8.2,
    "CO": 1.2,
    "O3": 85.3,
    "Temperature": 28.1,
    "Humidity": 68.5
  }
}
```

The values above illustrate the response format; actual predictions depend on the trained model.

**Example cURL request:**

```bash
curl -X POST "https://air-quality-index-aqi-predictor-2-6tr8.onrender.com/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "pm25": 25.4,
    "pm10": 45.8,
    "no2": 35.6,
    "so2": 8.2,
    "co": 1.2,
    "o3": 85.3,
    "temperature": 28.1,
    "humidity": 68.5
  }'
```

**Common response codes:**

| Code | Meaning |
|---|---|
| 200 | Prediction completed |
| 400 | Missing, invalid, or malformed input |
| 500 | Model unavailable or prediction failed |

### `GET /api/sample-data`

Returns the sample input scenarios used by the **Load Sample Data** feature.

[Open sample data endpoint](https://air-quality-index-aqi-predictor-2-6tr8.onrender.com/api/sample-data)

### `GET /api/health`

Returns the application status and whether the model and scaler are loaded.

[Open health-check endpoint](https://air-quality-index-aqi-predictor-2-6tr8.onrender.com/api/health)

A healthy response should report:

```json
{
  "status": "healthy",
  "model_status": "loaded"
}
```

## AQI Categories

The application maps model predictions to these categories:

| AQI value | Category |
|---:|---|
| 0–50 | Good |
| 51–100 | Moderate |
| 101–150 | Unhealthy for Sensitive Groups |
| 151–200 | Unhealthy |
| 201–300 | Very Unhealthy |
| 301–500 | Hazardous |

## Model Details and Limitations

- **Algorithm:** Random Forest Regressor with 100 estimators and a maximum tree depth of 15.
- **Features:** PM2.5, PM10, NO₂, SO₂, CO, O₃, temperature, and humidity.
- **Preprocessing:** StandardScaler is fitted on the training split and reused for prediction.
- **Training data:** The current training script generates 5,000 synthetic samples using NumPy distributions; it does not download real-time or monitoring-station data.
- **AQI calculation:** The target values are produced by a simplified, project-specific calculation. They are not an official regulatory AQI measurement.
- **Scope:** The model does not account for location, time trends, weather forecasts, or sensor calibration.

**Important:** This project is intended for learning and demonstration. Predictions should not be used as a substitute for official air-quality readings, medical advice, or regulatory reporting.

## Troubleshooting

| Issue | What to check |
|---|---|
| `Model files not found` | Run `python model_train.py` before starting the app. On Render, confirm that the build command includes `python model_train.py`. |
| `Failed to fetch` in the browser | Confirm that the Render service is live, the frontend is using the Render API URL in `script.js`, and the latest frontend commit has been deployed. |
| `model_status: not loaded` | Check Render logs for model-loading errors and confirm that `aqi_model.pkl` and `scaler.pkl` were generated during the build. |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements.txt`. |
| Port already in use locally | Stop the process using port 5000, or change the local port in the `app.run(...)` line in `app.py`. |
| First request is slow | A free Render instance may have been idle and need time to start. |

For deployment issues, check the Render service's **Logs** page. For browser-side issues, open Developer Tools and inspect the **Console** and **Network** tabs.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Commit your changes with a clear message.
5. Open a pull request describing the improvement.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Umar Rahi**

- GitHub: [@Umar-Rahi](https://github.com/Umar-Rahi)
- LinkedIn: [Umar Rahi](https://www.linkedin.com/in/umar-rahi/)
- Portfolio: [umar-rahi.github.io](https://umar-rahi.github.io/umar-rahi-portfolio/)
