import tensorflow as tf
import numpy as np

# Training data

x = np.array([10, 20, 30, 40, 50], dtype = float)
y = np.array([30, 60, 90, 120, 150], dtype = float)

# Build model 

model = tf.keras.Sequential([tf.keras.layers.Dense(units = 1,
                                                    input_shape = [1])])

# Compile model 
model.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Train model
model.fit(x, y, epochs = 200, verbose = 1)

# Test model 
print("prediction for x = 20", model.predict([60]))

