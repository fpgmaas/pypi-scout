import logging
from pathlib import Path

import polars as pl
from dotenv import load_dotenv

from pypi_scout.config import Config, StorageBackend
from pypi_scout.data.description_cleaner import CLEANING_FAILED, DescriptionCleaner
from pypi_scout.data.reader import DataReader
from pypi_scout.utils.blob_io import BlobIO
from pypi_scout.utils.logging import setup_logging


def read_raw_dataset(path_to_raw_dataset):
    logging.info("📂 Reading the raw dataset...")
    df = DataReader(path_to_raw_dataset).read()
    logging.info("📊 Number of rows in the raw dataset: %s", len(df))
    logging.info(f"The highest weekly downloads in the raw dataset: {df['weekly_downloads'].max():,}")
    logging.info(f"The lowest weekly downloads in the raw dataset: {df['weekly_downloads'].min():,}")
    return df


def filter_top_packages(df, frac_data_to_include):
    logging.info(
        f"Using only the packages with weekly_downloads in the top {frac_data_to_include * 100}% of the dataset because config.FRAC_DATA_TO_INCLUDE is set to {frac_data_to_include}!"
    )
    logging.info(
        "This means packages with low download counts are excluded from the results in the dashboard. To include more data, set config.FRAC_DATA_TO_INCLUDE to a higher value."
    )
    df = df.sort("weekly_downloads", descending=True)
    df = df.head(round(frac_data_to_include * len(df)))

    logging.info(f"📊 Number of rows after filtering: {len(df):,}")
    logging.info(f"The highest weekly downloads in the filtered dataset: {df['weekly_downloads'].max():,}")
    logging.info(f"The lowest weekly downloads in the filtered dataset: {df['weekly_downloads'].min():,}")
    return df


def clean_descriptions(df):
    logging.info("🧹 Cleaning the descriptions...")
    df = DescriptionCleaner().clean(df, "description", "description_cleaned")
    df = df.filter(~pl.col("description_cleaned").is_null())
    df = df.filter(pl.col("description_cleaned") != CLEANING_FAILED)
    return df


def store_processed_dataset_local(df: pl.DataFrame, processed_dataset_path: Path):
    logging.info("Storing the processed dataset...")
    df.write_csv(processed_dataset_path)
    logging.info("✅ Done!")


def store_processed_dataset_blob(df: pl.DataFrame, blob_io: BlobIO, blob_name: str):
    logging.info(f"Storing the processed dataset as {blob_name} in container '{blob_io.container_name}'...")
    blob_io.upload_csv(df, blob_name)
    logging.info("✅ Done!")


def handle_for_local_backend(config: Config):
    if (config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME).exists():
        logging.info(f"✔️ Processed dataset {config.PROCESSED_DATASET_CSV_NAME} already exists! Skipping.")
        return

    df = read_raw_dataset(config.DATA_DIR / config.RAW_DATASET_CSV_NAME)
    if config.FRAC_DATA_TO_INCLUDE < 1.0:
        df = filter_top_packages(df, config.FRAC_DATA_TO_INCLUDE)
    df = clean_descriptions(df)

    store_processed_dataset_local(df, config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)


def handle_for_blob_backend(config: Config):
    blob_io = BlobIO(
        config.STORAGE_BACKEND_BLOB_ACCOUNT_NAME,
        config.STORAGE_BACKEND_BLOB_CONTAINER_NAME,
        config.STORAGE_BACKEND_BLOB_KEY,
    )

    if blob_io.exists(config.PROCESSED_DATASET_CSV_NAME):
        logging.info(
            f"✔️  Raw dataset {config.PROCESSED_DATASET_CSV_NAME} already exists in container '{config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}'! Skipping download."
        )
        return

    df = read_raw_dataset(config.DATA_DIR / config.RAW_DATASET_CSV_NAME)
    if config.FRAC_DATA_TO_INCLUDE < 1.0:
        df = filter_top_packages(df, config.FRAC_DATA_TO_INCLUDE)
    df = clean_descriptions(df)

    store_processed_dataset_blob(df, blob_io, config.PROCESSED_DATASET_CSV_NAME)


def process_dataset():
    load_dotenv()
    config = Config()
    if config.STORAGE_BACKEND == StorageBackend.LOCAL:
        handle_for_local_backend(config)
    else:
        handle_for_blob_backend(config)


if __name__ == "__main__":
    setup_logging()
    process_dataset()
