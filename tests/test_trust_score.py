import sys
from pathlib import Path

# Allow Python to find the src module
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.trust_score import calculate_trust_score, classify_trust_level


def test_trust_score_is_between_0_and_100():
    seller = {
        "rating": 4.5,
        "reviews_count": 1250,
        "return_policy": "Yes",
        "warranty_available": "Yes",
        "verified_seller": "Yes",
        "complaint_count": 5,
    }

    score = calculate_trust_score(seller)

    assert 0 <= score <= 100


def test_high_trust_indicators():
    seller = {
        "rating": 4.5,
        "reviews_count": 1250,
        "return_policy": "Yes",
        "warranty_available": "Yes",
        "verified_seller": "Yes",
        "complaint_count": 5,
    }

    score = calculate_trust_score(seller)

    assert score == 97.5
    assert classify_trust_level(score) == "High Trust Indicators"


def test_low_trust_indicators():
    seller = {
        "rating": 2.0,
        "reviews_count": 10,
        "return_policy": "No",
        "warranty_available": "No",
        "verified_seller": "No",
        "complaint_count": 25,
    }

    score = calculate_trust_score(seller)

    assert score == 10.0
    assert classify_trust_level(score) == "Needs Further Verification"