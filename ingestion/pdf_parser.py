import pdfplumber
import re

def extract_from_pdf(pdf_path):
    extracted = {
        "revenue": None,
        "ebitda": None,
        "debt": None,
        "litigation": False
    }

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text=text+page.extract_text() or ""

    revenue_match=re.search(r"Revenue.*?₹?([\d,.]+)", text, re.IGNORECASE)
    ebitda_match=re.search(r"EBITDA.*?₹?([\d,.]+)", text, re.IGNORECASE)
    debt_match=re.search(r"Debt.*?₹?([\d,.]+)", text, re.IGNORECASE)

    if revenue_match:
        extracted["revenue"]=float(revenue_match.group(1).replace(",", ""))
    if ebitda_match:
        extracted["ebitda"]=float(ebitda_match.group(1).replace(",", ""))
    if debt_match:
        extracted["debt"]=float(debt_match.group(1).replace(",", ""))

    if "litigation" in text.lower() or "court" in text.lower():
        extracted["litigation"]=True

    return extracted