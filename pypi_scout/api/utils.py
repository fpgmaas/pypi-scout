import logging
from pathlib import Path

import polars as pl


def load_dataset(path_to_dataset: Path):
    logging.info("Loading the processed dataset...")
    df = pl.read_csv(path_to_dataset)
    logging.info(f"Finished loading the processed dataset. Number of rows: {len(df):,}")
    logging.info(f"The highest weekly downloads in the dataset: {df['weekly_downloads'].max():,}")
    logging.info(f"The lowest weekly downloads in the dataset: {df['weekly_downloads'].min():,}")
    return df
