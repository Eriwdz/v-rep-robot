from joblib import dump
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
# Load data
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from data_reader import DataReader

X, y = DataReader.read("data/preprocessed")
# split into a training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Compute a PCA
n_components = 100
pca = PCA(n_components=n_components, whiten=True)
pca.fit(X_train, y_train)

params = {
    'clf__C': [1, 10, 100, 1000],
    'clf__gamma': [0.001, 0.0001],
    'clf__kernel': ['rbf', "poly"],
}

pipeline = Pipeline([
    ("pca", pca),
    ("clf", SVC())
])

grid = GridSearchCV(pipeline, params, n_jobs=-1)
grid.fit(X_train, y_train)
clf = grid.best_estimator_
target_names = ["female", "male"]
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=target_names))
dump(clf, "models/classifier.model")
