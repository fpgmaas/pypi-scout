import argparse
import logging

from pypi_scout.scripts.download_raw_dataset import download_raw_dataset
from pypi_scout.scripts.process_raw_dataset import process_raw_dataset
from pypi_scout.scripts.setup_pinecone import setup_pinecone
from pypi_scout.scripts.upload_processed_datasets import upload_processed_datasets
from pypi_scout.scripts.upsert_data import upsert_data
from pypi_scout.utils.logging import setup_logging


def main(no_upsert):
    setup_logging()

    logging.info("\n\nSETTING UP PINECONE -------------\n")
    setup_pinecone()

    logging.info("\n\nDOWNLOADING RAW DATASET -------------\n")
    download_raw_dataset()

    logging.info("\n\nPROCESSING RAW DATASET -------------\n")
    process_raw_dataset()

    logging.info("\n\nUPLOADING PROCESSED DATASETS -------------\n")
    upload_processed_datasets()
    if not no_upsert:
        logging.info("\n\nUPSERTING DATA TO PINECONE -------------\n")
        upsert_data()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the setup script with optional flags.")
    parser.add_argument("--no-upsert", action="store_true", help="If set, do not upsert data to the Pinecone database.")

    args = parser.parse_args()

    main(no_upsert=args.no_upsert)
