from flask import Flask, request, jsonify
from keras.models import load_model

app = Flask(__name__)

# Attempt to load wear & tear model (optional)
try:
    wear_model = load_model("models/wear_tear_model.h5")
    print("Wear & Tear model loaded successfully.")
except Exception as e:
    print(f"Error loading wear model: {e}")
    wear_model = None

# Depreciation function (can be moved to a service)
def calculate_depreciation(brand, fabric, age_years, wear_level_score):
    brand_score = 0.8 if brand.lower() in ['gucci', 'prada', 'lv'] else 0.6
    fabric_score = 0.9 if fabric.lower() in ['leather', 'wool'] else 0.7
    age_score = max(0, 1 - (age_years / 10))
    wear_score = 1 - wear_level_score

    depreciation = brand_score * fabric_score * age_score * wear_score
    return round(depreciation, 3)

# Example API route
@app.route('/depreciation', methods=['POST'])
def get_depreciation():
    data = request.get_json()

    required_fields = ['brand', 'fabric', 'age_years', 'wear_level_score']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing one or more required fields'}), 400

    score = calculate_depreciation(
        brand=data['brand'],
        fabric=data['fabric'],
        age_years=float(data['age_years']),
        wear_level_score=float(data['wear_level_score'])
    )

    return jsonify({'depreciation_score': score})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
