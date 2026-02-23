import scipy
import pandas as pd

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class CassificationModel:
    def __init__(self, temp, params):
        self.data   = temp
        self.params = params
        self.report = {}

    def DecisionTree(self):
        target  = self.params['target']
        col     = self.params['select_colmn']
        first   = self.params['first_choice']
        second  = self.params['secnd_choice']
        query = "{}.isin(('{}', '{}'))".format(col, first, second)
        data = self.data.query(query)

        cols_to_drop = []
        for col in data.columns:
            if data[col].dtype != 'float64':
                if col != target:
                    cols_to_drop.append(col)
        X = data.loc[:, ~data.columns.isin(cols_to_drop)]
        y = (data[col] == target)

        TREE = DecisionTreeClassifier(max_depth=1).fit(X, y) #finds the bias
        predictions = TREE.predict(X).tolist()

        ass = accuracy_score(y, TREE.predict(X))
        self.REPORT = {
                'as':ass,
                'predictions':predictions,
                'tree':TREE
        }

    def Logistic(self):
        random_state    = self.params['random_state']
        test_size       = self.params['test_size']
        y = self.data.pop(self.params['target'])
        cols_to_drop = []
        for col in self.data.columns:
            if data[col].dtype != 'float64':
                if col != target['target']:
                    cols_to_drop.append(col)
        X = self.data.loc[:, ~data.columns.isin(cols_to_drop)]

        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                            test_size=test_size, 
                                            random_state=random_state)

        model = LogisticRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        cr = classification_report(y_test, predictions) 
        cm = confusion_matrix(y_test, predictions)
        ass = accuracy_score(y_test, predictions)
        mc = model.coef_.tolist()
        mi = model.intercept_.tolist()

        self.REPORT = {
            'model_coef': mc,
            'model_intercept': mi,
            'confusion_matrix': cm,
            'classification_report': cr,
            'as':ass,
            'model':model
        }

