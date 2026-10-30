from typing import Any

from src.connectors.base_connector import BaseConnector


class FlipkartConnector(BaseConnector):
    """Connector for authorized Flipkart product data."""

    def __init__(self):
        super().__init__("Flipkart")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """
        Search Flipkart products through an authorized API.

        Live API integration will be implemented after API access
        and credentials are configured.
        """
        if not query or not query.strip():
            return []

        raise NotImplementedError(
            "Flipkart API integration is not configured yet. "
            "Obtain authorized API access before searching live products."
        )