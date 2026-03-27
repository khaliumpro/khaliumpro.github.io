"""
============================================================
Lesson 2 (Part 2): Iris Flower Classification
TensorFlow 2.20+ | Keras API (Estimator-Free)
Author: Khalid Umar
============================================================

This tutorial demonstrates:
- Classification vs regression
- Loading CSV data
- Building input pipelines
- Training a neural network classifier
- Evaluating model performance
- Making predictions

Dataset: Iris flower dataset
Classes: Setosa, Versicolor, Virginica
"""

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import tensorflow as tf
import pandas as pd
import numpy as np

print("TensorFlow version:", tf.__version__)
print("-" * 60)

# ============================================================
# 2. LOAD DATASET
# ============================================================

CSV_COLUMN_NAMES = [
    "SepalLength",
    "SepalWidth",
    "PetalLength",
    "PetalWidth",
    "Species"
]

SPECIES = ["Setosa", "Versicolor", "Virginica"]

train_path = tf.keras.utils.get_file(
    "iris_training.csv",
    "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv"
)

test_path = tf.keras.utils.get_file(
    "iris_test.csv",
    "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv"
)

train_df = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
test_df = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)

print("Training data shape:", train_df.shape)
print("Testing data shape:", test_df.shape)
print("-" * 60)

# ============================================================
# 3. SPLIT FEATURES & LABELS
# ============================================================

train_labels = train_df.pop("Species")
test_labels = test_df.pop("Species")

print("Features:", list(train_df.columns))
print("-" * 60)

# ============================================================
# 4. BUILD INPUT PIPELINE
# ============================================================

def df_to_dataset(df, labels, shuffle=True, batch_size=32):
    df = df.copy()

    # Ensure correct dtype
    for col in df.columns:
        df[col] = df[col].astype("float32")

    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))

    if shuffle:
        ds = ds.shuffle(buffer_size=len(df))

    return ds.batch(batch_size)

train_ds = df_to_dataset(train_df, train_labels, shuffle=True)
test_ds = df_to_dataset(test_df, test_labels, shuffle=False)

# ============================================================
# 5. BUILD PREPROCESSING LAYERS
# ============================================================

inputs = {}
encoded_features = []

for feature in train_df.columns:
    inp = tf.keras.Input(shape=(1,), name=feature)
    norm = tf.keras.layers.Normalization()
    norm.adapt(train_df[feature].to_numpy().reshape(-1, 1))

    encoded = norm(inp)

    inputs[feature] = inp
    encoded_features.append(encoded)

# ============================================================
# 6. BUILD CLASSIFICATION MODEL
# ============================================================

x = tf.keras.layers.Concatenate()(encoded_features)

x = tf.keras.layers.Dense(30, activation="relu")(x)
x = tf.keras.layers.Dense(10, activation="relu")(x)

output = tf.keras.layers.Dense(3, activation="softmax")(x)

model = tf.keras.Model(inputs=inputs, outputs=output)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()
print("-" * 60)

# ============================================================
# 7. TRAIN MODEL
# ============================================================

history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=20
)

# ============================================================
# 8. EVALUATE MODEL
# ============================================================

loss, accuracy = model.evaluate(test_ds)
print(f"\nTest Accuracy: {accuracy:.4f}")
print("-" * 60)

# ============================================================
# 9. MAKE PREDICTIONS
# ============================================================

sample_data = {
    "SepalLength": [5.1, 6.0, 6.9],
    "SepalWidth": [3.5, 2.9, 3.1],
    "PetalLength": [1.4, 4.5, 5.4],
    "PetalWidth": [0.2, 1.5, 2.1],
}

sample_df = pd.DataFrame(sample_data)

for col in sample_df.columns:
    sample_df[col] = sample_df[col].astype("float32")

sample_ds = tf.data.Dataset.from_tensor_slices(dict(sample_df)).batch(1)

predictions = model.predict(sample_ds)

for i, probs in enumerate(predictions):
    class_id = np.argmax(probs)
    confidence = probs[class_id] * 100

    print(
        f"Sample {i + 1}: Prediction = {SPECIES[class_id]} "
        f"({confidence:.2f}%)"
    )

print("\nEnd of Iris Classification Tutorial")
