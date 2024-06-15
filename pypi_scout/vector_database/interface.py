import polars as pl
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class VectorDatabaseInterface:
    """
    A class that provides an interface for interacting with a vector database.

    Args:
        pinecone_token (str): The Pinecone API token.
        pinecone_index_name (str): The name of the Pinecone index.
        pinecone_namespace (str): The namespace for the Pinecone index.
        embeddings_model (SentenceTransformer): The sentence transformer model for encoding text into embeddings.
        batch_size (int, optional): The batch size for upserting data. Defaults to 250.
    """

    def __init__(
        self,
        pinecone_token: str,
        pinecone_index_name: str,
        pinecone_namespace: str,
        embeddings_model: SentenceTransformer,
        batch_size: int = 128,
    ):
        self.batch_size = batch_size
        self.model = embeddings_model
        pc = Pinecone(api_key=pinecone_token)
        self.index = pc.Index(pinecone_index_name)
        self.pinecone_namespace = pinecone_namespace

    def upsert_polars(self, df: pl.DataFrame, key_column: str, text_column: str):
        """
        Upserts the data from a Polars DataFrame into the vector database.

        Args:
            df (pl.DataFrame): The Polars DataFrame containing the data to be upserted.
            key_column (str): The name of the column in the DataFrame containing the unique keys.
            text_column (str): The name of the column in the DataFrame containing the text data.
        """
        df_chunks = self._split_dataframe_in_batches(df)
        for chunk in tqdm(df_chunks, desc="Upserting batches", unit="batch"):
            self._upsert_chunk(chunk, key_column, text_column)

    def find_similar(self, query: str, top_k: int = 25) -> pl.DataFrame:
        """
        Finds similar vectors in the database for a given query.

        Args:
            query (str): The query string.
            top_k (int, optional): The number of similar vectors to retrieve. Defaults to 25.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the similar vectors and their similarity scores.
        """
        embeddings = self.model.encode(query)
        matches = self.index.query(
            namespace=self.pinecone_namespace, vector=embeddings.tolist(), top_k=top_k, include_values=False
        )
        return pl.from_dicts([{"name": x["id"], "similarity": x["score"]} for x in matches["matches"]])

    def _upsert_chunk(self, chunk: pl.DataFrame, key_column: str, text_column: str):
        embeddings = self.model.encode(list(chunk[text_column]), show_progress_bar=False)
        vectors = [
            {"id": project_name, "values": embedding} for project_name, embedding in zip(chunk[key_column], embeddings)
        ]
        self.index.upsert(vectors=vectors, namespace=self.pinecone_namespace, show_progress=False)

    def _split_dataframe_in_batches(self, df):
        n_chunks = (df.height + self.batch_size - 1) // self.batch_size
        return [df.slice(i * self.batch_size, self.batch_size) for i in range(n_chunks)]
