# Step one of Tensorflow
import tensorflow as tf
print("TensorFlow version: KHALID", tf.__version__)
print(90 * 4)

print(2+6)

# Step two of Tensorflow
print("creating tensors...")

hello_tensor = tf.Variable("This is a hello", dtype = tf.string)
print(hello_tensor)

morning_tensor = tf.Variable(200, dtype = tf.int16)
print(morning_tensor)