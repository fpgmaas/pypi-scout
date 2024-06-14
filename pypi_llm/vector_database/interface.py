import polars as pl
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class VectorDatabaseInterface:
    def __init__(
        self,
        pinecone_token: str,
        pinecone_index_name: str,
        pinecone_namespace: str,
        embeddings_model: SentenceTransformer,
        batch_size: int = 250,
    ):
        self.batch_size = batch_size
        self.model = embeddings_model
        pc = Pinecone(api_key=pinecone_token)
        self.index = pc.Index(pinecone_index_name)
        self.pinecone_namespace = pinecone_namespace

    def upsert_polars(self, df: pl.DataFrame, key_column: str, text_column: str):
        df_chunks = self._split_dataframe_in_batches(df)
        for chunk in tqdm(df_chunks, desc="Upserting batches", unit="batch"):
            self._upsert_chunk(chunk, key_column, text_column)

    def find_similar(self, query: str, top_k: int = 25) -> pl.DataFrame:
        embeddings = self.model.encode(query)
        matches = self.index.query(
            namespace=self.pinecone_namespace, vector=embeddings.tolist(), top_k=top_k, include_values=False
        )
        return pl.from_dicts([{"name": x["id"], "similarity": x["score"]} for x in matches["matches"]])

    def _upsert_chunk(self, chunk: pl.DataFrame, key_column: str, text_column: str):
        embeddings = self.model.encode(list(chunk[text_column]))
        vectors = [
            {"id": project_name, "values": embedding} for project_name, embedding in zip(chunk[key_column], embeddings)
        ]
        self.index.upsert(vectors=vectors, namespace=self.pinecone_namespace)

    def _split_dataframe_in_batches(self, df):
        n_chunks = (df.height + self.batch_size - 1) // self.batch_size
        return [df.slice(i * self.batch_size, self.batch_size) for i in range(n_chunks)]
