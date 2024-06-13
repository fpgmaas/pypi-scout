from dotenv import load_dotenv
from pypi_llm.config import Config
from pinecone import Pinecone, ServerlessSpec


if __name__ =="__main__":

    load_dotenv()
    config = Config()

    pc = Pinecone(api_key=config.PINECONE_TOKEN)

    pc.create_index(
        name=config.PINECONE_INDEX_NAME,
        dimension=config.EMBEDDINGS_DIMENSION,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )