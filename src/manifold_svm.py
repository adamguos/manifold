import numpy as np
from sklearn import svm

import grassmann

"""
References:
    [1] Jayasumana et al: Kernel methods on Riemannian manifolds with Gaussian RBF kernels
"""

def gaussian_kernel(Y1, Y2, metric_sq, gamma):
    """
    Computes Gaussian (rbf) kernel matrix on data arrays Y1 and Y2, using supplied metric function.

    Parameters:
        Y1, Y2:     arrays of data points
        metric_sq:  square of metric function to use
        gamma:      hyperparameter controlling Gaussian variance
    """
    kern_matrix = np.zeros((len(Y1), len(Y2)))
    for i in range(len(Y1)):
        for j in range(len(Y2)):
            kern_matrix[i, j] = np.exp(-gamma * metric_sq(Y1[i], Y2[j]))
    return kern_matrix

def manifold_svm(X, y):
    kern = lambda Y1, Y2 : gaussian_kernel(Y1, Y2, grassmann.projection_metric_sq, 0.5)
    clf = svm.SVC(kernel=kern)
    clf.fit(X, y)
    return clf