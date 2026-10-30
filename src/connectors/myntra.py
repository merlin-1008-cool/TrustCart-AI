from typing import Any

from src.connectors.base_connector import BaseConnector


class MyntraConnector(BaseConnector):
    """Connector for authorized Myntra product data."""

    def __init__(self):
        super().__init__("Myntra")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Myntra products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Myntra integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )