from typing import Any

from src.connectors.base_connector import BaseConnector


class RelianceDigitalConnector(BaseConnector):
    """Connector for authorized Reliance Digital product data."""

    def __init__(self):
        super().__init__("Reliance Digital")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Reliance Digital products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Reliance Digital integration is not configured yet. "
            "Confirm authorized product-data access first."
        )