import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Update this to your dataset pathimport os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

train_dir = "dataset/FaceAuthentication/train"
test_dir = "dataset/FaceAuthentication/test"

img_size = (224,224)
batch_size = 16

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

num_classes = len(train_data.class_indices)

model = models.Sequential([
    layers.Conv2D(32,(3,3),activation="relu",input_shape=(224,224,3)),
    layers.MaxPooling2D(),

    layers.Conv2D(64,(3,3),activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128,(3,3),activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(128,activation="relu"),
    layers.Dense(num_classes,activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_data,
    validation_data=test_data,
    epochs=10
)

os.makedirs("app/models",exist_ok=True)

model.save("app/models/your_cnn_model.keras")

labels = train_data.class_indices

with open("app/models/class_labels.txt","w") as f:
    for label in labels:
        f.write(label+"\n")

print("Model training completed")
