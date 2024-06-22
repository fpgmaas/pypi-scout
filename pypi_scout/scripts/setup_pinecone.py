import logging

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from pinecone.core.client.exceptions import PineconeApiException

from pypi_scout.config import Config
from pypi_scout.utils.logging import setup_logging


def setup_pinecone():
    """
    This script sets up a Pinecone index for storing embeddings.

    It loads the environment variables from a .env file, creates a Pinecone client,
    and creates an index with the specified name, dimension, metric, and serverless specification.
    """

    load_dotenv()
    config = Config()

    logging.info("🔗 Connecting to Pinecone..")
    pc = Pinecone(api_key=config.PINECONE_TOKEN)

    try:
        logging.info("Creating Pinecone index..")
        pc.create_index(
            name=config.PINECONE_INDEX_NAME,
            dimension=config.EMBEDDINGS_DIMENSION,
            metric="dotproduct",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        logging.info("✅ Pinecone index created successfully.")
    except PineconeApiException as e:
        if e.status == 409:
            logging.warning(f"🔹 Pinecone index '{config.PINECONE_INDEX_NAME}' already exists.")
        else:
            logging.exception("❌ An error occurred while creating the Pinecone index.")


if __name__ == "__main__":
    setup_logging()
    setup_pinecone()
