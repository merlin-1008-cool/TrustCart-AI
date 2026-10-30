from typing import Any

from src.connectors.base_connector import BaseConnector


class SnapdealConnector(BaseConnector):
    """Connector for authorized Snapdeal product data."""

    def __init__(self):
        super().__init__("Snapdeal")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Snapdeal products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Snapdeal integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )