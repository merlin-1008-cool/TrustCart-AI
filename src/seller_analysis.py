from src.data_loader import load_seller_data
from src.price_analysis import analyze_prices
from src.trust_score import (
    calculate_trust_score,
    classify_trust_level,
)


def analyze_sellers():
    """
    Combine price analysis and seller trust scoring.

    Trust scores are preliminary prototype indicators,
    not validated measures of real-world seller trust.
    """

    df = load_seller_data()

    # Analyze product prices and rankings
    df = analyze_prices(df)

    # Calculate a trust score for each seller
    df["trust_score"] = df.apply(
        calculate_trust_score,
        axis=1,
    )

    # Assign an understandable trust category
    df["trust_level"] = df["trust_score"].apply(
        classify_trust_level
    )

    return df