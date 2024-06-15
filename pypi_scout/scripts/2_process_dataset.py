import logging

import polars as pl
from dotenv import load_dotenv

from pypi_scout.config import Config
from pypi_scout.data.description_cleaner import CLEANING_FAILED, DescriptionCleaner
from pypi_scout.data.reader import DataReader
from pypi_scout.utils.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    """
    This script processes a dataset by cleaning the description column and saving the processed dataset as a CSV file.
    """

    load_dotenv()
    config = Config()

    logging.info("Reading the raw dataset...")
    df = DataReader(config.DATA_DIR / config.RAW_DATASET_CSV_NAME).read()

    logging.info("Cleaning the descriptions...")
    df = DescriptionCleaner().clean(df, "description", "description_cleaned")
    df = df.filter(~pl.col("description_cleaned").is_null())
    df = df.filter(pl.col("description_cleaned") != CLEANING_FAILED)

    logging.info("Storing the processed dataset...")
    df.write_csv(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)
    logging.info("Done!")
