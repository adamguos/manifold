"""
References:
    [1] Mhaskar: A direct approach for function approximation on data defined manifolds
"""

import numpy as np
import scipy
from sklearn.base import BaseEstimator, ClassifierMixin
import pdb

import hermite
import metrics

def distance_matrix(X, Y, metric):
    """
    Computes distance matrix between elements of X and Y, using metric. Returns 2D array distance,
    where distance[i, j] = metric(X[i], Y[j]).
    """
    distance = np.zeros((len(X), len(Y)))
    for i in range(len(X)):
        for j in range(len(Y)):
            m = metric(X[i], Y[j])
            if np.isnan(m):
                pdb.set_trace()
            distance[i, j] = m
    return distance

class HermiteClassifier(BaseEstimator, ClassifierMixin):
    """
    Classifier using Hermite approximator.

    [1] equation (3.8)
    """
    def __init__(self, n=8, q=6, alpha=1, metric=None):
        self.n = n
        self.q = q
        self.alpha = alpha

        if metric == None:
            self.metric = lambda X, Y : np.linalg.norm(X - Y)
        else:
            self.metric = metric

    def fit(self, X_train, y_train):
        self.coef = self.n ** (self.q * (1 - self.alpha)) / len(X_train)
        self.X_train = X_train
        self.y_train = y_train
        return self

    def predict(self, X_test):
        norms = distance_matrix(self.X_train, X_test, self.metric)

        labels = np.repeat([self.y_train], len(X_test), axis=0).transpose()
        Phis = np.zeros_like(labels).astype(float)

        for j in range(Phis.shape[0]):
            Phis[j, :] = hermite.Phi(self.n, self.q, norms[j, :])

        # return np.sign(self.coef * np.sum(labels * Phis, axis=0))
        return self.coef * np.sum(labels * Phis, axis=0)
