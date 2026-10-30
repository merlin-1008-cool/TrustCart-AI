from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

HISTORY_FILE = PROJECT_ROOT / "data" / "raw" / "price_history.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "deal_analysis.csv"


def analyze_deals(history: pd.DataFrame) -> pd.DataFrame:
    """Evaluate simulated offers using historical and cross-retailer prices."""

    required_columns = [
        "product_id",
        "product_name",
        "category",
        "retailer_id",
        "retailer_name",
        "date",
        "price_inr",
        "data_type",
    ]

    missing = [col for col in required_columns if col not in history.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if history.empty:
        raise ValueError("Price history dataset is empty.")

    data = history.copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    data["price_inr"] = pd.to_numeric(data["price_inr"], errors="raise")

    if (data["price_inr"] <= 0).any():
        raise ValueError("Prices must be greater than zero.")

    results = []

    # Assess the latest recorded price for each product-retailer pair.
    latest = (
        data.sort_values("date")
        .groupby(["product_id", "retailer_id"], as_index=False)
        .tail(1)
    )

    for _, listing in latest.iterrows():
        product_id = listing["product_id"]
        retailer_id = listing["retailer_id"]

        product_history = data[data["product_id"] == product_id]
        retailer_history = product_history[
            product_history["retailer_id"] == retailer_id
        ]

        current_price = float(listing["price_inr"])
        historical_min = float(retailer_history["price_inr"].min())
        historical_average = float(retailer_history["price_inr"].mean())

        # Compare the latest prices recorded across retailers for this product.
        latest_product_prices = latest[latest["product_id"] == product_id]
        market_average = float(latest_product_prices["price_inr"].mean())
        market_minimum = float(latest_product_prices["price_inr"].min())

        historical_savings_percent = (
            (historical_average - current_price) / historical_average * 100
        )

        market_difference_percent = (
            (current_price - market_average) / market_average * 100
        )

        # Conservative labels based on historical and market comparisons.
        if (
            current_price <= historical_min * 1.01
            and current_price <= market_average * 0.97
        ):
            assessment = "Excellent Value"
        elif (
            current_price < historical_average * 0.97
            and current_price < market_average
        ):
            assessment = "Good Deal"
        elif current_price <= market_average * 1.03:
            assessment = "Average Price"
        else:
            assessment = "Compare Before Buying"

        results.append(
            {
                "product_id": product_id,
                "product_name": listing["product_name"],
                "category": listing["category"],
                "retailer_id": retailer_id,
                "retailer_name": listing["retailer_name"],
                "latest_price_inr": round(current_price, 2),
                "historical_min_inr": round(historical_min, 2),
                "historical_average_inr": round(historical_average, 2),
                "market_minimum_inr": round(market_minimum, 2),
                "market_average_inr": round(market_average, 2),
                "below_historical_average_percent": round(
                    historical_savings_percent, 2
                ),
                "difference_from_market_average_percent": round(
                    market_difference_percent, 2
                ),
                "deal_assessment": assessment,
                "data_type": "Simulated",
            }
        )

    return pd.DataFrame(results).sort_values(
        ["category", "product_name", "latest_price_inr"]
    ).reset_index(drop=True)


def main():
    if not HISTORY_FILE.exists():
        raise FileNotFoundError(
            f"Price history not found: {HISTORY_FILE}. "
            "Run src/generate_price_history.py first."
        )

    history = pd.read_csv(HISTORY_FILE)
    results = analyze_deals(history)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    print("TRUSTCART AI - DEAL ANALYSIS")
    print("-" * 40)
    print(f"Listings analysed: {len(results)}")
    print(f"Products analysed: {results['product_id'].nunique()}")
    print(f"Categories covered: {results['category'].nunique()}")
    print("\nDeal assessment counts:")
    print(results["deal_assessment"].value_counts().to_string())
    print("\nSample results:")
    print(
        results[
            [
                "product_name",
                "retailer_name",
                "latest_price_inr",
                "historical_average_inr",
                "deal_assessment",
            ]
        ].head(10).to_string(index=False)
    )
    print(f"\nSaved results to: {OUTPUT_FILE}")
    print("All prices are simulated demonstration data.")


if __name__ == "__main__":
    main()
