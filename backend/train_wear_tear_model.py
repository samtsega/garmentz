from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import numpy as np
from PIL import Image
import logging
import requests
from functools import lru_cache

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Azure Container SAS URL (read+write)
AZURE_CONTAINER_SAS = (
    "https://garmentzstorage.blob.core.windows.net/models"
    "?sp=rw&st=2025-07-01T01:04:29Z&se=2026-07-01T09:04:29Z&spr=https&sv=2024-11-04&sr=c"
    "&sig=v7ZIyeKfBumJW%2BhAKPPlIO27mi25DAY4rkiY%2FWsAM%2FA%3D"
)

# Depreciation model URL (read access)
DEPRECIATION_MODEL_URL = (
    "https://garmentzstorage.blob.core.windows.net/models/depreciation_model.h5"
    "?sp=r&st=2025-07-01T01:06:38Z&se=2026-07-01T09:06:38Z&spr=https&sv=2024-11-04&sr=b"
    "&sig=249jXOFpeAGQv3q7j%2FGuLGUs4%2B7vsyD192PuTyc4PeQ%3D"
)

# Wear model URL (read access)
WEAR_MODEL_URL = (
    "https://garmentzstorage.blob.core.windows.net/models/wear_tear_model.h5"
    "?sp=r&st=2025-07-01T01:08:23Z&se=2026-07-01T09:08:23Z&spr=https&sv=2024-11-04&sr=b"
    "&sig=tIABznfTRpTQyyy6poBENuPdwwRvrv2zI0JnkgyTPBA%3D"
)

# Load wear model
try:
    wear_model_path = "models/wear_tear_model.h5"
    os.makedirs("models", exist_ok=True)
    if not os.path.exists(wear_model_path):
        logger.info("Downloading wear model...")
        resp = requests.get(WEAR_MODEL_URL, timeout=60)
        resp.raise_for_status()
        with open(wear_model_path, "wb") as f:
            f.write(resp.content)
        logger.info("Wear model downloaded.")
    wear_model = load_model(wear_model_path)
    logger.info("Wear model loaded successfully.")
except Exception as e:
    logger.warning(f"Wear model load failed: {e}")
    wear_model = None

# Load depreciation model
try:
    depreciation_model_path = "models/depreciation_model.h5"
    if not os.path.exists(depreciation_model_path):
        logger.info("Downloading depreciation model...")
        resp = requests.get(DEPRECIATION_MODEL_URL, timeout=60)
        resp.raise_for_status()
        with open(depreciation_model_path, "wb") as f:
            f.write(resp.content)
        logger.info("Depreciation model downloaded.")
    depreciation_model = load_model(depreciation_model_path)
    logger.info("Depreciation model loaded successfully.")
except Exception as e:
    logger.error(f"Depreciation model load failed: {e}")
    depreciation_model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path, size=(224, 224)):
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize(size, Image.Resampling.LANCZOS)
            arr = np.array(img) / 255.0
            return np.expand_dims(arr, axis=0)
    except Exception as e:
        logger.error(f"Preprocessing error: {e}")
        return None

def analyze_wear(image_path):
    if wear_model is None:
        return 0.3
    arr = preprocess_image(image_path)
    if arr is None:
        return 0.5
    pred = wear_model.predict(arr, verbose=0)
    val = float(pred[0][0]) if pred.ndim > 1 else float(pred[0])
    return round(max(0, min(1, val)), 3)

def predict_depreciation(image_path):
    if depreciation_model is None:
        return 0.5
    arr = preprocess_image(image_path)
    if arr is None:
        return 0.5
    pred = depreciation_model.predict(arr, verbose=0)
    val = float(pred[0][0]) if pred.ndim > 1 else float(pred[0])
    return round(max(0, min(1, val)), 3)

def upload_to_azure(file_path, blob_name):
    try:
        with open(file_path, "rb") as f:
            headers = {
                "x-ms-blob-type": "BlockBlob",
                "Content-Type": "application/octet-stream"
            }
            blob_url = f"{AZURE_CONTAINER_SAS.split('?')[0]}/{blob_name}?{AZURE_CONTAINER_SAS.split('?')[1]}"
            resp = requests.put(blob_url, headers=headers, data=f)
            if resp.status_code in (201, 202):
                return blob_url
            logger.error(f"Azure upload failed: {resp.text}")
            return None
    except Exception as e:
        logger.error(f"Azure upload error: {e}")
        return None

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['image']
    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(local_path)

    wear_score = analyze_wear(local_path)
    depreciation_score = predict_depreciation(local_path)
    blob_url = upload_to_azure(local_path, filename)

    return jsonify({
        'success': True,
        'wear_level_score': wear_score,
        'depreciation_score': depreciation_score,
        'azure_blob_url': blob_url,
        'message': 'Image analyzed and uploaded.'
    })

@app.route('/convert-currency', methods=['POST'])
def convert_currency():
    try:
        data = request.get_json()
        amount = float(data['amount'])
        base = data['base_currency'].upper()
        target = data['target_currency'].upper()

        if base == target:
            return jsonify({'converted_amount': amount, 'exchange_rate': 1.0})

        rate = get_exchange_rate(base, target)
        if rate is None:
            return jsonify({'error': 'Exchange rate fetch failed'}), 500

        return jsonify({
            'converted_amount': round(amount * rate, 2),
            'exchange_rate': rate
        })
    except Exception as e:
        logger.error(f"Currency conversion error: {e}")
        return jsonify({'error': 'Invalid request'}), 400

@lru_cache(maxsize=128)
def get_exchange_rate(base, target):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json().get('rates', {}).get(target)

@app.route('/ebay-notify', methods=['GET', 'POST'])
def ebay_notify():
    # Add ngrok-skip-browser-warning header for eBay verification
    if request.method == 'GET':
        # eBay verification challenge
        challenge = request.args.get('challenge_code')
        if challenge:
            logger.info(f"eBay verification challenge received: {challenge}")
            # Must return EXACTLY the challenge code as plain text
            response = app.response_class(
                response=challenge,
                status=200,
                mimetype='text/plain'
            )
            return response
        else:
            logger.warning("GET request without challenge_code")
            return "Challenge code required", 400

    elif request.method == 'POST':
        try:
            # Handle eBay notifications
            content_type = request.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                payload = request.get_json()
            elif 'application/xml' in content_type or 'text/xml' in content_type:
                payload = request.data.decode('utf-8')
            else:
                payload = request.data
            
            logger.info(f"eBay notification received: {payload}")
            
            # Process the notification here
            # (item sold, listing ended, etc.)
            
            # eBay expects a 200 OK response
            return '', 200
            
        except Exception as e:
            logger.error(f"eBay notification processing error: {e}")
            # Still return 200 to avoid eBay retries
            return '', 200

# Alternative endpoint path (some developers prefer this)
@app.route('/webhooks/ebay', methods=['GET', 'POST'])
def ebay_webhook():
    return ebay_notify()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'wear_model_loaded': wear_model is not None,
        'depreciation_model_loaded': depreciation_model is not None
    })

if __name__ == '__main__':
    logger.info("Starting server...")
    app.run(host='0.0.0.0', port=5050, debug=True)