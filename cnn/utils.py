# cnn/utils.py

import os
import numpy as np
from flask import current_app, g
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def get_model():
    if 'model' not in g:
        model_path = os.path.join(current_app.root_path, 'app', 'models', 'your_cnn_model.keras')
        print("✅ Loading model from:", model_path)
        g.model = load_model(model_path)
    return g.model

def get_class_labels():
    if 'class_labels' not in g:
        labels_path = os.path.join(current_app.root_path, 'app', 'models', 'class_labels.txt')
        with open(labels_path, 'r') as f:
            g.class_labels = [line.strip() for line in f]
    return g.class_labels

def preprocess_image(img_path, target_size=(64, 64)):
    """
    Load and preprocess an image for CNN model prediction.
    """
    try:
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"❌ Error preprocessing image: {e}")
        raise e
