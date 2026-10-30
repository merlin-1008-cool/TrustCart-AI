from typing import Any

from src.connectors.base_connector import BaseConnector


class AmazonConnector(BaseConnector):
    """Connector for authorized Amazon India product data."""

    def __init__(self):
        super().__init__("Amazon India")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Amazon India products through an authorized API.

        Live API integration will be implemented after API access
        and credentials are configured.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Amazon API integration is not configured yet. "
            "Obtain authorized API access before searching live products."
        )