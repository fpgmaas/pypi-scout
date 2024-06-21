import logging
from pathlib import Path

import polars as pl
from dotenv import load_dotenv

from pypi_scout.config import Config, StorageBackend
from pypi_scout.utils.blob_io import BlobIO
from pypi_scout.utils.logging import setup_logging


def read_processed_dataset(path_to_processed_dataset: Path):
    logging.info("📂 Reading the processed dataset...")
    df = pl.read_csv(path_to_processed_dataset)
    logging.info("📊 Number of rows in the processed dataset: %s", len(df))
    return df


def read_csv_from_local_and_upload(config: Config):
    blob_io = BlobIO(
        config.STORAGE_BACKEND_BLOB_ACCOUNT_NAME,
        config.STORAGE_BACKEND_BLOB_CONTAINER_NAME,
        config.STORAGE_BACKEND_BLOB_KEY,
    )

    if blob_io.exists(config.PROCESSED_DATASET_CSV_NAME):
        if not config.OVERWRITE:
            logging.info(
                f"🔹  Processed dataset {config.PROCESSED_DATASET_CSV_NAME} already exists in container '{config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}'! Skipping upload."
            )
            return
        else:
            logging.info(
                f"⤵️  Processed dataset {config.PROCESSED_DATASET_CSV_NAME} already exists in container '{config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}', but config.OVERWRITE is `true`. Overwriting..."
            )

    df = read_processed_dataset(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)
    logging.info(
        f"Uploading {config.PROCESSED_DATASET_CSV_NAME} to blob container {config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}..."
    )
    blob_io.upload_csv(df, config.PROCESSED_DATASET_CSV_NAME)
    logging.info("✅ Done!")


def upload_processed_dataset():
    load_dotenv()
    config = Config()
    if config.STORAGE_BACKEND != StorageBackend.BLOB:
        logging.info(
            "Not using BLOB backend. Skipping upload. To enable, configure the `STORAGE_BACKEND_` variables in config"
        )
        return
    read_csv_from_local_and_upload(config)


if __name__ == "__main__":
    setup_logging()
    upload_processed_dataset()
