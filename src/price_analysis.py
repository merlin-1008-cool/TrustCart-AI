import pandas as pd


def analyze_prices(df):
    """
    Analyze product prices across sellers.

    Calculates price differences against the market average
    and ranks sellers by product price.
    """

    required_columns = [
        "product_id",
        "product_name",
        "platform",
        "seller_name",
        "price",
        "market_average_price",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    result = df.copy()

    result["price_difference"] = (
        result["price"] - result["market_average_price"]
    ).round(2)

    result["price_difference_percent"] = (
        result["price_difference"]
        / result["market_average_price"].replace(0, float("nan"))
        * 100
    ).round(2)

    result["price_status"] = result["price_difference"].apply(
        lambda difference: (
            "Below Market Average"
            if difference < 0
            else "Above Market Average"
            if difference > 0
            else "At Market Average"
        )
    )

    result["price_rank"] = (
        result.groupby("product_name")["price"]
        .rank(method="min", ascending=True)
        .astype(int)
    )

    return result.sort_values(
        ["product_id", "price"],
        ascending=[True, True]
    ).reset_index(drop=True)


def get_best_price(df, product_name):
    """Return the lowest-priced listing for a product."""

    product_listings = df[
        df["product_name"].str.casefold()
        == product_name.casefold()
    ]

    if product_listings.empty:
        return None

    return product_listings.loc[
        product_listings["price"].idxmin()
    ]