import tempfile
from io import BytesIO

import polars as pl
from azure.storage.blob import BlobServiceClient


class BlobIO:
    def __init__(self, account_name: str, container_name: str, account_key: str):
        self.account_name = account_name
        self.container_name = container_name
        self.account_key = account_key
        self.service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key
        )
        self.container_client = self.service_client.get_container_client(container_name)

    def upload_csv(self, data_frame: pl.DataFrame, blob_name: str) -> None:
        csv_buffer = BytesIO()
        data_frame.write_csv(csv_buffer)
        csv_buffer.seek(0)  # Reset buffer position to the beginning
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(csv_buffer, overwrite=True)

    def upload_local_csv(self, local_file_path: str, blob_name: str) -> None:
        with open(local_file_path, "rb") as data:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(data, overwrite=True)

    def download_csv(self, blob_name: str) -> pl.DataFrame:
        blob_client = self.container_client.get_blob_client(blob_name)
        download_stream = blob_client.download_blob()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            # Download the blob content into the temporary file
            temp_file.write(download_stream.readall())
            temp_file.flush()

            # Read the CSV using Polars
            df = pl.read_csv(temp_file.name)

        return df

    def exists(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.exists()
