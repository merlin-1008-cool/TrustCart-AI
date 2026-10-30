from typing import Any

from src.connectors.base_connector import BaseConnector


class JioMartConnector(BaseConnector):
    """Connector for authorized JioMart product data."""

    def __init__(self):
        super().__init__("JioMart")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search JioMart products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "JioMart integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )