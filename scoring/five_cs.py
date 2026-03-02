def compute_five_cs(pdf, gst, bank, site, research):
    return {
        "Character": {
            "score": 60 if pdf["litigation"] else 80,
            "comment": "Litigation risk observed" if pdf["litigation"] else "No adverse legal history"
        },
        "Capacity": {
            "score": 50 if site["capacity"] < 50 else 75,
            "comment": "Low utilization impacts repayment capacity"
        },
        "Capital": {
            "score": 70,
            "comment": "Adequate capital structure"
        },
        "Collateral": {
            "score": 65,
            "comment": "Moderate asset coverage"
        },
        "Conditions": {
            "score": 60 if research["risk_score"] > 0 else 80,
            "comment": "Sector/regulatory headwinds detected"
        }
    }