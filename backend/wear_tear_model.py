import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array

class WearTearModel:
    def __init__(self, model_path):
        try:
            self.model = load_model(model_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
        self.labels = ['heavily worn', 'lightly worn', 'not worn']

    def predict(self, img_path):
        if self.model is None:
            return "Model not loaded."
        img = load_img(img_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        preds = self.model.predict(img_array)
        index = np.argmax(preds)
        return self.labels[index]

# Example usage:
# model = WearTearModel('models/wear_tear_model.h5')
# result = model.predict('test_images/shirt.jpg')
# print(result)
