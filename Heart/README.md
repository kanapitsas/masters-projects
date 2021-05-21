# Data Science Projet

This is a project I completed during my Master's degree, for the Data Science course. I studied the [Heart Failure database](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-020-1023-5#Sec2)

The paper is in the `rapport.pdf` file (in french).

# How to use
There are three main files:
- `heart.py` : where the models and tests are.
- `heart_data.py` provides a function to load the data.
- `heart_graphics.py` gathers all the functions used to generate the plots inside `plots/`.

Here is a sample script on how to use the code :

```python
from sklearn.model_selection import train_test_split
from heart_data import *
import heart

X, y = import_heart_data(x_and_y = True)
X_train, X_test, y_train, y_test = train_test_split(X, y)

clf = heart.get_benchmark_model(X_train, y_train) # Get the logistic regression model
heart.evaluate_model(clf, X_test, y_test)         # Print the accuracy and class_accuracy

```
