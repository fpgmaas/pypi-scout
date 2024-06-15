import polars as pl
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from pypi_llm.config import Config
from pypi_llm.utils.score_calculator import calculate_score
from pypi_llm.vector_database import VectorDatabaseInterface

app = FastAPI()

load_dotenv()
config = Config()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pl.read_csv(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)
model = SentenceTransformer(config.EMBEDDINGS_MODEL_NAME)

vector_database_interface = VectorDatabaseInterface(
    pinecone_token=config.PINECONE_TOKEN,
    pinecone_index_name=config.PINECONE_INDEX_NAME,
    embeddings_model=model,
    pinecone_namespace=config.PINECONE_NAMESPACE,
)


class QueryModel(BaseModel):
    query: str
    top_k: int = 30


class Match(BaseModel):
    name: str
    summary: str
    similarity: float
    weekly_downloads: int


class SearchResponse(BaseModel):
    matches: list[Match]


@app.post("/search/", response_model=SearchResponse)
async def search(query: QueryModel):
    df_matches = vector_database_interface.find_similar(query.query, top_k=query.top_k * 2)
    df_matches = df_matches.join(df, how="left", on="name")

    df_matches = calculate_score(df_matches)
    df_matches = df_matches.sort("score", descending=True)
    df_matches = df_matches.head(query.top_k)

    print("sending")
    return SearchResponse(matches=df_matches.to_dicts())
