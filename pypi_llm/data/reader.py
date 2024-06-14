from dataclasses import dataclass
from pathlib import Path

import polars as pl


@dataclass
class DataReader:
    data_dir: Path

    def read(self):
        df = pl.read_csv(self.data_dir / "pypi_dataset.csv")
        df = df.with_columns(weekly_downloads=(pl.col("number_of_downloads") / 4).round().cast(pl.Int32))
        df = df.drop("number_of_downloads")
        df = df.unique(subset="name")
        df = df.filter(~pl.col("description").is_null())
        df = df.sort("weekly_downloads", descending=True)
        return df
