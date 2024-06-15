import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    PINECONE_INDEX_NAME = "pypi"
    PINECONE_NAMESPACE = "ns1"
    PINECONE_TOKEN: str = field(default_factory=lambda: os.getenv("PINECONE_TOKEN"))

    EMBEDDINGS_MODEL_NAME = "all-mpnet-base-v2"
    EMBEDDINGS_DIMENSION = 768

    DATA_DIR: Path = Path("data")
    RAW_DATASET_CSV_NAME = "raw_dataset.csv"
    PROCESSED_DATASET_CSV_NAME = "processed_dataset.csv"
    GOOGLE_FILE_ID = "1huR7-VD3AieBRCcQyRX9MWbPLMb_czjq"

    def __post_init__(self):
        if not self.PINECONE_TOKEN:
            raise OSError("PINECONE_TOKEN not found in environment variables")  # noqa: TRY003
