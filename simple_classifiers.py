"""
try to classify reddit posts.
"""
import os
import pandas as pd
import glob
from sklearn_pandas import DataFrameMapper, cross_val_score
import sklearn
import numpy as np
from collections import defaultdict
from pprint import pprint

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import cross_validate, StratifiedKFold, KFold
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid


def print_topk(k, feature_names, clf):
    """Prints features with the highest coefficient values, per class"""
    top10 = np.argsort(clf.coef_[0])[-k:]
    print(
        "{}".format(
            " ".join(feature_names[j] for j in top10)
        )
    )

def main():
    filename = 'labeled_posts_50k_neg.csv'
    path = 'labeled_data/' + filename
    data = pd.read_csv(path, encoding='latin-1')

    # all_labeled = pd.read_csv('labeled_data/labeled_posts.csv', encoding='latin-1')

    data = data.fillna({
        'subreddit': ''
    })
    mapper = DataFrameMapper([
        ('subreddit', sklearn.preprocessing.LabelBinarizer()),
        # ('title', CountVectorizer(stop_words=True, lowercase=True, max_features=50)),
        ('title', TfidfVectorizer(stop_words='english', lowercase=True)),
    ])

    X = mapper.fit_transform(data.copy())


    algo_to_score = defaultdict(dict)
    for clf, name in [
        (svm.LinearSVC(verbose=0), 'svm',),
        (SGDClassifier(max_iter=10, tol=None, verbose=0), 'sgd',),
        (LogisticRegression(verbose=0), 'logistic'),
        # (NearestCentroid(), 'nearest centroid'), # pretty bad recall. Kick this one out.
    ]:
        if name == 'logistic':
            clf.fit(X, data.from_influence_operation)
            print_topk(20, mapper.transformed_names_, clf)
        for folds in [
            StratifiedKFold(5, True, 0),
            # KFold(5, True, 0)
        ]:
            scores = cross_validate(
                clf, X, y=data.from_influence_operation, cv=folds,
                scoring=['f1', 'precision', 'recall'])
            ret = {}
            for key, val in scores.items():
                if 'test_' in key:
                    ret[key] = np.mean(val)
            algo_to_score[name]['cross_validation'] = ret
            # clf.fit(X, data.from_influence_operation)
            # y = clf.predict(all_labeled)
            # report = classification_report(expected, y)
    pprint(algo_to_score)

if __name__ == '__main__':
    main()