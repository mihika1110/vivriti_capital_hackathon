def recommend_terms(revenue, risk_score):
    base_limit=revenue*0.3 if revenue else 10_000_000

    risk_factor=max(0.4, (100-risk_score)/100)
    final_limit=base_limit*risk_factor

    base_rate=10.5
    risk_premium=risk_score/20

    return {
        "limit": round(final_limit, 2),
        "interest_rate": round(base_rate+risk_premium, 2)
    }