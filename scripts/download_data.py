import argparse

from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError

project_dir = Path(__file__).resolve().parent.parent
raw_dir = project_dir / "data" / "raw"

base_url = "https://physionet.org/files/eegmmidb/1.0.0/"
runs = [4, 8, 12]


def download_data(include_test=False):
    raw_dir.mkdir(parents=True, exist_ok=True)

    subjects = range(1, 26) if include_test else range(1, 21)

    downloaded = 0
    skipped = 0
    failed = []

    for subject in subjects:
        subject_id = f"S{subject:03d}"

        for run in runs:
            filename = f"{subject_id}R{run:02d}.edf"
            file_path = raw_dir / filename
            url = f"{base_url}{subject_id}/{filename}"

            if file_path.exists() and file_path.stat().st_size > 0:
                skipped += 1
                continue

            try:
                print(f"Downloading {filename}")
                urlretrieve(url, file_path)

                if file_path.stat().st_size == 0:
                    raise ValueError("Empty file")

                downloaded += 1

            except (HTTPError, URLError, OSError, ValueError) as error:
                if file_path.exists():
                    file_path.unlink()

                failed.append(filename)
                print(f"Failed: {filename} | {error}")

    print("Downloaded:", downloaded)
    print("Skipped:", skipped)
    print("Failed:", len(failed))

    if failed:
        print("Missing files:", failed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-test", action="store_true")
    args = parser.parse_args()

    download_data(include_test=args.include_test)