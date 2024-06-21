import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class StorageBackend(Enum):
    LOCAL = "LOCAL"
    BLOB = "BLOB"


@dataclass
class Config:
    # Name of the Pinecone index used for storing vector representations of the package descriptions.
    PINECONE_INDEX_NAME = "pypi"

    # Namespace within the Pinecone index to logically separate data.
    PINECONE_NAMESPACE = "ns1"

    # API token for authenticating with Pinecone. Should be set as an environment variable.
    PINECONE_TOKEN: str = field(default_factory=lambda: os.getenv("PINECONE_TOKEN"))

    # Name of the model used for generating vector embeddings from text.
    # See https://sbert.net/docs/sentence_transformer/pretrained_models.html for available models.
    EMBEDDINGS_MODEL_NAME = "all-mpnet-base-v2"

    # Dimension of the vector embeddings produced by the model. Should match the output of the model above.
    EMBEDDINGS_DIMENSION = 768

    # Boolean to overwrite existing files. e.g. re-download the raw dataset, upload processed dataset to blob, etc.
    OVERWRITE: bool = True

    # Directory where dataset files are stored.
    DATA_DIR: Path = Path("data")

    # Filename for the raw dataset CSV.
    RAW_DATASET_CSV_NAME = "raw_dataset.csv"

    # Filename for the processed dataset CSV.
    PROCESSED_DATASET_CSV_NAME = "processed_dataset.csv"

    # Google Drive file ID for downloading the raw dataset.
    GOOGLE_FILE_ID = "1huR7-VD3AieBRCcQyRX9MWbPLMb_czjq"

    # Number of top results to return for a query.
    N_RESULTS_TO_RETURN = 30

    # Fraction of the dataset to include in the vector database. This value determines the portion of top packages
    # (sorted by weekly downloads) to include. Increase this value to include a larger portion of the dataset, up to 1.0 (100%).
    # For reference, a value of 0.25 corresponds to including all PyPI packages with at least approximately 650 weekly downloads
    FRAC_DATA_TO_INCLUDE = 0.25

    # Weights for the combined score calculation. Higher WEIGHT_SIMILARITY prioritizes
    # relevance based on text similarity, while higher WEIGHT_WEEKLY_DOWNLOADS prioritizes
    # packages with more weekly downloads.
    WEIGHT_SIMILARITY = 0.8
    WEIGHT_WEEKLY_DOWNLOADS = 0.2

    # Storage backend configuration. Can be either StorageBackend.LOCAL or StorageBackend.BLOB.
    # If StorageBackend.BLOB, the processed dataset will be uploaded to Blob, and the backend API
    # will read the data from there, rather than from a local data directory. In order to use StorageBackend.BLOB,
    # the other `STORAGE_BACKEND_BLOB_` variables need to be set as environment variables.
    STORAGE_BACKEND: StorageBackend = StorageBackend.LOCAL
    STORAGE_BACKEND_BLOB_ACCOUNT_NAME: str | None = None
    STORAGE_BACKEND_BLOB_CONTAINER_NAME: str | None = None
    STORAGE_BACKEND_BLOB_KEY: str | None = None

    def __post_init__(self) -> None:
        if not self.PINECONE_TOKEN:
            raise OSError("PINECONE_TOKEN not found in environment variables")  # noqa: TRY003

        if os.getenv("STORAGE_BACKEND") == "BLOB":
            self.STORAGE_BACKEND = StorageBackend.BLOB
            self.STORAGE_BACKEND_BLOB_ACCOUNT_NAME = os.getenv("STORAGE_BACKEND_BLOB_ACCOUNT_NAME")
            self.STORAGE_BACKEND_BLOB_CONTAINER_NAME = os.getenv("STORAGE_BACKEND_BLOB_CONTAINER_NAME")
            self.STORAGE_BACKEND_BLOB_KEY = os.getenv("STORAGE_BACKEND_BLOB_KEY")

            if not all(
                [
                    self.STORAGE_BACKEND_BLOB_ACCOUNT_NAME,
                    self.STORAGE_BACKEND_BLOB_CONTAINER_NAME,
                    self.STORAGE_BACKEND_BLOB_KEY,
                ]
            ):
                raise OSError("One or more BLOB storage environment variables are missing!")  # noqa: TRY003
