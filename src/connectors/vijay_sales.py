from typing import Any

from src.connectors.base_connector import BaseConnector


class VijaySalesConnector(BaseConnector):
    """Connector for authorized Vijay Sales product data."""

    def __init__(self):
        super().__init__("Vijay Sales")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Vijay Sales products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Vijay Sales integration is not configured yet. "
            "Confirm authorized product-data access first."
        )