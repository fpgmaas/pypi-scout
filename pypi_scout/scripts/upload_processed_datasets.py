import logging
from pathlib import Path

import polars as pl
from dotenv import load_dotenv

from pypi_scout.config import Config, StorageBackend
from pypi_scout.utils.blob_io import BlobIO
from pypi_scout.utils.logging import setup_logging


class CsvToBlobUploader:
    def __init__(self, config: Config):
        self.config = config
        self.blob_io = BlobIO(
            config.STORAGE_BACKEND_BLOB_ACCOUNT_NAME,
            config.STORAGE_BACKEND_BLOB_CONTAINER_NAME,
            config.STORAGE_BACKEND_BLOB_KEY,
        )
        self.overwrite = config.OVERWRITE

    def read_csv(self, path_to_csv: Path) -> pl.DataFrame:
        logging.info(f"📂 Reading the dataset from {path_to_csv}...")
        df = pl.read_csv(path_to_csv)
        logging.info(f"📊 Number of rows in the dataset {path_to_csv.name}: {len(df):,}")
        return df

    def upload_csv_to_blob(self, df: pl.DataFrame, csv_name: str):
        if self.blob_io.exists(csv_name):
            if not self.overwrite:
                logging.info(
                    f"🔹  Dataset {csv_name} already exists in container '{self.config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}'! Skipping upload."
                )
                return
            else:
                logging.info(
                    f"⤵️  Dataset {csv_name} already exists in container '{self.config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}', but overwrite is enabled. Overwriting..."
                )

        logging.info(f"Uploading {csv_name} to blob container {self.config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}...")
        self.blob_io.upload_csv(df, csv_name)
        logging.info("✅ Done!")

    def process_and_upload_datasets(self, dataset_names: list[str]):
        for dataset_name in dataset_names:
            csv_path = self.config.DATA_DIR / dataset_name
            df = self.read_csv(csv_path)
            self.upload_csv_to_blob(df, dataset_name)


def upload_processed_datasets():
    load_dotenv()
    config = Config()

    if config.STORAGE_BACKEND != StorageBackend.BLOB:
        logging.info(
            "Not using BLOB backend. Skipping upload. To enable, configure the `STORAGE_BACKEND_` variables in config"
        )
        return

    dataset_names = [config.PROCESSED_DATASET_CSV_NAME, config.DATASET_FOR_API_CSV_NAME]

    uploader = CsvToBlobUploader(config)
    uploader.process_and_upload_datasets(dataset_names)


if __name__ == "__main__":
    setup_logging()
    upload_processed_datasets()
