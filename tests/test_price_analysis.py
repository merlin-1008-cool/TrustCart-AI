import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.price_analysis import analyze_prices, get_best_price


def test_price_difference_and_status():
    df = pd.DataFrame([
        {
            "product_id": "P001",
            "product_name": "Samsung Galaxy S24",
            "platform": "ShopA",
            "seller_name": "TechWorld",
            "price": 54999,
            "market_average_price": 59999,
        }
    ])

    result = analyze_prices(df)

    assert result.loc[0, "price_difference"] == -5000
    assert result.loc[0, "price_status"] == "Below Market Average"


def test_price_ranking():
    df = pd.DataFrame([
        {
            "product_id": "P001",
            "product_name": "Samsung Galaxy S24",
            "platform": "ShopA",
            "seller_name": "TechWorld",
            "price": 54999,
            "market_average_price": 59999,
        },
        {
            "product_id": "P001",
            "product_name": "Samsung Galaxy S24",
            "platform": "ShopB",
            "seller_name": "MobileDeals",
            "price": 44999,
            "market_average_price": 59999,
        }
    ])

    result = analyze_prices(df)

    cheapest = result[result["seller_name"] == "MobileDeals"].iloc[0]
    expensive = result[result["seller_name"] == "TechWorld"].iloc[0]

    assert cheapest["price_rank"] == 1
    assert expensive["price_rank"] == 2


def test_get_best_price():
    df = pd.DataFrame([
        {
            "product_id": "P001",
            "product_name": "Samsung Galaxy S24",
            "platform": "ShopA",
            "seller_name": "TechWorld",
            "price": 54999,
            "market_average_price": 59999,
        },
        {
            "product_id": "P001",
            "product_name": "Samsung Galaxy S24",
            "platform": "ShopB",
            "seller_name": "MobileDeals",
            "price": 44999,
            "market_average_price": 59999,
        }
    ])

    result = get_best_price(df, "Samsung Galaxy S24")

    assert result["seller_name"] == "MobileDeals"
    assert result["price"] == 44999