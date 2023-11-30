"""
Running device guesser, Wiktor Rostkowski Jan Szenborn, 2023

Wine Quality Classifier and SVM Visualization, 

This script analyzes the wine quality dataset, aiming to classify wines into two categories based on their features.
It uses Support Vector Machines (SVM) with a grid search.

How to Use:
1. Ensure you have the necessary dependencies installed by running `pip install -r requirements.txt`.
2. Execute the script using Python with `python SVM-wine.py`.
3. Explore the SVM classifier accuracy and detailed classification report for the wine quality dataset.
4. Visualize the decision function of SVM classifiers with different hyperparameters.

Note: The wine quality is transformed into two categories, 0 and 1, based on user-defined quality ranges.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Read data
data = pd.read_csv('./data/winequality-white.csv', sep=';')

# Transform wine quality into two categories (you can adjust the ranges)
data['quality_category'] = pd.cut(data['quality'], bins=[0, 6, 10], labels=[0, 1])

# Select relevant columns
X = data[["residual sugar", "alcohol"]].values
y = data['quality_category'].astype(int)

# Standardize the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Train SVM classifier using grid search
C_range = np.logspace(-2, 2, 5)
gamma_range = np.logspace(-5, 1, 5)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
grid.fit(X_train, y_train)

# Best parameters and model
best_params = grid.best_params_
best_model = grid.best_estimator_

# Predictions for test data
y_pred = best_model.predict(X_test)

# Model evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"SVM classifier accuracy: {accuracy:.2f}\n")
print(classification_report(y_test, y_pred, zero_division=1))

# Visualization setup
C_2d_range = [1e-2, 1, 1e2]
gamma_2d_range = [1e-1, 1, 1e1]
classifiers = []
for C in C_2d_range:
    for gamma in gamma_2d_range:
        clf = SVC(C=C, gamma=gamma)
        clf.fit(X, y)
        classifiers.append((C, gamma, clf))

# Visualization
plt.figure(figsize=(8, 6))
xx, yy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
for k, (C, gamma, clf) in enumerate(classifiers):
    # Evaluate decision function in a grid
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Visualize decision function for these parameters
    plt.subplot(len(C_2d_range), len(gamma_2d_range), k + 1)
    plt.title("gamma=10^%d, C=10^%d" % (np.log10(gamma), np.log10(C)), size="medium")

    # Visualize parameter's effect on decision function
    plt.pcolormesh(xx, yy, -Z, cmap=plt.cm.RdBu)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdBu_r, edgecolors="k")
    plt.xticks(())
    plt.yticks(())
    plt.axis("tight")

# Display the plot
plt.show()
