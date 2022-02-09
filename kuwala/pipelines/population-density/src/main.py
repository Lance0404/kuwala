import sys

sys.path.insert(0, "../../../common/")

import argparse

from Downloader import Downloader
from Processor import Processor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--continent", help="Continent of the file")
    parser.add_argument("--country", help="Country of the file")
    parser.add_argument(
        "--demographic_groups", help="Demographic groups to be downloaded"
    )
    args = parser.parse_args()

    files, output_dir, updated_date = Downloader.start(args)

    Processor.start(files, output_dir, updated_date)
