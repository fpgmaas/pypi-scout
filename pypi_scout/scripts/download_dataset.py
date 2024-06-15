import logging

import gdown
from dotenv import load_dotenv

from pypi_scout.config import Config
from pypi_scout.utils.logging import setup_logging


def download_dataset():
    """
    Downloads the dataset from a Google Drive link using the gdown library.
    """
    load_dotenv()
    config = Config()

    logging.info("Downloading raw dataset from Google Drive...")
    url = f"https://drive.google.com/uc?id={config.GOOGLE_FILE_ID}"
    output = str(config.DATA_DIR / config.RAW_DATASET_CSV_NAME)
    gdown.download(url, output, quiet=False)
    logging.info("Done!")


if __name__ == "__main__":
    setup_logging()
    download_dataset()
