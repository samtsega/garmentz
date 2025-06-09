import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class DepreciationModel:
    def __init__(self, model_path: str = None):
        try:
            self.model = load_model(model_path) if model_path else None
            print("Depreciation model loaded.")
        except Exception as e:
            print(f"Warning: Could not load model. Using rule-based fallback. Error: {e}")
            self.model = None

    def predict(self, img_path: str) -> float:
        """
        Predicts depreciation percentage using the ML model (e.g., 0.25 for 25% loss).
        """
        if not self.model:
            raise ValueError("Model not loaded. Cannot predict.")
        
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = self.model.predict(img_array)
        return round(float(prediction[0][0]), 2)

    def calculate_depreciation(self, brand, fabric, age_years, wear_level_score) -> float:
        """
        Rule-based depreciation scoring fallback.
        """
        brand_score = 0.8 if brand.lower() in ['gucci', 'prada', 'lv'] else 0.6
        fabric_score = 0.9 if fabric.lower() in ['leather', 'wool'] else 0.7
        age_score = max(0, 1 - (age_years / 10))  # 10% value loss per year
        wear_score = 1 - wear_level_score        # wear level between 0 (new) and 1 (worn)

        depreciation = brand_score * fabric_score * age_score * wear_score
        return round(depreciation, 3)
