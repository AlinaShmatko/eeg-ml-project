import numpy as np
import pandas as pd
import torch

from sklearn.model_selection import GroupKFold
from sklearn.metrics import balanced_accuracy_score, f1_score
from src.training import train_model


def evaluate_deep_config(X, y, groups, development_idx, architecture="EEGNet", max_folds=4):
    inner_cv = GroupKFold(n_splits=4)
    stop_cv = GroupKFold(n_splits=4)
    results = []

    for fold, (inner_train, inner_score) in enumerate(inner_cv.split(
            X[development_idx], y[development_idx], groups[development_idx]), start=1):
        train_pool_idx = development_idx[inner_train]
        score_idx = development_idx[inner_score]

        fit_local, stop_local = next(stop_cv.split(
            X[train_pool_idx], y[train_pool_idx], groups[train_pool_idx]))

        fit_idx = train_pool_idx[fit_local]
        stop_idx = train_pool_idx[stop_local]

        subject_sets = [set(groups[idx]) for idx in [fit_idx, stop_idx, score_idx]]
        assert all(subject_sets[i].isdisjoint(subject_sets[j])
                   for i in range(3) for j in range(i + 1, 3))

        model, history, best_epoch, best_loss = train_model(
            X[fit_idx], y[fit_idx], X[stop_idx], y[stop_idx],
            architecture=architecture)

        model.eval()
        with torch.no_grad():
            y_pred = model(torch.from_numpy(X[score_idx])).argmax(dim=1).cpu().numpy()

        for subject in np.unique(groups[score_idx]):
            mask = groups[score_idx] == subject

            results.append({"Fold": fold, "Subject": subject,
                            "BA": balanced_accuracy_score(y[score_idx][mask], y_pred[mask]),
                            "Macro-F1": f1_score(y[score_idx][mask], y_pred[mask], average="macro"),
                            "Best Epoch": best_epoch})

        if fold >= max_folds:
            break

    return pd.DataFrame(results)