from typing import Any

from src.connectors.base_connector import BaseConnector


class MeeshoConnector(BaseConnector):
    """Connector for authorized Meesho product data."""

    def __init__(self):
        super().__init__("Meesho")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Meesho products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Meesho integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )