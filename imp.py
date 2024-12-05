from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd

app = Flask(__name__)

# Example dataset with climatic parameters (as before)
data = {
    'Temperature': [25, 30, 22, 35, 28, 24, 26, 33, 20, 27],
    'Rainfall': [200, 150, 120, 100, 300, 180, 220, 110, 350, 210],
    'Humidity': [80, 60, 75, 40, 50, 65, 70, 45, 85, 60],
    'SoilType': ['Loamy', 'Sandy', 'Clay', 'Loamy', 'Sandy', 'Loamy', 'Clay', 'Sandy', 'Clay', 'Loamy'],
    'Crop': ['Wheat', 'Rice', 'Maize', 'Wheat', 'Rice', 'Wheat', 'Maize', 'Rice', 'Maize', 'Wheat']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert categorical feature (SoilType) into numeric values
df['SoilType'] = df['SoilType'].map({'Loamy': 0, 'Sandy': 1, 'Clay': 2})

# Features and target variable
X = df[['Temperature', 'Rainfall', 'Humidity', 'SoilType']]
y = df['Crop']

# Train model
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y)

@app.after_request
def after_request(response):
    """Manually add CORS headers"""
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'  # Allow these methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'  # Allow specific headers
    return response

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()  # Get input data from the request
        # Extract values from the incoming JSON
        temperature = data['Temperature']
        rainfall = data['Rainfall']
        humidity = data['Humidity']
        soil_type = data['SoilType']

        # Prepare input for prediction
        input_data = [[temperature, rainfall, humidity, soil_type]]

        # Scale the input
        input_scaled = scaler.transform(input_data)

        # Make prediction
        predicted_crop = model.predict(input_scaled)[0]

        # Suggest sustainable farming method based on the predicted crop
        sustainable_method = suggest_sustainable_method(predicted_crop, temperature, rainfall, humidity)

        return jsonify({'predicted_crop': predicted_crop, 'sustainable_method': sustainable_method})

    except Exception as e:
        return jsonify({'error': str(e)})

# Function to suggest sustainable farming methods
def suggest_sustainable_method(predicted_crop, temperature, rainfall, humidity):
    farming_methods = {
        'Wheat': 'Use organic fertilizers, Crop rotation, Drip irrigation',
        'Rice': 'Use integrated pest management, Wetland rice farming, Organic fertilizers',
        'Maize': 'Use drought-resistant varieties, Conservation tillage, Mulching'
    }

    # Suggest methods based on climate conditions
    if rainfall < 150:
        farming_methods[predicted_crop] += ', Implement rainwater harvesting techniques'
    if humidity > 70:
        farming_methods[predicted_crop] += ', Focus on integrated pest management'
    if temperature > 30:
        farming_methods[predicted_crop] += ', Implement water-efficient irrigation techniques like drip irrigation'

    return farming_methods.get(predicted_crop, 'No sustainable methods found for this crop')

if __name__ == '__main__':
    app.run(debug=True)
