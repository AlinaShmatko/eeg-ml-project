from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.features import FilterBankCSP


def build_model(feature_method, classifier, n_components=3):
    if feature_method == "CSP":
        extractor = CSP(n_components=n_components, reg=None, log=True,
                        norm_trace=False, rank=None)
    elif feature_method == "FBCSP":
        extractor = FilterBankCSP(n_components=n_components)
    else:
        raise ValueError(f"Unknown feature method: {feature_method}")

    if classifier == "LDA":
        return make_pipeline(extractor, LinearDiscriminantAnalysis())
    elif classifier == "SVM":
        return make_pipeline(extractor, StandardScaler(),
                             SVC(kernel="rbf", C=1.0, gamma="scale"))
    else:
        raise ValueError(f"Unknown classifier: {classifier}")