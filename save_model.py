import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Create simple CNN model
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')  # for 10 classes dummy example
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# For demo, we won't train the model; just save it
save_path = "app/models/your_cnn_model.keras"

# Make sure the directory exists
os.makedirs(os.path.dirname(save_path), exist_ok=True)

model.save(save_path)
print(f"Model saved to {save_path}")
