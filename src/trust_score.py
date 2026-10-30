def calculate_trust_score(seller):
    """
    Calculate a prototype seller trust score out of 100.

    This is a preliminary scoring model for development,
    not a validated measure of real-world seller trust.
    """

    score = 0

    # 1. Seller rating: 25 points
    rating = float(seller["rating"])
    score += (rating / 5) * 25

    # 2. Customer review count: 15 points
    reviews = int(seller["reviews_count"])

    if reviews >= 1000:
        score += 15
    elif reviews >= 500:
        score += 12
    elif reviews >= 100:
        score += 9
    elif reviews >= 20:
        score += 5

    # 3. Return policy: 15 points
    if str(seller["return_policy"]).strip().lower() == "yes":
        score += 15

    # 4. Warranty availability: 15 points
    if str(seller["warranty_available"]).strip().lower() == "yes":
        score += 15

    # 5. Verified seller: 20 points
    if str(seller["verified_seller"]).strip().lower() == "yes":
        score += 20

    # 6. Customer complaints: 10 points
    complaints = int(seller["complaint_count"])

    if complaints <= 5:
        score += 10
    elif complaints <= 10:
        score += 7
    elif complaints <= 20:
        score += 4

    return round(max(0, min(100, score)), 2)


def classify_trust_level(score):
    """Classify the prototype score into an understandable category."""

    if score >= 80:
        return "High Trust Indicators"
    elif score >= 60:
        return "Moderate Trust Indicators"
    else:
        return "Needs Further Verification"