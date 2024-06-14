import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    DATA_DIR: Path = Path("data")
    PINECONE_INDEX_NAME = "pypi"
    PINECONE_TOKEN: str = field(default_factory=lambda: os.getenv("PINECONE_TOKEN"))
    EMBEDDINGS_MODEL = "all-mpnet-base-v2"
    EMBEDDINGS_DIMENSION = 768

    def __post_init__(self):
        if not self.PINECONE_TOKEN:
            raise OSError("PINECONE_TOKEN not found in environment variables")  # noqa: TRY003
