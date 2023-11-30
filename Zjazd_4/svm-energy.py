"""
Running device guesser, Wiktor Rostkowski Jan Szenborn, 2023
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Load and prepare data set
data = pd.read_csv('./data/energy.csv', sep=',')

# Selecting the desired features
X = data[['phase_1', 'phase_2', 'phase_3']].values
y = data['device']

# Scale the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Train SVM classifier
classifier = SVC(kernel='linear', C=1, decision_function_shape='ovr')
classifier.fit(X_train, y_train)

# Predictions for test data
y_pred = classifier.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
print(f"SVM classifier accuracy: {accuracy:.2f}\n")
print(classification_report(y_test, y_pred))
