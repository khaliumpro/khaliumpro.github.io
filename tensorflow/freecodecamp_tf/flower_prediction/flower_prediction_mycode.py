import tensorflow as tf
import pandas as pd
import numpy as np

print("Flower Pridiction:", tf.__version__)
print("- * 60")

# Define column names for the CSV files
CSV_COLUMN_NAMES = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "Species"]

# Human-readable class labels
SPECIES = ["Setosa", "Versicolor", "Virginica"]

# Download datasets if not already cached

train_path = tf.keras.utils.get_file("iris_training.csv", 
    "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv"
)

test_path = tf.keras.utils.get_file(
    "iris_test.csv",
    "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv"
)


#Load CSV files into Pandas DataFrames
train_df = pd.read_csv(train_path, names = CSV_COLUMN_NAMES, header = 0)
test_df = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header = 0)

print("Traning data shape:", train_df.shape)
print("Testing data shape:", test_df.shape)

# Remove column are input features
train_labels = train_df.pop("Species")
test_labels = test_df.pop("Species")

# Remaining columns are input features
print("Feature column:", list(train_df.columns))

def df_to_dataset(df, labels, shuffle = True, batch_size = 32): 
    df = df.copy()

    # Convert all features to float32 for TensorFlow compatibility
    for col in df.columns: 
        df[col] = df[col].astype("float32")

    # Create TensorFlow dataset from features and labels
    dataset = tf.data.Dataset.from_tensor_slices((dict(df), labels))

    # Shuffle only during training 
    if shuffle: dataset = dataset.shuffle(buffer_size = len (df))

    # Return batched dataset
    return dataset.batch(batch_size)

# Create training and testing datasets
train_ds = df_to_dataset(train_df, train_labels, shuffle = True)
test_ds = df_to_dataset(test_df, test_labels, shuffle=False)





