from tensorflow.keras.models import load_model

model = load_model("app/models/your_cnn_model.keras")

print("Model loaded successfully")
print(model.summary())