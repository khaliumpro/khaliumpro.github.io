import tensorflow as tf
from tensorflow.keras import layers, models

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalize data(0-255-> 0-1)
x_train = x_train / 225.0
x_test = x_test / 225.0

# Add channel dimension (CNN requirement)
x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]

# Build CNN model 
model = models.Sequential([
    # Conv2D determine or capture the geomtric shape of an object
    # It likes a sensor which responsibe for identifying object
    # What is 32 in Conv2D?

    # Clean identified or detectable image such as squre pattern etc.

    # What is 3, 3 or 3 *3 in Conv2D?
    # 3 X 3 figured out the shape of the matric i.e 3 rows, 3 column
    # WHat is input_shape = (28, 28, 1)
    # 
    layers.Conv2D(32, (3,3), activation = 'relu', input_shape = (28, 28, 1)), 
    
    # WHat is max pooling?
    # Max Pooling is a size reduction mechanism
    # It also helps to reduce simulation complexity
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation = 'relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(128, activation = 'relu'),
    layers.Dense(10, activation = 'softmax')])

# Compile model 

model.compile (optimizer = 'adam',
               loss = 'sparse_categorical_crossentropy',
                metrics = ['accuracy'] )

# Train model 
model.fit(x_train, y_train, epochs = 5)

# Evaluation 
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print("Test accuracy:", test_accuracy)

