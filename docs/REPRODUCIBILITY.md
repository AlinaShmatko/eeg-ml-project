# Reproducing the experiments

The notebooks document an exploratory progression rather than a single pipeline that needs to be retrained every time. The final independent evaluation is in Notebook 11.

## Environment

Use Python 3.11. From the project root:

```bash
conda create -n eeg_ml python=3.11
conda activate eeg_ml
pip install -r requirements.txt
python scripts/download_data.py --include-test
```

Alternatively, create the environment with `conda env create -f environment.yml` from the project root. Do not run both environment-creation commands for the same existing environment.

Open Jupyter with the `eeg_ml` kernel. For notebooks with relative paths such as `../data/raw`, start Jupyter from the `notebooks/` directory:

```bash
cd notebooks
jupyter lab
```

## Notebook guide

| Notebook | Purpose |
|---|---|
| 01–02 | Raw signals, annotations, spectral analysis, epochs and handcrafted features |
| 03–06 | Classical ML, subject-aware evaluation and feature analysis |
| 07–09 | CSP/FBCSP and further exploratory EEG experiments |
| 10 | Channel/window sensitivity, deep models and development-cohort model selection |
| 11 | Frozen CSP + LDA trained on S001–S020 and tested on S021–S025 |

Notebook 08 contains a **preliminary held-out experiment within the development cohort**. It is not a second independent final test.

## Reported results

The selected CSP + LDA model uses six channels, 8–30 Hz filtering, 0–2 s epochs and three CSP components. The 20-subject development LOSO balanced accuracy was **0.624** (exploratory). Independent test balanced accuracy on five previously unseen subjects was **0.618**, with Macro-F1 **0.616**.

The values in `reports/tables/` are summaries of saved notebook results. Figures in `reports/figures/` visualize these summaries; they are not additional experiments.

## Reproducibility limits

- Deep-learning sections in Notebook 10 require many separate training runs and may take substantial time on CPU.
- Neural-network training can vary across hardware and random seeds. Multi-seed repeatability was not established.
- Development results informed model selection and therefore are exploratory, not unbiased final estimates.
- S021–S025 have already been evaluated. Do not tune new models on them and still call them an independent test.
- `tests/` contains quick checks on **synthetic data**, not a reproduction of the published EEG scores.
