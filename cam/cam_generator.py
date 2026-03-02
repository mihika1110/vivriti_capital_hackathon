from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_cam(output_path, company_name, scoring_result):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Credit Appraisal Memo (CAM)")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 90, f"Company: {company_name}")
    c.drawString(50, height - 120, f"Decision: {scoring_result['decision']}")
    c.drawString(50, height - 150, f"Risk Score: {scoring_result['risk_score']}")

    y = height - 190
    c.drawString(50, y, "Key Risk Factors:")
    y -= 20

    for reason in scoring_result["reasons"]:
        c.drawString(70, y, f"- {reason}")
        y -= 20

    c.save()