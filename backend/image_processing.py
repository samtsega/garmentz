from tensorflow.keras.preprocessing import image
import numpy as np

def preprocess_image(img_path: str):
    """
    Loads and preprocesses an image for model input.
    Resize to (224, 224), normalize pixel values.
    """
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)
