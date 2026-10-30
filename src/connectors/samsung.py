from typing import Any

from src.connectors.base_connector import BaseConnector


class SamsungConnector(BaseConnector):
    """Connector for authorized Samsung India product data."""

    def __init__(self):
        super().__init__("Samsung India")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Samsung India products through an authorized API
        or product feed.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Samsung India integration is not configured yet. "
            "Confirm authorized API or product-feed access first."
        )