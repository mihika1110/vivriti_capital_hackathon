from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_cam(output_path, company_name, scoring):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "CREDIT APPRAISAL MEMORANDUM (CAM)")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Borrower Name: {company_name}")
    y -= 20
    c.drawString(50, y, f"Final Decision: {scoring['decision']}")
    y -= 20
    c.drawString(50, y, f"Overall Risk Score: {scoring['risk_score']}/100")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "1. Executive Summary")
    y -= 20

    c.setFont("Helvetica", 11)
    summary = (
        f"The credit proposal for {company_name} has been evaluated using the "
        "Intelli-Credit AI Decisioning Engine. The assessment integrates financial "
        "performance, statutory data, unstructured disclosures, secondary research, "
        "and qualitative site visit observations."
    )
    c.drawString(50, y, summary)
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "2. Key Risk Drivers")
    y -= 20

    c.setFont("Helvetica", 11)
    for reason in scoring["reasons"]:
        c.drawString(60, y, f"- {reason}")
        y=y-15

    y=y-20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "3. AI-Based Recommendation Rationale")
    y=y-20

    c.setFont("Helvetica", 11)
    rationale = (
        "The recommendation has been generated using an explainable hybrid model "
        "combining machine learning predictions with rule-based credit heuristics. "
        "Human qualitative inputs from site visits have been incorporated to adjust "
        "the final risk assessment."
    )
    c.drawString(50, y, rationale)
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "4. Conclusion")
    y -= 20

    c.setFont("Helvetica", 11)
    conclusion = (
        "Based on the above analysis, the proposal has been evaluated in line with "
        "prudent credit risk management practices. The recommendation reflects both "
        "quantitative risk indicators and qualitative business insights."
    )
    c.drawString(50, y, conclusion)

    c.save()