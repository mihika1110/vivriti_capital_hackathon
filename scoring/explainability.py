def generate_explanation(decision, risk_score, reasons):
    explanation = []
    explanation.append(f"Overall risk score assessed at {risk_score}.")

    if decision == "REJECT":
        explanation.append("The proposal is rejected due to elevated risk factors:")
    else:
        explanation.append("The proposal is approved with mitigated risk profile:")

    for r in reasons:
        explanation.append(f"- {r}")

    return explanation