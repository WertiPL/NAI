import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Prepare data
data = pd.read_csv('./data/winequality-white.csv', sep=';')

X = data.drop('quality', axis=1)
y = (data['quality'] > 6).astype(int)  # Binary classification (1 if quality > 6, else 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Train SVM classifier
classifier = SVC(random_state=123)
classifier.fit(X_train, y_train)

# Predict
y_pred = classifier.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)

# Metrics
print(f"SVM classifier accuracy: {accuracy:.2f}\n")
print(classification_report(y_test, y_pred, zero_division=1))
