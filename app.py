from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from ingestion.pdf_parser import extract_from_pdf
from ingestion.structured_parser import gst_mismatch, bank_vs_gst
from scoring.credit_scoring import compute_risk_score
from cam.cam_generator import generate_cam

import shutil
import os

app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="templates"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/process")
async def process(
    request: Request,
    company_name: str = Form(...),
    capacity: int = Form(...),
    pdf: UploadFile = Form(...)
):
    os.makedirs("uploads", exist_ok=True)
    pdf_path = f"uploads/{pdf.filename}"

    # Save uploaded PDF
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(pdf.file, f)

    # Extract PDF data
    pdf_data = extract_from_pdf(pdf_path)

    # Structured data checks
    gst_data = gst_mismatch("data/gst_3b.csv", "data/gst_2a.csv")
    bank_data = bank_vs_gst("data/bank_statement.csv", gst_data["gst_3b"])

    site_visit = {"capacity": capacity}

    # Compute scoring
    scoring = compute_risk_score(pdf_data, gst_data, bank_data, site_visit)

    # Generate CAM
    cam_path = f"uploads/{company_name}_CAM.pdf"
    generate_cam(cam_path, company_name, scoring)

    # Return result page
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "score": scoring["risk_score"],
            "ml_prob": scoring["ml_probability"],
            "decision": scoring["decision"],
            "reasons": scoring["reasons"],
            "cam_path": "/" + cam_path
        }
    )