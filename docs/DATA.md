# Dataset

The project uses the [EEG Motor Movement/Imagery Dataset (v1.0.0)](https://physionet.org/content/eegmmidb/1.0.0/) from PhysioNet.

- Recordings: R04, R08, and R12 (imagined left- and right-fist movements)
- T1: imagined left fist; T2: imagined right fist **for these runs**
- Original recordings: 64 channels at 160 Hz
- Development subjects: S001–S020 (60 recordings, 900 epochs)
- Independent test subjects: S021–S025 (15 recordings, 225 epochs)

The selected final pipeline uses C3, Cz, C4, CP3, CPz, and CP4, an 8–30 Hz band-pass filter, and 0–2 s epochs. Average reference is applied before channel selection.

## Download

From the project root, after installing dependencies:

```bash
python scripts/download_data.py --include-test
```

This requires the `--include-test` option in `scripts/download_data.py`. It downloads all 75 EDF recordings into `data/raw/`, skipping existing nonempty files. The `data/MNE-eegbci-data/` directory is an optional local MNE cache and is not needed in the repository.

Raw EDF recordings are **not** committed to GitHub. Small derived feature tables in `data/processed/` may be included to support early notebooks.

## Attribution

Schalk, G. (2009). *EEG Motor Movement/Imagery Dataset (version 1.0.0).* PhysioNet. https://doi.org/10.13026/C28G6P

PhysioNet lists the dataset under the [Open Data Commons Attribution License v1.0](https://opendatacommons.org/licenses/by/1-0/). This data license is separate from any license for the project's Python code.
