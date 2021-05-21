from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import confusion_matrix

# -------------------
# -- Global variables
# -------------------

# These are the most important features, as determined in the paper
important_features = ['serum_creatinine', 'ejection_fraction', 'age', 'serum_sodium']
k_cv = 10 # Number of folds for cross-validation

# ----------------------
# -- Custom transformers
# ----------------------

class Translate(TransformerMixin, BaseEstimator):
    '''This transformer changes the names of the features and labels based on a "translation" dictionnary.
    Parameters
    ----------
    names_dict : a dictionnary containing the translations. Keys are the current names, and values are the translations.'''
    def __init__(self, names_dict):
        self.dict = names_dict

    def fit(self, X, y=None):
        '''X is assumed to be a pandas array, and y None, or a pandas series'''
        # The only thing to do is to check that every translation is provided
        to_translate = list(X.columns)
        if y is not None:
            to_translate.append(y.name)
        for name in to_translate:
            if name not in self.dict:
                raise Exception('Missing translation for ', name)
        return self

    def transform(self, X, y=None):
        from copy import deepcopy
        new_X = deepcopy(X)
        new_X.columns = list(map(lambda x: self.dict[x], X.columns))
        if y is not None:
            new_y = deepcopy(y)
            new_y.name = self.dict[y.name]
            return (new_X, new_y)
        return new_X

class OnlyKeep(TransformerMixin, BaseEstimator):
    '''Very simple transformer that only keeps the columns in the list `classes` for X.
    Leaves the labels y untouched.
    Parameters
    ----------
    classes : the list of classes to keep (by names)'''
    def __init__(self, classes):
        self.classes = classes
    def fit(self, *args):
        return self
    def transform(self, X, y=None):
        return X[self.classes]

class InverseFeature(TransformerMixin, BaseEstimator):
    '''Multiply one or more columns by -1.
    Parameters
    ----------
    classes : the list of classes to be transformed (by name)'''
    def __init__(self, classes):
        self.classes = classes
    def fit(self, *args):
        return self
    def transform(self, X, y=None):
        from copy import deepcopy
        new_X = deepcopy(X)
        new_X[self.classes] = -new_X[self.classes]
        return new_X

# ---------
# -- Models
# ---------

def get_benchmark_model(X_train, y_train):
    '''Performs a cross-validation on the following pipeline:
    Keep important features -> MinMax scaler -> Logistic regression
    Where the complexity paramter of the logistic regression varies from 10e-3 to 10e4

    Parameters
    ----------
    X_train, y_train : the training data.

    Returns
    -------
    A sklearn estimator.'''
    pl = Pipeline([('extraction', OnlyKeep(important_features)),
                   ('scaler', MinMaxScaler()),
                   ('logistic', LogisticRegression(class_weight='balanced'))])

    params = {"logistic__C": [10**x for x in range(-3, 5)]} # We only tune the complexity param
    clf = GridSearchCV(pl, params, cv=k_cv)
    clf.fit(X_train, y_train)

    return clf.best_estimator_

def get_poly_logistic_model(X_train, y_train):
    '''Performs a cross-validation on the following pipeline:
    Keep important features -> inverse features
    -> MinMax scaler -> polynomial features -> Logistic regression
    Where the complexity paramter of the logistic regression varies from 10e-3 to 10e4,
    and the polynomial degree varies from 2 to 4.

    Parameters
    ----------
    X_train, y_train : the training data.

    Returns
    -------
    A sklearn estimator.'''
    pl = Pipeline([('extraction', OnlyKeep(important_features)),
                   ('inverse', InverseFeature(['ejection_fraction'])),
                   ('scaler', MinMaxScaler()),
                   ('poly', PolynomialFeatures()),
                   ('logistic', LogisticRegression(max_iter=1000))
                  ])
    params = {"logistic__C": [10**x for x in range(-3, 5)],
              "poly__degree": [2,3,4]}
    clf = GridSearchCV(pl, params, cv=k_cv)
    clf.fit(X_train, y_train)

    return clf.best_estimator_

def compare_models(X_train, y_train):
    '''Performs a cross-validation on the following pipeline:
    Keep important features -> MinMax scaler -> model
    Where the model is in :
     - MLP
     - SVM
     - K-nearest-neighbours
     - AdaBoost
     - RandomForest

    The optimized parameters are inside the `params` list. This can easily be changed.

    Parameters
    ----------
    X_train, y_train : the training data.

    Returns
    -------
    A list of tuples containing the name of the model, and the corresponding
    sklearn estimator.'''
    from sklearn.neural_network import MLPClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

    models = [
        ('MLP', MLPClassifier(max_iter=10000)),
        ('SVM', SVC()),
        ('K-NN', KNeighborsClassifier()),
        ('AdaBoost', AdaBoostClassifier()),
        ('RandomForest', RandomForestClassifier())
    ]

    params = [
        {'MLP__hidden_layer_sizes': [10, 50, [20, 10], [20, 10, 10], [20, 20, 20]]}, # These are pretty arbitrary
        {'SVM__C': [10**x for x in range(-3, 4)],
         'SVM__kernel': ['poly', 'rbf']},
        {'K-NN__n_neighbors': [3, 5, 10, 15, 20, 30]},
        {'AdaBoost__n_estimators': [1, 2, 3, 4, 5, 10, 50, 100, 200, 400, 800]},
        {'RandomForest__n_estimators': [5, 10, 50, 100, 200, 400, 800],
         'RandomForest__max_depth': [1, 2, 3, 4, 5, 10, 20, None]}
    ]

    best_models = []
    for model, param in zip(models, params):
        pl = Pipeline([
            ('keeper', OnlyKeep(important_features)),
            ('scaler', MinMaxScaler()),
            model
        ])
        clf = GridSearchCV(pl, param, cv=k_cv)
        clf.fit(X_train, y_train)
        best_models.append((model[0], clf.best_estimator_)) # Save the best-performing models
        print(model[0], clf.best_score_, clf.best_params_)  # Print the best scores and params
    return best_models

# -----------------------
# -- Evaluation functions
# -----------------------

def evaluate_model(clf, X_test, y_test):
    '''Prints the score of the classifier, as well as the class-accuracy.

    Parameters
    ----------
    clf : a sklearn classifier
    X_test, y_test : the test data'''
    print('Score:', clf.score(X_test, y_test))
    print('Accuracy per class', *class_accuracy(clf.predict(X_test), y_test))

def class_accuracy(y_true, y_pred):
    '''Returns the accuracy, conditionned on y=0 and y=1

    Parameters
    ----------
    y_true, y_pred : the true labels and the predictions

    Returns
    -------
    A numpy array with the accuracies'''
    mat = confusion_matrix(y_true, y_pred)
    return mat.diagonal() / mat.sum(axis=1)
