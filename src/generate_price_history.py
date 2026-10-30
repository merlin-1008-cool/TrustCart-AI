from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = PROJECT_ROOT / "data" / "raw" / "products.csv"
RETAILERS_FILE = PROJECT_ROOT / "data" / "retailers.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "price_history.csv"

# Fixed seed ensures repeatable demonstration data.
rng = np.random.default_rng(42)

# Approximate reference prices in INR for demonstration purposes.
BASE_PRICES = {
    "P001": 54999,
    "P002": 49999,
    "P003": 54999,
    "P004": 49999,
    "P005": 59999,
    "P006": 99999,
    "P007": 24999,
    "P008": 24999,
    "P009": 9999,
    "P010": 19999,
    "P011": 24999,
    "P012": 22999,
    "P013": 32999,
    "P014": 34999,
    "P015": 17999,
    "P016": 49999,
    "P017": 99999,
    "P018": 59999,
    "P019": 9999,
    "P020": 4499,
    "P021": 4999,
}


def main():
    products = pd.read_csv(PRODUCTS_FILE)
    retailers = pd.read_csv(RETAILERS_FILE)

    # Weekly observations over approximately six months.
    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=26,
        freq="7D",
    )

    records = []

    for _, product in products.iterrows():
        product_id = product["product_id"]
        base_price = BASE_PRICES[product_id]

        # Each product is available from a consistent subset of retailers.
        available_count = int(rng.integers(6, len(retailers) + 1))
        available_indices = sorted(
            rng.choice(
                len(retailers),
                size=available_count,
                replace=False,
            ).tolist()
        )

        selected_retailers = retailers.iloc[available_indices]

        # Each retailer gets a stable pricing position for this product.
        retailer_factors = {
            row["retailer_id"]: float(rng.uniform(0.94, 1.09))
            for _, row in selected_retailers.iterrows()
        }

        # Gradual product-level variation across the six-month period.
        product_trend = rng.uniform(-0.06, 0.04)

        for _, retailer in selected_retailers.iterrows():
            retailer_id = retailer["retailer_id"]
            retailer_name = retailer["retailer_name"]
            retailer_factor = retailer_factors[retailer_id]

            for week_index, date in enumerate(dates):
                progress = week_index / max(len(dates) - 1, 1)

                trend_factor = 1 + product_trend * progress
                random_factor = rng.normal(1.0, 0.018)

                # Occasional temporary price reductions.
                promotion_factor = (
                    float(rng.uniform(0.90, 0.97))
                    if rng.random() < 0.12
                    else 1.0
                )

                simulated_price = round(
                    base_price
                    * retailer_factor
                    * trend_factor
                    * random_factor
                    * promotion_factor
                    / 100
                ) * 100

                records.append(
                    {
                        "product_id": product_id,
                        "product_name": product["product_name"],
                        "category": product["category"],
                        "retailer_id": retailer_id,
                        "retailer_name": retailer_name,
                        "date": date.strftime("%Y-%m-%d"),
                        "price_inr": int(simulated_price),
                        "data_type": "Simulated",
                    }
                )

    history = pd.DataFrame(records)
    history = history.sort_values(
        ["product_id", "retailer_name", "date"]
    ).reset_index(drop=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    history.to_csv(OUTPUT_FILE, index=False)

    print("SIMULATED PRICE HISTORY GENERATED")
    print("-" * 40)
    print(f"Products: {products['product_id'].nunique()}")
    print(f"Retailers in configuration: {len(retailers)}")
    print(f"Historical price records: {len(history)}")
    print(f"Observation dates: {history['date'].nunique()}")
    print(f"Categories: {history['category'].nunique()}")
    print(f"Output file: {OUTPUT_FILE}")
    print("\nRecords per category:")
    print(history.groupby("category").size().to_string())
    print("\nSample records:")
    print(history.head(5).to_string(index=False))
    print("\nAll records are marked as Simulated.")


if __name__ == "__main__":
    main()
