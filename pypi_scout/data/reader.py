from dataclasses import dataclass
from pathlib import Path

import polars as pl


@dataclass
class DataReader:
    """
    A class for reading and processing data from a raw PyPI dataset.
    """

    raw_dataset: Path

    def read(self):
        """
        Reads the raw dataset, performs data processing operations, and returns the processed dataframe.
        The dataset should at least have the following columns: name, description, and number_of_downloads.

        Returns:
            DataFrame: The processed dataframe.
        """
        df = pl.read_csv(self.raw_dataset)
        df = df.with_columns(weekly_downloads=(pl.col("number_of_downloads") / 4).round().cast(pl.Int32))
        df = df.drop("number_of_downloads")
        df = df.unique(subset="name")
        df = df.filter(~pl.col("description").is_null())
        df = df.sort("weekly_downloads", descending=True)
        return df
