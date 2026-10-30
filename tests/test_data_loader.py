from src.data_loader import load_seller_data


def test_load_seller_data():
    df = load_seller_data()
    assert not df.empty
    assert df.shape == (12, 12)
    assert "product_name" in df.columns
    assert "seller_name" in df.columns
    assert "price" in df.columns