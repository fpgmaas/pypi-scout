import polars as pl
from dotenv import load_dotenv

from pypi_llm.config import Config
from pypi_llm.data.description_cleaner import CLEANING_FAILED, DescriptionCleaner
from pypi_llm.data.reader import DataReader
from pypi_llm.data.vector_database_upserter import VectorDatabaseUpserter

load_dotenv()
config = Config()

df = DataReader(config.DATA_DIR).read()

df = DescriptionCleaner().clean(df, "description", "description_cleaned")
df = df.filter(~pl.col("description_cleaned").is_null())
df = df.filter(pl.col("description_cleaned") != CLEANING_FAILED)

upserter = VectorDatabaseUpserter(
    pinecone_token=config.PINECONE_TOKEN,
    pinecone_index_name=config.PINECONE_INDEX_NAME,
    embeddings_model_name=config.EMBEDDINGS_MODEL,
)

upserter.upsert_polars(df, key_column="name", text_column="description_cleaned")
