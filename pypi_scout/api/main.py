import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from pypi_scout.api.utils import load_dataset
from pypi_scout.config import Config
from pypi_scout.utils.logging import setup_logging
from pypi_scout.utils.score_calculator import calculate_score
from pypi_scout.vector_database import VectorDatabaseInterface

setup_logging()
logging.info("Initializing backend...")

app = FastAPI()

load_dotenv()
config = Config()

origins = [
    "http://localhost:3000",
    "http://frontend-service:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = load_dataset(config.DATA_DIR / config.PROCESSED_DATASET_CSV_NAME)

model = SentenceTransformer(config.EMBEDDINGS_MODEL_NAME)

vector_database_interface = VectorDatabaseInterface(
    pinecone_token=config.PINECONE_TOKEN,
    pinecone_index_name=config.PINECONE_INDEX_NAME,
    embeddings_model=model,
    pinecone_namespace=config.PINECONE_NAMESPACE,
)


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


@app.post("/search/", response_model=SearchResponse)
async def search(query: QueryModel):
    """
    Search for the packages whose summary and description have the highest similarity to the query.
    We take the top_k * 2 most similar packages, and then calculate weighted score based on the similarity and weekly downloads.
    The top_k packages with the highest score are returned.
    """

    logging.info(f"Searching for similar projects. Query: '{query.query}'")
    df_matches = vector_database_interface.find_similar(query.query, top_k=query.top_k * 2)
    df_matches = df_matches.join(df, how="left", on="name")

    if df_matches["weekly_downloads"].is_null().any():
        logging.error(
            "One or more entries have 'None' for 'weekly_downloads'. "
            "This means they were found in the vector database but not in the local dataset."
        )
        logging.error(
            "The most likely cause is that the local dataset was generated with a lower config.FRAC_DATA_TO_INCLUDE "
            "value than the vector database."
        )
        logging.error("To solve this, delete the Pinecone index and rerun the setup script.")
        raise HTTPException(status_code=400, detail="One or more entries have 'None' for 'weekly_downloads'.")

    logging.info(
        f"Fetched the {len(df_matches)} most similar projects. Calculating the weighted scores and filtering..."
    )
    df_matches = calculate_score(
        df_matches, weight_similarity=config.WEIGHT_SIMILARITY, weight_weekly_downloads=config.WEIGHT_WEEKLY_DOWNLOADS
    )
    df_matches = df_matches.sort("score", descending=True)
    df_matches = df_matches.head(query.top_k)
    logging.info(f"Returning the {len(df_matches)} best matches.")
    return SearchResponse(matches=df_matches.to_dicts())
