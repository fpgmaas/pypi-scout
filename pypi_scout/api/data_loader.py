import logging
from typing import Tuple

import polars as pl

from pypi_scout.config import Config, StorageBackend
from pypi_scout.utils.blob_io import BlobIO


class ApiDataLoader:
    def __init__(self, config: Config):
        self.config = config

    def load_dataset(self) -> Tuple[pl.DataFrame, pl.DataFrame]:
        if self.config.STORAGE_BACKEND == StorageBackend.LOCAL:
            df_packages, df_embeddings = self._load_local_dataset()
        elif self.config.STORAGE_BACKEND == StorageBackend.BLOB:
            df_packages, df_embeddings = self._load_blob_dataset()
        else:
            raise ValueError(f"Unexpected value found for STORAGE_BACKEND: {self.config.STORAGE_BACKEND}")  # noqa: TRY003

        return df_packages, df_embeddings

    def _load_local_dataset(self) -> Tuple[pl.DataFrame, pl.DataFrame]:
        packages_dataset_path = self.config.DATA_DIR / self.config.DATASET_FOR_API_CSV_NAME
        embeddings_dataset_path = self.config.DATA_DIR / self.config.EMBEDDINGS_PARQUET_NAME

        logging.info(f"Reading packages dataset from `{packages_dataset_path}`...")
        df_packages = pl.read_csv(packages_dataset_path)
        self._log_packages_dataset_info(df_packages)

        logging.info(f"Reading embeddings from `{embeddings_dataset_path}`...")
        df_embeddings = pl.read_parquet(embeddings_dataset_path)
        self._log_embeddings_dataset_info(df_embeddings)

        return df_packages, df_embeddings

    def _load_blob_dataset(self) -> Tuple[pl.DataFrame, pl.DataFrame]:
        blob_io = BlobIO(
            self.config.STORAGE_BACKEND_BLOB_ACCOUNT_NAME,
            self.config.STORAGE_BACKEND_BLOB_CONTAINER_NAME,
            self.config.STORAGE_BACKEND_BLOB_KEY,
        )

        logging.info(
            f"Downloading `{self.config.DATASET_FOR_API_CSV_NAME}` from container `{self.config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}`..."
        )
        df_packages = blob_io.download_csv_to_df(self.config.DATASET_FOR_API_CSV_NAME)
        self._log_packages_dataset_info(df_packages)

        logging.info(
            f"Downloading `{self.config.EMBEDDINGS_PARQUET_NAME}` from container `{self.config.STORAGE_BACKEND_BLOB_CONTAINER_NAME}`..."
        )
        df_embeddings = blob_io.download_parquet_to_df(self.config.EMBEDDINGS_PARQUET_NAME)
        self._log_embeddings_dataset_info(df_embeddings)

        return df_packages, df_embeddings

    def _log_packages_dataset_info(self, df_packages: pl.DataFrame) -> None:
        logging.info(f"Finished loading the `packages` dataset. Number of rows in dataset: {len(df_packages):,}")
        logging.info(df_packages.describe())

    def _log_embeddings_dataset_info(self, df_embeddings: pl.DataFrame) -> None:
        logging.info(f"Finished loading the `embeddings` dataset. Number of rows in dataset: {len(df_embeddings):,}")
        logging.info(df_embeddings.describe())
