from typing import Any

from src.connectors.base_connector import BaseConnector


class TataNeuConnector(BaseConnector):
    """Connector for authorized Tata Neu product data."""

    def __init__(self):
        super().__init__("Tata Neu")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Tata Neu products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Tata Neu integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )