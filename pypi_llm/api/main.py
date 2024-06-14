import polars as pl
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from pypi_llm.config import Config
from pypi_llm.vector_database import VectorDatabaseInterface

app = FastAPI()

# Load environment variables
load_dotenv()
config = Config()

# Setup CORS
origins = [
    "http://localhost:3000",
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset and model
df = pl.read_csv(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)
model = SentenceTransformer(config.EMBEDDINGS_MODEL_NAME)

# Initialize vector database interface
vector_database_interface = VectorDatabaseInterface(
    pinecone_token=config.PINECONE_TOKEN, pinecone_index_name=config.PINECONE_INDEX_NAME, embeddings_model=model
)


# Define request and response models
class QueryModel(BaseModel):
    query: str


class Match(BaseModel):
    name: str
    summary: str
    similarity: float
    weekly_downloads: int


class SearchResponse(BaseModel):
    matches: list[Match]


# Define search endpoint
@app.post("/search/", response_model=SearchResponse)
async def search(query: QueryModel):
    df_matches = vector_database_interface.find_similar(query.query, top_k=50)
    df_matches = df_matches.join(df, how="left", on="name")
    df_matches = df_matches.sort("similarity", descending=True)
    return SearchResponse(matches=df_matches.to_dicts())
