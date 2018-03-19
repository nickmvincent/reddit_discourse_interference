"""
try to classify reddit posts.
"""
import os
import pandas as pd
import glob
from sklearn_pandas import DataFrameMapper, cross_val_score
import sklearn
import numpy as np

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
    data = pd.read_csv('labeled_data/labeled_posts_10k_neg.csv', encoding='latin-1')

    data = data.fillna({
        'subreddit': ''
    })
    mapper = DataFrameMapper([
        ('subreddit', sklearn.preprocessing.LabelBinarizer()),
        # ('title', CountVectorizer(stop_words=True, lowercase=True, max_features=50)),
        ('title', TfidfVectorizer(stop_words='english', lowercase=True)),
    ])

    X = mapper.fit_transform(data.copy())
    print(X)

    clf = SGDClassifier(max_iter=10, tol=None, verbose=0)
    # clf = svm.LinearSVC(verbose=0)
    # clf = LogisticRegression(verbose=0)
    # clf.fit(X, data.from_influence_operation)
    # print_topk(20, mapper.transformed_names_, clf)

    # clf = NearestCentroid()
    for cv in [
        StratifiedKFold(5, True, 0),
        KFold(5, True, 0)
    ]:
        scores = cross_validate(clf, X, y=data.from_influence_operation, cv=cv, scoring=['precision', 'recall', 'f1', 'average_precision', 'roc_auc'])
        for key, val in scores.items():
            if 'test_' in key:
                print('{}:{}'.format(key, val))

    # pipe = sklearn.pipeline.Pipeline([
    #     ('featurize', mapper),
    #     ('clf', SGDClassifier(max_iter=10, tol=None, verbose=0)),
    # ])

    # scores = cross_val_score(pipe, X=data.copy(), y=data.from_influence_operation, scoring=None, cv=10)
    # print(scores)


if __name__ == '__main__':
    main()