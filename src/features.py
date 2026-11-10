import numpy as np
import mne
from mne.decoding import CSP
from sklearn.base import BaseEstimator, TransformerMixin


class FilterBankCSP(BaseEstimator, TransformerMixin):
    def __init__(self, n_components=3):
        self.n_components = n_components

    def fit(self, X, y):
        self.csps_ = []

        for band_idx in range(X.shape[1]):
            csp = CSP(n_components=self.n_components, reg=None, log=True,
                      norm_trace=False, rank=None)

            with mne.use_log_level("WARNING"):
                csp.fit(X[:, band_idx, :, :], y)

            self.csps_.append(csp)

        return self

    def transform(self, X):
        features = [csp.transform(X[:, band_idx, :, :])
                    for band_idx, csp in enumerate(self.csps_)]

        return np.concatenate(features, axis=1)