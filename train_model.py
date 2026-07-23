import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import json
import matplotlib.pyplot as plt

# ================= DATASET PATH =================
dataset_path = "dataset"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ================= DATA AUGMENTATION =================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=25,
    zoom_range=0.2,
    horizontal_flip=True,
    shear_range=0.2,
    brightness_range=[0.8, 1.2]
)

val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# ================= TRAIN DATA =================
train_data = train_datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

# ================= VALIDATION DATA =================
val_data = val_datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# ================= SAVE CLASS MAPPING =================
class_indices = train_data.class_indices

with open("class_indices.json", "w") as f:
    json.dump(class_indices, f)

print("Class mapping saved:")
print(class_indices)

# ================= TRANSFER LEARNING MODEL =================
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False  # freeze base model

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(train_data.num_classes, activation='softmax')
])

# ================= COMPILE =================
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ================= TRAIN =================
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=25
)

# ================= SAVE MODEL =================
model.save("plant_model.h5")
print("Model saved successfully!")

# ================= ACCURACY GRAPH =================
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'])
plt.show()