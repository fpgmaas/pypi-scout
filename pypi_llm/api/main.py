import polars as pl
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from pypi_llm.config import Config
from pypi_llm.vector_database import VectorDatabaseInterface

app = FastAPI()

load_dotenv()
config = Config()

df = pl.read_csv(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)
model = SentenceTransformer(config.EMBEDDINGS_MODEL_NAME)

vector_database_interface = VectorDatabaseInterface(
    pinecone_token=config.PINECONE_TOKEN, pinecone_index_name=config.PINECONE_INDEX_NAME, embeddings_model=model
)


class QueryModel(BaseModel):
    query: str


class Match(BaseModel):
    name: str
    similarity: float
    weekly_downloads: int


class MatchesResponse(BaseModel):
    matches: list[Match]


@app.get("/matches/", response_model=MatchesResponse)
async def get_matches(query: QueryModel):
    df_matches = vector_database_interface.find_similar(query.query)
    df_matches = df_matches.join(df, how="left", on="name")
    df_matches = df_matches.sort("similarity", descending=True)
    return MatchesResponse(matches=df_matches.to_dicts())
