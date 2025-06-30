import os
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# Configurations
IMAGE_DIR = 'static/'
LABELS_CSV = 'csv/dataset.csv'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20

def load_data(image_dir, dataset_csv):
    df = pd.read_csv(dataset_csv)
    images = []
    labels = []

    # Map text labels to numeric values
    wear_signs_mapping = {
        'not worn': 0.0,
        'lightly worn': 0.5,
        'heavily worn': 1.0
    }

    for _, row in df.iterrows():
        img_path = os.path.join(image_dir, row['image_name'])
        if os.path.exists(img_path):
            img = load_img(img_path, target_size=IMAGE_SIZE)
            img_array = img_to_array(img) / 255.0  # Normalize pixel values
            images.append(img_array)

            wear_text = str(row['wear_signs']).strip().lower()
            label = wear_signs_mapping.get(wear_text, 0.0)  # Default to 0.0 if unknown
            labels.append(label)
        else:
            print(f"Warning: Image {img_path} not found.")

    X = np.array(images)
    y = np.array(labels)
    return X, y

def build_model(input_shape=(224, 224, 3)):
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(1, activation='linear')  # Regression output
    ])
    model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mae'])
    return model

def main():
    print("Loading data...")
    X, y = load_data(IMAGE_DIR, LABELS_CSV)
    print(f"Loaded {len(X)} images.")

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = build_model(input_shape=IMAGE_SIZE + (3,))
    model.summary()

    print("Training model...")
    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE
    )

    os.makedirs('model', exist_ok=True)
    model.save('model/depreciation_model.h5')
    print("Model saved as model/depreciation_model.h5")

# Fallback rule-based depreciation function (unchanged)
def calculate_depreciation(brand, fabric, age_years, wear_level_score):
    brand_score = 0.8 if brand.lower() in ['gucci', 'prada', 'lv'] else 0.6
    fabric_score = 0.9 if fabric.lower() in ['leather', 'wool'] else 0.7
    age_score = max(0, 1 - (age_years / 10))
    wear_score = 1 - wear_level_score
    depreciation = brand_score * fabric_score * age_score * wear_score
    return round(depreciation, 3)

if __name__ == '__main__':
    main()
