import pandas as pd
from pathlib import Path


def load_seller_data():
    """Load seller data from the project's raw CSV dataset."""

    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "raw" / "seller_data.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Seller dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    required_columns = [
        "product_id",
        "product_name",
        "platform",
        "seller_name",
        "price",
        "market_average_price",
        "rating",
        "reviews_count",
        "return_policy",
        "warranty_available",
        "verified_seller",
        "complaint_count",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("The seller dataset contains no records.")

    return df