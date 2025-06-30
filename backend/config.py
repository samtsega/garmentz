import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    WEAR_TEAR_MODEL_PATH = os.path.join(BASE_DIR, 'model', 'wear_tear_model.h5')

    # eBay API configs (replace with real values)
    EBAY_APP_ID = 'YOUR_EBAY_APP_ID'
    EBAY_CERT_ID = 'YOUR_EBAY_CERT_ID'
    EBAY_DEV_ID = 'YOUR_EBAY_DEV_ID'
