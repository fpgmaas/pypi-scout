from unittest.mock import MagicMock

import numpy as np
import polars as pl
import pytest

from pypi_scout.vector_database.interface import VectorDatabaseInterface


@pytest.fixture
def mock_pinecone(mocker):
    mock_pinecone = mocker.patch("pypi_scout.vector_database.interface.Pinecone").return_value
    mock_index = MagicMock()
    mock_pinecone.Index.return_value = mock_index
    return mock_pinecone, mock_index


@pytest.fixture
def mock_model(mocker):
    return mocker.patch("pypi_scout.vector_database.interface.SentenceTransformer").return_value


@pytest.fixture
def vdb(mock_pinecone, mock_model):
    return VectorDatabaseInterface(
        pinecone_token="fake_token",  # noqa: S106
        pinecone_index_name="fake_index",
        pinecone_namespace="fake_namespace",
        embeddings_model=mock_model,
        batch_size=2,
    )


def test_initialization(mock_pinecone, mock_model, vdb):
    mock_pinecone[0].Index.assert_called_with("fake_index")
    assert vdb.pinecone_namespace == "fake_namespace"
    assert vdb.batch_size == 2
    assert vdb.model == mock_model


def test_find_similar(mock_model, vdb):
    # Mock the model.encode method
    mock_model.encode.return_value = np.array([0.1] * 768)

    # Mock the Pinecone query method
    vdb.index.query.return_value = {"matches": [{"id": "1", "score": 0.99}, {"id": "2", "score": 0.98}]}

    result_df = vdb.find_similar(query="test query", top_k=2)

    # Create expected DataFrame
    expected_df = pl.DataFrame([{"name": "1", "similarity": 0.99}, {"name": "2", "similarity": 0.98}])

    # Check that the result matches the expected DataFrame
    assert result_df.equals(expected_df)
