import logging

import polars as pl
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

from pypi_scout.api.data_loader import ApiDataLoader
from pypi_scout.config import Config
from pypi_scout.embeddings.simple_vector_database import SimpleVectorDatabase
from pypi_scout.utils.logging import setup_logging
from pypi_scout.utils.score_calculator import calculate_score

# Setup logging
setup_logging()
logging.info("Initializing backend...")

# Initialize limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Load environment variables and configuration
load_dotenv()
config = Config()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporary wildcard for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_loader = ApiDataLoader(config)
df_packages, df_embeddings = data_loader.load_dataset()

model = SentenceTransformer(config.EMBEDDINGS_MODEL_NAME)

vector_database = SimpleVectorDatabase(embeddings_model=model, df_embeddings=df_embeddings)


class QueryModel(BaseModel):
    query: str
    top_k: int = config.N_RESULTS_TO_RETURN


class Match(BaseModel):
    name: str
    summary: str
    similarity: float
    weekly_downloads: int


class SearchResponse(BaseModel):
    matches: list[Match]
    warning: bool = False
    warning_message: str = None


@app.post("/api/search", response_model=SearchResponse)
@limiter.limit("4/minute")
async def search(query: QueryModel, request: Request):
    """
    Search for the packages whose summary and description have the highest similarity to the query.
    We take the top_k * 2 most similar packages, and then calculate weighted score based on the similarity and weekly downloads.
    The top_k packages with the highest score are returned.
    """

    if query.top_k > 60:
        raise HTTPException(status_code=400, detail="top_k cannot be larger than 100.")

    logging.info(f"Searching for similar projects. Query: '{query.query}'")
    df_matches = vector_database.find_similar(query.query, top_k=query.top_k * 2)
    df_matches = df_matches.join(df_packages, how="left", on="name")
    logging.info(
        f"Fetched the {len(df_matches)} most similar projects. Calculating the weighted scores and filtering..."
    )

    warning = False
    warning_message = ""
    matches_missing_in_local_dataset = df_matches.filter(pl.col("weekly_downloads").is_null())["name"].to_list()
    if matches_missing_in_local_dataset:
        warning = True
        warning_message = (
            f"The following entries have 'None' for 'weekly_downloads': {matches_missing_in_local_dataset}. "
            "These entries were found in the vector database but not in the local dataset and have been excluded from the results."
        )
        logging.error(warning_message)
        df_matches = df_matches.filter(~pl.col("name").is_in(matches_missing_in_local_dataset))

    df_matches = calculate_score(
        df_matches, weight_similarity=config.WEIGHT_SIMILARITY, weight_weekly_downloads=config.WEIGHT_WEEKLY_DOWNLOADS
    )
    df_matches = df_matches.sort("score", descending=True)

    if len(df_matches) > query.top_k:
        df_matches = df_matches.head(query.top_k)

    logging.info(f"Returning the {len(df_matches)} best matches.")
    df_matches = df_matches.select(["name", "similarity", "summary", "weekly_downloads"])
    return SearchResponse(matches=df_matches.to_dicts(), warning=warning, warning_message=warning_message)
