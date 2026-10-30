from typing import Any

from src.connectors.base_connector import BaseConnector


class TataCliqConnector(BaseConnector):
    """Connector for authorized Tata CLiQ product data."""

    def __init__(self):
        super().__init__("Tata CLiQ")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Tata CLiQ products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Tata CLiQ integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )