"""
Core Marketing Analytics KPI Formulas
Meta Ads Campaign Performance Analysis

Formulas implemented:
- CTR (Click-Through Rate): (Clicks / Impressions) * 100
- CPC (Cost Per Click): Spend / Clicks
- CPM (Cost Per Mille): (Spend / Impressions) * 1000
- Conversion Rate (CR): (Conversions / Clicks) * 100
- CPA (Cost Per Acquisition): Spend / Conversions
- ROAS (Return On Ad Spend): Revenue / Spend
"""

def calculate_ctr(clicks: int | float, impressions: int | float) -> float:
    """Calculate Click-Through Rate as a percentage."""
    if impressions == 0 or impressions is None:
        return 0.0
    return round((clicks / impressions) * 100, 2)

def calculate_cpc(spend: float, clicks: int | float) -> float:
    """Calculate Cost Per Click in currency units."""
    if clicks == 0 or clicks is None:
        return 0.0
    return round(spend / clicks, 2)

def calculate_cpm(spend: float, impressions: int | float) -> float:
    """Calculate Cost Per Thousand Impressions (CPM)."""
    if impressions == 0 or impressions is None:
        return 0.0
    return round((spend / impressions) * 1000, 2)

def calculate_conversion_rate(conversions: int | float, clicks: int | float) -> float:
    """Calculate Conversion Rate as a percentage."""
    if clicks == 0 or clicks is None:
        return 0.0
    return round((conversions / clicks) * 100, 2)

def calculate_cpa(spend: float, conversions: int | float) -> float:
    """Calculate Cost Per Acquisition / Conversion."""
    if conversions == 0 or conversions is None:
        return 0.0
    return round(spend / conversions, 2)

def calculate_roas(revenue: float, spend: float) -> float:
    """Calculate Return On Advertising Spend (ROAS)."""
    if spend == 0 or spend is None:
        return 0.0
    return round(revenue / spend, 2)
