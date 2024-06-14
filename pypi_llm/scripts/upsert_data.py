import polars as pl
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from pypi_llm.config import Config
from pypi_llm.data.description_cleaner import CLEANING_FAILED, DescriptionCleaner
from pypi_llm.data.reader import DataReader
from pypi_llm.vector_database import VectorDatabaseInterface

if __name__ == "__main__":
    load_dotenv()
    config = Config()

    df = DataReader(config.DATA_DIR).read()

    df = DescriptionCleaner().clean(df, "description", "description_cleaned")
    df = df.filter(~pl.col("description_cleaned").is_null())
    df = df.filter(pl.col("description_cleaned") != CLEANING_FAILED)

    df.write_csv(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)

    vector_database_interface = VectorDatabaseInterface(
        pinecone_token=config.PINECONE_TOKEN,
        pinecone_index_name=config.PINECONE_INDEX_NAME,
        embeddings_model=SentenceTransformer(config.EMBEDDINGS_MODEL_NAME),
    )

    df = df.with_columns(
        summary_and_description_cleaned=pl.concat_str(pl.col("summary"), pl.lit(" "), pl.col("description_cleaned"))
    )
    vector_database_interface.upsert_polars(df, key_column="name", text_column="summary_and_description_cleaned")
