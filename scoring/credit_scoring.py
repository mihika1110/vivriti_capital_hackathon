import joblib
import numpy as np

model = joblib.load("scoring/credit_model.pkl")

def compute_risk_score(pdf_data, gst_data, bank_data, site_visit):
    reasons = []

    # Feature engineering
    ebitda_margin = 0
    if pdf_data["revenue"] and pdf_data["ebitda"]:
        ebitda_margin = pdf_data["ebitda"] / pdf_data["revenue"]

    features = np.array([[
        ebitda_margin,
        gst_data["mismatch_percent"],
        int(bank_data["risk"]),
        int(pdf_data["litigation"]),
        site_visit["capacity"]
    ]])

    ml_prob = model.predict_proba(features)[0][1]  # probability of default
    ml_score = ml_prob * 100

    # Rule-based overrides (Explainable layer)
    if pdf_data["litigation"]:
        reasons.append("Litigation detected in documents")

    if gst_data["risk"]:
        reasons.append("High GST mismatch (GSTR-2A vs 3B)")

    if site_visit["capacity"] < 50:
        reasons.append("Low factory utilization observed during site visit")

    # Final score = ML + rule penalties
    rule_penalty = len(reasons) * 5
    final_score = min(100, ml_score + rule_penalty)

    decision = "APPROVE" if final_score < 40 else "REJECT"

    return {
        "risk_score": round(final_score, 2),
        "ml_probability": round(ml_prob, 2),
        "decision": decision,
        "reasons": reasons
    }