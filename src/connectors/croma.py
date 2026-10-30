from typing import Any

from src.connectors.base_connector import BaseConnector


class CromaConnector(BaseConnector):
    """Connector for authorized Croma product data."""

    def __init__(self):
        super().__init__("Croma")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Croma products through an authorized API or product feed.

        Live integration will be implemented after the required
        data access and permissions are confirmed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Croma product-data integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )