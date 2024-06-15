import logging

import polars as pl
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from pypi_llm.config import Config
from pypi_llm.utils.logging import setup_logging
from pypi_llm.vector_database import VectorDatabaseInterface

setup_logging()

if __name__ == "__main__":
    """
    Upserts data from a processed dataset CSV into a vector database.
    """
    load_dotenv()
    config = Config()

    logging.info("Reading the processed dataset...")
    df = pl.read_csv(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)

    logging.info("Connecting to the vector database..")
    vector_database_interface = VectorDatabaseInterface(
        pinecone_token=config.PINECONE_TOKEN,
        pinecone_index_name=config.PINECONE_INDEX_NAME,
        embeddings_model=SentenceTransformer(config.EMBEDDINGS_MODEL_NAME),
        pinecone_namespace=config.PINECONE_NAMESPACE,
    )

    logging.info("Upserting data into the vector database..")
    df = df.with_columns(
        summary_and_description_cleaned=pl.concat_str(pl.col("summary"), pl.lit(" - "), pl.col("description_cleaned"))
    )
    vector_database_interface.upsert_polars(df, key_column="name", text_column="summary_and_description_cleaned")
    logging.info("Done!")
