from pypi_scout.scripts.download_dataset import download_dataset
from pypi_scout.scripts.process_dataset import process_dataset
from pypi_scout.scripts.setup_pinecone import setup_pinecone
from pypi_scout.scripts.upsert_data import upsert_data
from pypi_scout.utils.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    setup_pinecone()
    download_dataset()
    process_dataset()
    upsert_data()
