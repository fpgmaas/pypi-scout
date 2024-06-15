import logging

import polars as pl
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from pypi_scout.config import Config
from pypi_scout.utils.logging import setup_logging
from pypi_scout.vector_database import VectorDatabaseInterface


def upsert_data():
    """
    Upserts data from a processed dataset CSV into a vector database.
    """
    load_dotenv()
    config = Config()

    logging.info("Reading the processed dataset...")
    df = pl.read_csv(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)

    if config.FRAC_DATA_TO_INCLUDE < 1.0:
        logging.info(
            f"Using only the packages with weekly_downloads in the top {config.FRAC_DATA_TO_INCLUDE * 100}% of the dataset because config.FRAC_DATA_TO_INCLUDE is set to {config.FRAC_DATA_TO_INCLUDE}!"
        )
        logging.info(
            "This can be useful for testing purposes and to quickly get started. To include the entire dataset, set config.FRAC_DATA_TO_INCLUDE to 1.0."
        )
        df = df.sort("weekly_downloads", descending=True)
        df = df.head(round(config.FRAC_DATA_TO_INCLUDE * len(df)))

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


if __name__ == "__main__":
    setup_logging()
    upsert_data()
