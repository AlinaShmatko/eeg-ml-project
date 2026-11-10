import numpy as np
import pytest
import mne

from src.models import build_model


def test_csp_lda_pipeline():
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 6, 321)) * 1e-6
    y = np.array([0, 1] * 15)

    X[y == 0, 0] *= 2
    X[y == 1, 3] *= 2

    model = build_model("CSP", "LDA", n_components=3)

    with mne.use_log_level("ERROR"):
        model.fit(X[:24], y[:24])
        features = model.named_steps["csp"].transform(X[24:])

    predictions = model.predict(X[24:])

    assert features.shape == (6, 3)
    assert predictions.shape == (6,)
    assert np.isfinite(features).all()
    assert set(np.unique(predictions)).issubset({0, 1})


def test_unknown_classifier():
    with pytest.raises(ValueError, match="Unknown classifier"):
        build_model("CSP", "Unknown")
