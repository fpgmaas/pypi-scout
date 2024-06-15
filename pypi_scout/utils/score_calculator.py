import polars as pl


def calculate_score(
    df: pl.DataFrame, weight_similarity: float = 0.5, weight_weekly_downloads: float = 0.5
) -> pl.DataFrame:
    """
    Calculate a combined score based on similarity and weekly downloads.

    The function ranks the similarity and weekly downloads, normalizes these ranks to a [0, 1] scale,
    and then computes a combined score based on the provided weights for similarity and weekly downloads.
    The DataFrame is sorted by the combined score in descending order.

    Args:
        df (pl.DataFrame): DataFrame containing 'similarity' and 'weekly_downloads' columns.
        weight_similarity (float): Weight for the similarity score in the combined score calculation. Default is 0.5.
        weight_weekly_downloads (float): Weight for the weekly downloads score in the combined score calculation. Default is 0.5.

    """
    df = df.with_columns(
        rank_similarity=pl.col("similarity").rank("dense", descending=False),
        rank_weekly_downloads=pl.col("weekly_downloads").rank("dense", descending=False),
    )

    df = df.with_columns(
        normalized_similarity=(pl.col("rank_similarity") - 1) / (df["rank_similarity"].max() - 1),
        normalized_weekly_downloads=(pl.col("rank_weekly_downloads") - 1) / (df["rank_weekly_downloads"].max() - 1),
    )

    df = df.with_columns(
        score=weight_similarity * pl.col("normalized_similarity")
        + weight_weekly_downloads * pl.col("normalized_weekly_downloads")
    )

    df = df.sort("score", descending=True)
    return df
