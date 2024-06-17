import argparse
from pypi_scout.scripts.download_dataset import download_dataset
from pypi_scout.scripts.process_dataset import process_dataset
from pypi_scout.scripts.setup_pinecone import setup_pinecone
from pypi_scout.scripts.upsert_data import upsert_data
from pypi_scout.utils.logging import setup_logging

def main(no_upsert):
    setup_logging()
    setup_pinecone()
    download_dataset()
    process_dataset()
    if not no_upsert:
        upsert_data()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the setup script with optional flags.")
    parser.add_argument('--no-upsert', action='store_true', help='If set, do not upsert data to the Pinecone database.')
    
    args = parser.parse_args()
    
    main(no_upsert=args.no_upsert)
