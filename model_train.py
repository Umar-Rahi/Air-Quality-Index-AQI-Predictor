import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')

def calculate_aqi(pm25, pm10, no2, so2, co, o3):
    """
    Calculate AQI based on pollutant concentrations
    Simplified AQI calculation for demonstration
    """
    # AQI breakpoints and corresponding concentration ranges
    # This is a simplified version - real AQI calculation is more complex
    
    # PM2.5 AQI calculation (µg/m³)
    if pm25 <= 12:
        aqi_pm25 = pm25 * 50 / 12
    elif pm25 <= 35.4:
        aqi_pm25 = 50 + (pm25 - 12) * 50 / (35.4 - 12)
    elif pm25 <= 55.4:
        aqi_pm25 = 100 + (pm25 - 35.4) * 50 / (55.4 - 35.4)
    elif pm25 <= 150.4:
        aqi_pm25 = 150 + (pm25 - 55.4) * 100 / (150.4 - 55.4)
    elif pm25 <= 250.4:
        aqi_pm25 = 200 + (pm25 - 150.4) * 100 / (250.4 - 150.4)
    else:
        aqi_pm25 = 300 + (pm25 - 250.4) * 200 / (500.4 - 250.4)
    
    # PM10 AQI calculation (µg/m³)
    if pm10 <= 54:
        aqi_pm10 = pm10 * 50 / 54
    elif pm10 <= 154:
        aqi_pm10 = 50 + (pm10 - 54) * 50 / (154 - 54)
    elif pm10 <= 254:
        aqi_pm10 = 100 + (pm10 - 154) * 50 / (254 - 154)
    elif pm10 <= 354:
        aqi_pm10 = 150 + (pm10 - 254) * 100 / (354 - 254)
    elif pm10 <= 424:
        aqi_pm10 = 200 + (pm10 - 354) * 100 / (424 - 354)
    else:
        aqi_pm10 = 300 + (pm10 - 424) * 200 / (604 - 424)
    
    # Simplified calculations for other pollutants
    # NO2 (ppb)
    aqi_no2 = min(no2 * 2, 500)
    
    # SO2 (ppb)
    aqi_so2 = min(so2 * 3, 500)
    
    # CO (ppm)
    aqi_co = min(co * 50, 500)
    
    # O3 (ppb)
    aqi_o3 = min(o3 * 1.5, 500)
    
    # Return the maximum AQI (dominant pollutant)
    return max(aqi_pm25, aqi_pm10, aqi_no2, aqi_so2, aqi_co, aqi_o3)

def generate_synthetic_data(n_samples=5000):
    """Generate synthetic air quality data for training"""
    np.random.seed(42)
    
    # Generate realistic air quality parameters
    pm25 = np.random.exponential(15, n_samples)  # PM2.5 (µg/m³)
    pm10 = pm25 * np.random.uniform(1.2, 2.5, n_samples)  # PM10 usually higher than PM2.5
    no2 = np.random.exponential(20, n_samples)  # NO2 (ppb)
    so2 = np.random.exponential(5, n_samples)   # SO2 (ppb)
    co = np.random.exponential(1, n_samples)    # CO (ppm)
    o3 = np.random.exponential(30, n_samples)   # O3 (ppb)
    
    # Weather parameters
    temperature = np.random.normal(25, 10, n_samples)  # Temperature (°C)
    humidity = np.random.uniform(30, 90, n_samples)    # Humidity (%)
    
    # Add some correlations for realism
    # Higher temperature can increase O3
    o3 += temperature * 0.5 + np.random.normal(0, 5, n_samples)
    o3 = np.maximum(o3, 0)
    
    # Higher humidity can affect particulate matter
    pm25 += humidity * 0.1 + np.random.normal(0, 2, n_samples)
    pm25 = np.maximum(pm25, 0)
    
    # Cap values at realistic maximums
    pm25 = np.minimum(pm25, 500)
    pm10 = np.minimum(pm10, 600)
    no2 = np.minimum(no2, 200)
    so2 = np.minimum(so2, 100)
    co = np.minimum(co, 50)
    o3 = np.minimum(o3, 300)
    
    # Calculate AQI for each sample
    aqi_values = []
    for i in range(n_samples):
        aqi = calculate_aqi(pm25[i], pm10[i], no2[i], so2[i], co[i], o3[i])
        aqi_values.append(aqi)
    
    # Create DataFrame
    data = pd.DataFrame({
        'PM2.5': pm25,
        'PM10': pm10,
        'NO2': no2,
        'SO2': so2,
        'CO': co,
        'O3': o3,
        'Temperature': temperature,
        'Humidity': humidity,
        'AQI': aqi_values
    })
    
    return data

def train_model():
    """Train the AQI prediction model"""
    print("Generating synthetic air quality data...")
    data = generate_synthetic_data()
    
    print(f"Dataset shape: {data.shape}")
    print(f"AQI range: {data['AQI'].min():.2f} - {data['AQI'].max():.2f}")
    
    # Features and target
    features = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'Temperature', 'Humidity']
    X = data[features]
    y = data['AQI']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    
    # Evaluate model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Performance:")
    print(f"MSE: {mse:.2f}")
    print(f"R2 Score: {r2:.4f}")
    print(f"RMSE: {np.sqrt(mse):.2f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    # Save sample training data
    data.head(20).to_csv("sample_training_data.csv", index=False)

    # Save feature importance
    feature_importance.to_csv("feature_importance.csv", index=False)

    # Save model summary to text file
    with open("model_summary.txt", "w") as f:
        f.write("Random Forest Regressor Model\n")
        f.write(f"R2 Score: {r2:.4f}\n")
        f.write(f"MSE: {mse:.2f}\n")
        f.write(f"RMSE: {np.sqrt(mse):.2f}\n\n")
        f.write("Feature Importance:\n")
        f.write(feature_importance.to_string(index=False))

    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Save the model and scaler
    print("\nSaving model and scaler...")
    joblib.dump(model, 'aqi_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    
    print("Model training completed successfully!")
    print("Files saved: aqi_model.pkl, scaler.pkl")
    
    return model, scaler

if __name__ == "__main__":
    train_model()