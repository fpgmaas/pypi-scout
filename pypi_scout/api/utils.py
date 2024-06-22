import logging
import sys

import polars as pl

from pypi_scout.config import Config, StorageBackend
from pypi_scout.utils.blob_io import BlobIO


def load_dataset(config: Config) -> pl.DataFrame:
    dataset_path = config.DATA_DIR / config.DATASET_FOR_API_CSV_NAME

    if dataset_path.exists():
        logging.info(f"Found local dataset. Reading dataset from `{dataset_path}`...")
        df = pl.read_csv(dataset_path)

    elif config.STORAGE_BACKEND == StorageBackend.BLOB:
        logging.info(
            f"Downloading `{config.DATASET_FOR_API_CSV_NAME}` from container `{config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}`..."
        )
        blob_io = BlobIO(
            config.STORAGE_BACKEND_BLOB_ACCOUNT_NAME,
            config.STORAGE_BACKEND_BLOB_CONTAINER_NAME,
            config.STORAGE_BACKEND_BLOB_KEY,
        )
        df = blob_io.download_csv(config.DATASET_FOR_API_CSV_NAME)
        logging.info("Finished downloading.")

    else:
        logging.error(
            f"Dataset {dataset_path} not found, and config.StorageBackend is not `BLOB` so can't download the dataset from Azure. Terminating."
        )
        sys.exit(1)

    logging.info(f"Finished loading the processed dataset. Number of rows: {len(df):,}")
    logging.info(f"The highest weekly downloads in the dataset: {df['weekly_downloads'].max():,}")
    logging.info(f"The lowest weekly downloads in the dataset: {df['weekly_downloads'].min():,}")
    return df
