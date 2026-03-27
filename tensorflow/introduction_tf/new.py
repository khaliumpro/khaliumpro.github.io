import tensorflow as tf
import numpy as np

# Training data
x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3, 5, 7, 9, 11], dtype=float)

# Build model
model = tf.keras.Sequential([
    tf.keras.Input(shape=(1,)),
    tf.keras.layers.Dense(1)
])

# Compile model
model.compile(
    optimizer='adam',
    loss='mean_squared_error'
)

# Train model (SHOW epochs)
model.fit(x, y, epochs=500, verbose=2)

# Test prediction
prediction = model.predict(np.array([[6]], dtype=float))
print("Prediction for x = 6:", prediction)
