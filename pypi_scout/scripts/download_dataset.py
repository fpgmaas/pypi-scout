import logging

import gdown
from dotenv import load_dotenv

from pypi_scout.config import Config, StorageBackend
from pypi_scout.utils.blob_io import BlobIO
from pypi_scout.utils.logging import setup_logging


def download_dataset():
    """
    Downloads the dataset from a Google Drive link using the gdown library.
    """
    load_dotenv()
    config = Config()

    if config.STORAGE_BACKEND == StorageBackend.LOCAL:
        handle_for_local_backend(config)
    else:
        handle_for_blob_backend(config)


def handle_for_local_backend(config: Config):
    target_path = config.DATA_DIR / config.RAW_DATASET_CSV_NAME
    if target_path.exists():
        logging.info(f"✔️  Raw dataset {target_path} from Google Drive already exists! Skipping download.")
        return

    logging.info(f"⬇️ Downloading raw dataset from Google Drive to {target_path}...")
    url = f"https://drive.google.com/uc?id={config.GOOGLE_FILE_ID}"
    gdown.download(url, str(target_path), quiet=False)
    logging.info("✅ Done!")


def handle_for_blob_backend(config: Config):
    blob_io = BlobIO(
        config.STORAGE_BACKEND_BLOB_ACCOUNT_NAME,
        config.STORAGE_BACKEND_BLOB_CONTAINER_NAME,
        config.STORAGE_BACKEND_BLOB_KEY,
    )

    if blob_io.exists(config.RAW_DATASET_CSV_NAME):
        logging.info(
            f"✔️  Raw dataset {config.RAW_DATASET_CSV_NAME} already exists in container '{config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}'! Skipping download."
        )
        return

    temp_target_path = config.DATA_DIR / config.RAW_DATASET_CSV_NAME
    logging.info("⬇️ Downloading raw dataset from Google Drive to temporary file...")
    url = f"https://drive.google.com/uc?id={config.GOOGLE_FILE_ID}"
    gdown.download(url, str(temp_target_path), quiet=False)

    logging.info("Downloading done, now uploading to Blob...")
    blob_io.upload_local_csv(temp_target_path, config.RAW_DATASET_CSV_NAME)
    logging.info("✅ Done!")


if __name__ == "__main__":
    setup_logging()
    download_dataset()
