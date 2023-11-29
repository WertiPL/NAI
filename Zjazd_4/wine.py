"""
Wine quality classifier, Wiktor Rostkowski Jan Szenborn, 2023

This script will train a decision tree by using 20% of data from CSV file.
Then, it will try to classify wine quality using that model and will print statistic metrics.

How to use:
- activate venv in root repo directory using `source venv/bin/activate`
- install requirements by `pip install -r requirements.txt`
- go into this folder and run script via `python3 wine.py`
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score, classification_report
import graphviz

# Prepare data
data = pd.read_csv('./data/winequality-white.csv', sep=';')

X = data.drop('quality', axis=1)
y = data['quality']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Train
classifier = DecisionTreeClassifier(random_state=123)
classifier.fit(X_train, y_train)

# Predict
y_pred = classifier.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)

print(f"Wine classifier accuracy: {accuracy:.2f}\n")
print(classification_report(y_test, y_pred))

# Create decision tree visualisation
tree_graph = export_graphviz(
    classifier, feature_names=X.columns, class_names=[str(i) for i in sorted(y.unique())], filled=True, rounded=True
)

graph = graphviz.Source(tree_graph, format='svg')
graph.render('wine_tree', format='svg', cleanup=True)
