"""
Wine quality classifier, Wiktor Rostkowski Jan Szenborn, 2023

This script will train a neural network to detect wine quality.
Then, it will try to classify wine quality using that model and will print statistic metrics.

How to use:
- activate venv in root repo directory using `source venv/bin/activate`
- install requirements by `pip install -r requirements.txt`
- go into this folder and run script via `python3 wine.py`
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import itertools
import random
import os

# Less verbose
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

# Configuration
random_state = 132

# Prepare data
data = pd.read_csv('../Zjazd_4/data/winequality-white.csv', sep=';')

X = data.drop('quality', axis=1)
y = tf.keras.utils.to_categorical(data['quality'], num_classes=10)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
X_validate, X_test, y_validate, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=random_state)

# Define class names
class_names = [str(i) for i in range(1, 11)]

model = tf.keras.Sequential()

# Input layer
model.add(tf.keras.Input(shape=(11,), dtype=tf.float32, name='x'))

# Hidden layers
for i in range(1, 5):
    model.add(tf.keras.layers.Dense(35, activation='sigmoid'))
    model.add(tf.keras.layers.Dropout(0.25))

# Output layer
model.add(tf.keras.layers.Dense(10, activation='softmax', name='output'))

# Model compilation

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='binary_crossentropy',
              metrics=['categorical_crossentropy'])

# Model training
history = model.fit(X_train, y_train, validation_data=(X_validate, y_validate), verbose=0)

val_loss = history.history['val_loss'][0]
val_categorical_crossentropy = history.history['val_categorical_crossentropy'][0]
print(f"Validation data loss: {val_loss:.3f}, categorical crossentropy: {val_categorical_crossentropy:.3f}")

test_loss, test_categorical_crossentropy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test data loss: {test_loss:.3f}, categorical crossentropy: {test_categorical_crossentropy:.3f}")

# Predictions on the test data
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Convert one-hot encoded labels back to class labels
y_test_classes = np.argmax(y_test, axis=1)

# Generate the confusion matrix
conf_matrix = tf.math.confusion_matrix(y_test_classes, y_pred_classes)

# Normalize the confusion matrix
conf_matrix_normalized = conf_matrix / tf.reduce_sum(conf_matrix, axis=1, keepdims=True)



# Plot non-normalized confusion matrix
disp = ConfusionMatrixDisplay(conf_matrix.numpy(), display_labels=class_names)
disp.plot(cmap=plt.cm.Blues, values_format=".0f")
disp.ax_.set_title("Confusion matrix, without normalization")

# Plot normalized confusion matrix
disp_normalized = ConfusionMatrixDisplay(conf_matrix_normalized.numpy(), display_labels=class_names)
disp_normalized.plot(cmap=plt.cm.Blues, values_format=".2f")
disp_normalized.ax_.set_title("Normalized confusion matrix")

plt.show()