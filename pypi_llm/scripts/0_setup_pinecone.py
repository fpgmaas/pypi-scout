import logging

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

from pypi_llm.config import Config
from pypi_llm.utils.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    """
    This script sets up a Pinecone index for storing embeddings.

    It loads the environment variables from a .env file, creates a Pinecone client,
    and creates an index with the specified name, dimension, metric, and serverless specification.
    """

    load_dotenv()
    config = Config()

    logging.info("Connection to Pinecone..")
    pc = Pinecone(api_key=config.PINECONE_TOKEN)

    logging.info("Creating Pinecone index..")
    pc.create_index(
        name=config.PINECONE_INDEX_NAME,
        dimension=config.EMBEDDINGS_DIMENSION,
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    logging.info("Done!")
