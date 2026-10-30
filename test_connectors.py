from src.connectors.coordinator import RetailerCoordinator


def test_retailer_connectors():
    coordinator = RetailerCoordinator()

    print("\n" + "=" * 50)
    print("TRUSTCART AI - CONNECTOR TEST")
    print("=" * 50)

    print(f"\nTotal connectors registered: {len(coordinator.connectors)}")

    print("\nRegistered retailers:")

    for number, connector in enumerate(coordinator.connectors, start=1):
        print(f"{number}. {connector.retailer_name}")

    print("\nTesting coordinator search...")

    results = coordinator.search_all("Samsung Galaxy S25")

    print(f"\nSearch query: {results['query']}")
    print(f"Products found: {results['total_products']}")
    print(
        f"Retailers awaiting integration: "
        f"{len(results['unavailable_retailers'])}"
    )

    print("\nConnector test completed.")
    print("=" * 50)

    assert len(coordinator.connectors) == 12
    assert len(results["unavailable_retailers"]) == 12
    assert results["total_products"] == 0

    print("\nSUCCESS: All 12 connectors are registered correctly!")


if __name__ == "__main__":
    test_retailer_connectors()