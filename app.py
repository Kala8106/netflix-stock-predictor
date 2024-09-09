from flask import Flask, render_template, request
import numpy as np
import pickle
from pymongo import MongoClient


app = Flask(__name__)

# Load the trained model from the pickle file
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

client = MongoClient('mongodb://localhost:27017/')
db = client['predictions']  # Change 'your_database' to your database name
collection = db['netflix_predictions']

@app.route('/')
def home():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        open_val = float(request.form['open'])
        high_val = float(request.form['high'])
        low_val = float(request.form['low'])
        volume_val = float(request.form['volume'])

        # Predict using the loaded model
        input_values = np.array([[open_val, high_val, low_val, volume_val]])
        predicted_close = model.predict(input_values)
        data = {
            'open': open_val,
            'high': high_val,
            'low': low_val,
            'volume': volume_val,
            'predicted_close': predicted_close[0]
        }
        collection.insert_one(data)

        return render_template('index.html', prediction=predicted_close[0])

if __name__ == '__main__':
    app.run(debug=True)