from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import os

from ingestion.pdf_parser import extract_from_pdf
from ingestion.structured_parser import gst_mismatch, bank_vs_gst
from scoring.credit_scoring import compute_risk_score
from scoring.five_cs import compute_five_cs
from scoring.pricing import recommend_terms
from cam.cam_generator import generate_cam
from research.news_agent import analyze_news

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()


@app.post("/process")
async def process(
    request: Request,
    company_name: str = Form(...),
    capacity: int = Form(...),
    notes: str = Form(""),
    pdf: UploadFile = Form(...)
):
    os.makedirs("uploads", exist_ok=True)

    pdf_path = f"uploads/{pdf.filename}"
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(pdf.file, f)

    # --- DATA INGESTION ---
    pdf_data = extract_from_pdf(pdf_path)
    gst_data = gst_mismatch("data/gst_3b.csv", "data/gst_2a.csv")
    bank_data = bank_vs_gst("data/bank_statement.csv", gst_data["gst_3b"])

    # --- RESEARCH AGENT ---
    research_data = analyze_news(company_name)

    # --- SITE VISIT INPUT ---
    site_visit = {
        "capacity": capacity,
        "notes": notes
    }

    # --- SCORING ---
    scoring = compute_risk_score(pdf_data, gst_data, bank_data, site_visit)

    # Human-in-the-loop logic
    if "delay" in notes.lower() or "concern" in notes.lower():
        scoring["risk_score"] += 5
        scoring["reasons"].append("Negative observations from site visit notes")

    # --- FIVE Cs ---
    five_cs = compute_five_cs(pdf_data, gst_data, bank_data, site_visit, research_data)

    # --- PRICING ---
    pricing = recommend_terms(pdf_data.get("revenue"), scoring["risk_score"])

    # --- CAM GENERATION ---
    cam_path = f"uploads/{company_name}_CAM.pdf"
    generate_cam(cam_path, company_name, scoring)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "score": scoring["risk_score"],
            "ml_prob": scoring["ml_probability"],
            "decision": scoring["decision"],
            "reasons": scoring["reasons"],
            "five_cs": five_cs,
            "limit": pricing["limit"],
            "rate": pricing["interest_rate"],
            "cam_path": "/" + cam_path
        }
    )