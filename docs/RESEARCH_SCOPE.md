# Research scope and possible extensions

## Aim

I built this project to understand how machine learning can be applied to neurophysiological signals and how well an EEG motor imagery classifier generalizes to new people.

The aim was to work through the full problem: inspect the EEG recordings, preprocess signals, extract features, train models, compare subject-aware evaluations, and examine errors on unseen participants. It is a machine learning case study in computational neuroscience, not a clinical tool or a real-time BCI.

## What I investigated

- Raw EEG signals, event annotations, PSD and mu/beta-band power
- Time-domain and spectral features with classical classifiers
- CSP and FBCSP features, channel sets and temporal windows
- Logistic Regression, LDA, SVM, EEGNet, DeepConvNet and ATCNet
- Cross-subject differences using grouped validation and LOSO
- Independent CSP + LDA evaluation on S021–S025 (BA = 0.618)

The experiments suggested that participant-specific prediction bias is an important difficulty: some unseen subjects are classified more reliably than others, and different participants show opposite class biases.

## Where the research could go next

| Direction | Question I would investigate |
|---|---|
| Cross-subject shift | How much do covariance and frequency-band distributions differ between individuals? |
| ERD/ERS | Are mu/beta power changes and their laterality related to imagined left/right movement? |
| EEG artifacts | How sensitive are the results to artifact rejection, referencing and preprocessing choices? |
| Alternative spatial representations | Could Riemannian covariance methods improve subject-independent decoding? |
| Model stability | How much do results vary with random seeds, participants and dataset size? |
| Subject calibration | Does a small labeled calibration set help, compared with zero-calibration performance? |
| Deeper neural models | What happens when architectures are compared under matched tuning and compute budgets? |
| Interpretability | Which CSP spatial patterns reflect plausible motor-related activity, and what are their limits? |

These are **possible extensions**, not results claimed by this repository. Some were investigated preliminarily, but not comprehensively. The current work intentionally focuses on demonstrating the ML workflow rather than exhaustive hyperparameter search or benchmarking.

## Limitations

The study uses 20 development subjects and five independent test subjects. Several architecture comparisons use different training protocols. For some deep models, Braindecode adapts the architecture when the temporal input is short, so window differences can also change model capacity.

The independent test was inspected once. Further development should use a new held-out cohort to support another independent evaluation; the five existing test subjects should not be reused for model tuning.
