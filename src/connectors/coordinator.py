from typing import Any

from src.connectors.amazon import AmazonConnector
from src.connectors.flipkart import FlipkartConnector
from src.connectors.croma import CromaConnector
from src.connectors.reliance_digital import RelianceDigitalConnector
from src.connectors.vijay_sales import VijaySalesConnector
from src.connectors.tata_cliq import TataCliqConnector
from src.connectors.tata_neu import TataNeuConnector
from src.connectors.jiomart import JioMartConnector
from src.connectors.snapdeal import SnapdealConnector
from src.connectors.meesho import MeeshoConnector
from src.connectors.samsung import SamsungConnector
from src.connectors.myntra import MyntraConnector


class RetailerCoordinator:
    """Coordinate product searches across all configured retailers."""

    def __init__(self):
        self.connectors = [
            AmazonConnector(),
            FlipkartConnector(),
            CromaConnector(),
            RelianceDigitalConnector(),
            VijaySalesConnector(),
            TataCliqConnector(),
            TataNeuConnector(),
            JioMartConnector(),
            SnapdealConnector(),
            MeeshoConnector(),
            SamsungConnector(),
            MyntraConnector(),
        ]

    def search_all(self, query: str) -> dict[str, Any]:
        """Search all connectors and collect available results."""

        if not query or not query.strip():
            raise ValueError("Please provide a product search query.")

        results = []
        unavailable_retailers = []

        for connector in self.connectors:
            try:
                products = connector.search_products(query.strip())
                results.extend(products)

            except NotImplementedError:
                unavailable_retailers.append(connector.retailer_name)

        return {
            "query": query.strip(),
            "total_products": len(results),
            "products": results,
            "unavailable_retailers": unavailable_retailers,
        }