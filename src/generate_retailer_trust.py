from pathlib import Path
import hashlib

import pandas as pd


# =========================================================
# FILE PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[1]

PRODUCTS_FILE = ROOT / "data" / "raw" / "products.csv"
RETAILERS_FILE = ROOT / "data" / "retailers.csv"
HISTORY_FILE = ROOT / "data" / "raw" / "price_history.csv"

OUTPUT_FILE = (
    ROOT / "data" / "raw" / "retailer_trust.csv"
)


# =========================================================
# LOAD EXISTING DATA
# =========================================================

for file_path in [
    PRODUCTS_FILE,
    RETAILERS_FILE,
    HISTORY_FILE,
]:

    if not file_path.exists():

        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )


products = pd.read_csv(PRODUCTS_FILE)

retailers = pd.read_csv(RETAILERS_FILE)

history = pd.read_csv(HISTORY_FILE)

history["date"] = pd.to_datetime(
    history["date"],
    errors="coerce",
)

history["price_inr"] = pd.to_numeric(
    history["price_inr"],
    errors="coerce",
)


# =========================================================
# GET LATEST SIMULATED PRICE FOR EACH LISTING
# =========================================================

latest = (
    history.dropna(
        subset=["date", "price_inr"]
    )
    .sort_values("date")
    .groupby(
        [
            "product_id",
            "retailer_id",
            "retailer_name",
        ],
        as_index=False,
    )
    .tail(1)
)


# =========================================================
# CREATE SIMULATED TRUST INDICATORS
# =========================================================

rows = []

for _, listing in latest.iterrows():

    unique_key = (
        f"{listing['product_id']}|"
        f"{listing['retailer_id']}"
    )

    seed = int(
        hashlib.sha256(
            unique_key.encode("utf-8")
        ).hexdigest()[:8],
        16,
    )

    # These values are generated for demonstration only.
    rating = round(
        3.2 + (seed % 19) / 10,
        1,
    )

    reviews_count = 35 + (seed % 2400)

    verified_seller = seed % 5 != 0

    complaint_count = seed % 75

    return_policy = seed % 4 != 0

    warranty_available = seed % 3 != 0

    rows.append(
        {
            "product_id": listing["product_id"],
            "product_name": listing["product_name"],
            "category": listing["category"],
            "retailer_id": listing["retailer_id"],
            "retailer_name": listing["retailer_name"],
            "price_inr": round(
                float(listing["price_inr"]),
                2,
            ),
            "verified_seller": verified_seller,
            "rating": min(rating, 5.0),
            "reviews_count": int(reviews_count),
            "complaint_count": int(complaint_count),
            "return_policy": return_policy,
            "return_details": (
                "Illustrative return/exchange policy"
                if return_policy
                else "Not listed in demo data"
            ),
            "warranty_available": warranty_available,
            "warranty_details": (
                "Illustrative warranty indicator"
                if warranty_available
                else "Not listed in demo data"
            ),
            "data_type": "Simulated",
        }
    )


# =========================================================
# SAVE DATASET
# =========================================================

result = pd.DataFrame(rows)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

result.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("Retailer trust dataset created successfully.")

print(f"File: {OUTPUT_FILE}")

print(
    f"Product-retailer listings: {len(result)}"
)

print(
    "IMPORTANT: Ratings, reviews, verification, complaints, "
    "returns and warranty values are simulated."
)