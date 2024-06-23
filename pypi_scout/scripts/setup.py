import logging

from pypi_scout.scripts.create_vector_embeddings import create_vector_embeddings
from pypi_scout.scripts.download_raw_dataset import download_raw_dataset
from pypi_scout.scripts.process_raw_dataset import process_raw_dataset
from pypi_scout.scripts.upload_processed_datasets import upload_processed_datasets
from pypi_scout.utils.logging import setup_logging


def main():
    setup_logging()

    logging.info("\n\nDOWNLOADING RAW DATASET -------------\n")
    download_raw_dataset()

    logging.info("\n\nPROCESSING RAW DATASET -------------\n")
    process_raw_dataset()

    logging.info("\n\nCREATING VECTOR EMBEDDINGS -------------\n")
    create_vector_embeddings()

    logging.info("\n\nUPLOADING PROCESSED DATASETS -------------\n")
    upload_processed_datasets()


if __name__ == "__main__":
    main()
