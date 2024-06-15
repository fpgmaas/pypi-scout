import logging

import polars as pl
from dotenv import load_dotenv

from pypi_scout.config import Config
from pypi_scout.data.description_cleaner import CLEANING_FAILED, DescriptionCleaner
from pypi_scout.data.reader import DataReader
from pypi_scout.utils.logging import setup_logging


def process_dataset():
    """
    This script processes a dataset by cleaning the description column and saving the processed dataset as a CSV file.
    """

    load_dotenv()
    config = Config()

    processed_dataset_path = config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME

    if processed_dataset_path.exists():
        logging.info("Processed dataset already exists. Skipping the cleaning process.")
        return

    logging.info("Reading the raw dataset...")
    df = DataReader(config.DATA_DIR / config.RAW_DATASET_CSV_NAME).read()

    logging.info("Cleaning the descriptions...")
    df = DescriptionCleaner().clean(df, "description", "description_cleaned")
    df = df.filter(~pl.col("description_cleaned").is_null())
    df = df.filter(pl.col("description_cleaned") != CLEANING_FAILED)

    logging.info("Storing the processed dataset...")
    df.write_csv(processed_dataset_path)
    logging.info("Done!")


if __name__ == "__main__":
    setup_logging()
    process_dataset()