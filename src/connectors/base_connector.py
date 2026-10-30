from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    """Common interface for authorized retailer product-data sources."""

    def __init__(self, retailer_name: str):
        self.retailer_name = retailer_name

    @abstractmethod
    def search_products(self, query: str) -> list[dict[str, Any]]:
        """Search products using an authorized API or product feed."""
        raise NotImplementedError

    def normalize_product(self, product: dict[str, Any]) -> dict[str, Any]:
        """Standardize product information across retailers."""
        return {
            "retailer": self.retailer_name,
            "product_id": product.get("product_id"),
            "name": product.get("name"),
            "price": product.get("price"),
            "currency": product.get("currency", "INR"),
            "availability": product.get("availability"),
            "product_url": product.get("product_url"),
            "image_url": product.get("image_url"),
        }