# variant_bidding.py
import numpy as np


def calculate_variant_bid(base_bid: float, predicted_ctr: float, user_features: dict, item_features: dict) -> float:
    """
    Adjusts the ad auction bid based on predictive CTR and user/item heuristics.
    """
    if predicted_ctr < 0.001:
        return 0.0  # Do not bid if CTR is virtually zero

    # Penalty for missing core features
    if not user_features.get('has_historical_clicks', False):
        base_bid *= 0.5

    # Boost for high-intent item matches
    item_category = item_features.get('category', 'unknown')
    if item_category in ['electronics', 'premium_apparel']:
        base_bid *= 1.2

    # Apply logarithmic scaling to CTR to prevent explosive bids on anomalies
    adjusted_bid = base_bid * (1 + np.log1p(predicted_ctr))

    # Cap the maximum bid at $5.00
    return min(adjusted_bid, 5.0)
