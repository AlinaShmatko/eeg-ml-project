# Publishing the existing project on GitHub

These instructions apply to the **original `eeg-ml-project` folder**. There is no need to replace the original notebooks or start a second project.

1. Save changes in PyCharm/Jupyter. Keep `README.md`, `requirements.txt`, `.gitignore`, `notebooks/`, `src/`, `scripts/`, `docs/`, and any selected small files under `reports/` and `data/processed/`.
2. Confirm `.gitignore` excludes `*.edf`, `data/raw/`, `data/MNE-eegbci-data/`, `.ipynb_checkpoints/`, `__pycache__/`, and virtual environments.
3. Open GitHub Desktop → **File → Add Local Repository** and select `eeg-ml-project`. If it is not yet a Git repository, use **Create a Repository**.
4. Before committing, inspect **Changes** carefully. Raw EDF files and the MNE cache must not be listed.
5. Commit with a simple message such as `Add EEG motor imagery classification project`.
6. Choose **Publish repository** (or **Push origin** if a remote already exists). Use **Public** if you want reviewers to open the repository without an invitation.
7. Open the GitHub repository in a browser. Check that README renders, `notebooks/10_joint_model_selection.ipynb` and `11_final_evaluation.ipynb` open, and report figures display.

If raw data have already been tracked by Git, `.gitignore` alone will not untrack them; remove them from Git's index **without deleting your local data** before publishing. Do not publish a previous commit containing raw data by accident.

An optional code license is a separate decision. The PhysioNet dataset has its own attribution license; publishing code does not change that license.
