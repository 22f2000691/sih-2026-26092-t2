import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import LoanApplicationRequest, FinancialSimulationResult, FullApplicationResponse, RawVoiceRequest, ApplyRequest
from services.simulator import simulate_loan_terms
from services.router import find_optimal_partners
from services.nlp import parse_vernacular_intent

cors_origins = [
    origin.strip() for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",") if origin.strip()
]

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIH Health-Aware Router API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "operational", "service": "health-aware-router"}

@app.get("/partners/count")
def get_partners_count(db: Session = Depends(get_db)):
    count = db.query(models.ChannelPartner).count()
    return {"total_registered_partners": count}


@app.post("/simulate", response_model=FinancialSimulationResult)
def run_financial_simulation(application: LoanApplicationRequest):
    return simulate_loan_terms(application)

@app.post("/process-application", response_model=FullApplicationResponse)
def process_full_application(application: LoanApplicationRequest, db: Session = Depends(get_db)):
    # 1. Run the financial simulation[cite: 1]
    sim_result = simulate_loan_terms(application)
    
    # 2. Find the optimal channel partners[cite: 1]
    partners = []
    if sim_result.is_eligible:
        partners = find_optimal_partners(db, application)
        
    return FullApplicationResponse(
        simulation=sim_result,
        recommended_partners=partners
    )

@app.post("/apply", response_model=FullApplicationResponse)
def process_apply(request: ApplyRequest, db: Session = Depends(get_db)):
    if request.input_mode == "form":
        structured_data = LoanApplicationRequest(
            business_type=request.loan_type or "General",
            loan_type=request.loan_type,
            capital_required=request.capital_required or 0.0,
            annual_income=request.annual_income or 0.0,
            latitude=request.latitude,
            longitude=request.longitude,
            education_status="student" if (request.loan_type or "").lower() == "education" else None,
        )
    else:
        structured_data = parse_vernacular_intent(
            request.translated_text or "",
            request.latitude,
            request.longitude,
        )
        if request.loan_type:
            structured_data.loan_type = request.loan_type
            structured_data.business_type = request.loan_type
            if request.loan_type.lower() == "education":
                structured_data.education_status = "student"

    sim_result = simulate_loan_terms(structured_data)
    partners = []
    if sim_result.is_eligible:
        partners = find_optimal_partners(db, structured_data)

    return FullApplicationResponse(
        simulation=sim_result,
        recommended_partners=partners
    )


@app.post("/voice-apply", response_model=FullApplicationResponse)
def process_voice_application(request: RawVoiceRequest, db: Session = Depends(get_db)):
    apply_request = ApplyRequest(
        input_mode="voice",
        translated_text=request.translated_text,
        latitude=request.latitude,
        longitude=request.longitude,
    )
    return process_apply(apply_request, db)
