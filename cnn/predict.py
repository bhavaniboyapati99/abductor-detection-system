import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import current_app

def predict_image_class(img_path):
    """
    Predict the class of a given image using the CNN model.

    Args:
        img_path (str): Full path to the image to classify.

    Returns:
        tuple: (predicted_class: str, confidence: float or None)
    """
    # Paths to model and label files
    model_path = os.path.join(current_app.root_path, "models", "your_cnn_model.keras")
    labels_path = os.path.join(current_app.root_path, "models", "class_labels.txt")

    # Ensure model exists
    if not os.path.exists(model_path):
        print("❌ Model file not found")
        return "Unknown", None

    # Load model
    model = load_model(model_path)

    # Load class labels
    if not os.path.exists(labels_path):
        print("❌ Labels file not found")
        return "Unknown", None

    with open(labels_path, "r") as f:
        class_names = [line.strip() for line in f]

    # Load and preprocess image
    try:
        img = image.load_img(img_path, target_size=(64, 64))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
    except Exception as e:
        print(f"❌ Failed to preprocess image: {e}")
        return "Unknown", None

    # Predict
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_index])

    # Confidence threshold
    if confidence < 0.5:
        print(f"❌ Low confidence ({confidence:.2f}) — returning Unknown")
        return "Unknown", None

    predicted_class = class_names[predicted_index]
    return predicted_class, round(confidence, 2)
