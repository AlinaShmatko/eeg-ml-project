# EEG Motor Imagery Classification

This project explores how machine learning can be used to classify motor imagery from EEG signals.

I wanted to understand the full process of working with neurophysiological data: from signal exploration and preprocessing to feature extraction, model training, and evaluation on previously unseen subjects.

The focus is not on achieving the highest possible accuracy, but on understanding how different ML approaches perform on EEG data and what makes cross-subject generalization difficult.

## 1. Dataset

The project uses the EEG Motor Movement/Imagery Dataset from PhysioNet.

Dataset: https://physionet.org/content/eegmmidb/1.0.0/

The original recordings contain 64 EEG channels sampled at 160 Hz.

I use motor imagery runs R04, R08, and R12 to classify two events:

- T1: imagined left-fist movement
- T2: imagined right-fist movement

The data are divided by subject:

| Dataset | Subjects | EEG epochs |
|---|---|---:|
| Development | S001–S020 | 900 |
| Independent test | S021–S025 | 225 |

No subjects are shared between the development and test sets.

## 2. Methods

### EEG analysis

The initial notebooks explore raw EEG signals, event annotations, power spectral density (PSD), and frequency-band power.

The analysis focuses on motor-related EEG activity, particularly the mu/alpha (8–13 Hz) and beta (13–30 Hz) frequency bands.

### Machine learning

I started with handcrafted time-domain and frequency-domain features and evaluated several classical classifiers:

- Logistic Regression
- Linear Discriminant Analysis (LDA)
- Support Vector Machine (SVM)

I then investigated spatial feature extraction using Common Spatial Patterns (CSP) and Filter Bank CSP (FBCSP).

The later experiments also include EEGNet, DeepConvNet, and ATCNet.

### Cross-subject evaluation

The main challenge is classification on subjects who were not included in model training.

To investigate this, I used subject-aware cross-validation, including Leave-One-Subject-Out (LOSO), and examined performance separately for individual participants.

The final model was selected using the development cohort. An independent set of five previously unseen subjects was reserved for final evaluation.

## 3. Results

The selected model is CSP + LDA with:

- 6 EEG channels: C3, Cz, C4, CP3, CPz, CP4
- 8–30 Hz band-pass filtering
- 0–2 s EEG epochs
- 3 CSP components

### Development experiments

| Model | Mean LOSO Balanced Accuracy |
|---|---:|
| CSP + LDA | 0.624 |
| EEGNet | 0.607 |
| DeepConvNet | 0.575 |
| ATCNet | 0.516 |

These results are exploratory because the development subjects were also used during model and configuration selection.

The models were not evaluated under fully identical training procedures, so this table should not be interpreted as a definitive ranking of architectures.

### Independent evaluation

The selected CSP + LDA model was trained on S001–S020 and evaluated on S021–S025.

| Metric | Result |
|---|---:|
| Accuracy | 0.618 |
| Balanced Accuracy | 0.618 |
| Macro-F1 | 0.616 |

The independent test result was close to the development LOSO Balanced Accuracy of 0.624.

However, performance differed across individual subjects. Some participants showed a strong prediction bias toward T1 or T2.

This suggests that generalization across individuals remains an important challenge.

## 4. Project Structure

- `notebooks/` — EEG exploration, feature engineering, model development, and evaluation
- `src/` — reusable preprocessing, feature extraction, training, and evaluation functions
- `scripts/` — dataset downloading
- `data/processed/` — feature tables from the initial experiments

The notebooks follow the progression of the project:

| Notebooks | Focus |
|---|---|
| 01–02 | Data exploration and signal preprocessing |
| 03–06 | Classical ML, feature analysis, and optimization |
| 07–09 | CSP, generalization, and advanced EEG experiments |
| 10 | Model comparison and selection |
| 11 | Independent evaluation on unseen subjects |

Notebook 08 documents an earlier held-out experiment within the development cohort. The final independent evaluation is presented in Notebook 11.

## 5. How to Run

The project was developed using Python 3.11.

Create an environment and install the dependencies:

```bash
conda create -n eeg_ml python=3.11
conda activate eeg_ml
pip install -r requirements.txt
python scripts/download_data.py --include-test
cd notebooks
jupyter lab
```
The deep-learning comparisons in Notebook 10 require considerably more computation than the initial experiments. 
Some early notebooks use the small feature tables committed under `data/processed/`.

## 6. Limitations and Future Work

This is an exploratory ML study using neurophysiological data, not an exhaustive benchmark, medical device, or real-time brain–computer interface.

Possible next steps include:

- **Cross-subject variability:** differences in EEG feature distributions and spatial covariance between participants.
- **ERD/ERS:** changes in mu/beta-band power during imagined left- and right-fist movements.
- **Model robustness:** artifact rejection, preprocessing sensitivity and variability across training seeds.
- **Alternative features:** Riemannian covariance methods, connectivity measures and more systematic FBCSP evaluation.
- **Deep learning:** matched training budgets, capacity control and validation for competing architectures.
- **Subject adaptation:** calibration and domain adaptation using a new, explicitly separated evaluation protocol.

Some of these questions were explored preliminarily, but not exhaustively. The purpose of this project was to follow an end-to-end ML workflow for EEG signals and identify problems that deserve deeper investigation. Any future tuning would require a **new independent test cohort**, since results for S021–S025 are already known.

## 7. References

- Schalk, G. (2009). *EEG Motor Movement/Imagery Dataset (version 1.0.0)*. PhysioNet. https://doi.org/10.13026/C28G6P
- Schalk, G., et al. (2004). *BCI2000: A General-Purpose Brain-Computer Interface (BCI) System*. IEEE Transactions on Biomedical Engineering, 51(6), 1034–1043.

The PhysioNet data are licensed under the [Open Data Commons Attribution License v1.0](https://opendatacommons.org/licenses/by/1-0/). Raw EDF files are not included in this repository.
