import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class WearTearModel:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.labels = ['heavily worn', 'lightly worn', 'not worn']

    def predict(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        preds = self.model.predict(img_array)
        index = np.argmax(preds)
        return self.labels[index]
    
try:
    model = load_model('path/to/your/model.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None