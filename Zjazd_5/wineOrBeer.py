"""
Beer Wine classifier, Jan Szenborn,  2023

This script will train a neural network to detect which is wine or beer looking only on price and alcohol .
Then, it will try to detect wine or beer using that model and will print statistic metrics.

How to use:
- activate venv in root repo directory using `source venv/bin/activate`
- install requirements by `pip install -r requirements.txt`
- go into this folder and run script via `python3 wineOrBeer.py`

"""
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import ConfusionMatrixDisplay

# Configuration
random_state = 42

# Prepare data
data = pd.read_csv('./data/beer_wine.csv', sep=',')

# Mapping categories to numerical values
data['class'] = data['class'].map({'beer': 0, 'wine': 1})

X = data.drop('class', axis=1)
y = data['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), verbose=0)

# Evaluate the model
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy: {test_acc}')

# Predictions on the test data
y_pred = (model.predict(X_test) > 0.5).astype("int32")  # Convert probabilities to binary predictions

# Generate the confusion matrix
conf_matrix = tf.math.confusion_matrix(y_test, y_pred)

# Normalize the confusion matrix
conf_matrix_normalized = conf_matrix / tf.reduce_sum(conf_matrix, axis=1, keepdims=True)

# Plot the confusion matrix
class_names = ['beer', 'wine']

# Plot non-normalized confusion matrix
disp = ConfusionMatrixDisplay(conf_matrix.numpy(), display_labels=class_names)
disp.plot(cmap=plt.cm.Blues, values_format=".0f")
disp.ax_.set_title("Confusion matrix, without normalization")

# Plot normalized confusion matrix
disp_normalized = ConfusionMatrixDisplay(conf_matrix_normalized.numpy(), display_labels=class_names)
disp_normalized.plot(cmap=plt.cm.Blues, values_format=".2f")
disp_normalized.ax_.set_title("Normalized confusion matrix")

plt.show()
