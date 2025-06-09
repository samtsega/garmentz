import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import numpy as np
from keras.models import load_model
from PIL import Image
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = load_model('wear_tear_model.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ebay_item_details(ebay_item_id):
    # Stubbed function — replace with actual eBay API call logic
    # Sample mock return
    return {
        "brand": "Nike",
        "purchase_date": "2020-05-01",
        "price": 120.00
    }

def compute_depreciation_score(purchase_date, wear_score, original_price):
    current_year = datetime.now().year
    try:
        purchase_year = datetime.strptime(purchase_date, "%Y-%m-%d").year
    except:
        purchase_year = current_year

    age_factor = (current_year - purchase_year) / 10
    wear_factor = wear_score / 10
    price_factor = min(1, original_price / 1000)

    depreciation_score = 1 - (0.5 * age_factor + 0.3 * wear_factor + 0.2 * price_factor)
    return round(max(depreciation_score, 0), 2)

def preprocess_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)

def get_condition_score(prediction_class):
    if prediction_class == 'not worn':
        return 1  # Best condition
    elif prediction_class == 'lightly worn':
        return 5
    elif prediction_class == 'heavily worn':
        return 9  # Worst condition
    return 5

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    ebay_item_id = request.form.get('ebay_item_id', None)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        image_data = preprocess_image(filepath)
        prediction = model.predict(image_data)
        predicted_class_index = np.argmax(prediction)
        class_names = ['heavily worn', 'lightly worn', 'not worn']
        predicted_class = class_names[predicted_class_index]

        wear_score = get_condition_score(predicted_class)

        ebay_data = get_ebay_item_details(ebay_item_id) if ebay_item_id else {
            "brand": "Unknown",
            "purchase_date": "2021-01-01",
            "price": 100.00
        }

        depreciation_score = compute_depreciation_score(
            ebay_data['purchase_date'], wear_score, ebay_data['price']
        )

        os.remove(filepath)

        return jsonify({
            'predicted_class': predicted_class,
            'wear_score': wear_score,
            'depreciation_score': depreciation_score,
            'ebay_data': ebay_data
        })
    else:
        return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
