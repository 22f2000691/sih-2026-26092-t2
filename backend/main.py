from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import LoanApplicationRequest, FinancialSimulationResult, FullApplicationResponse, RawVoiceRequest
from services.simulator import simulate_loan_terms
from services.router import find_optimal_partners
from services.nlp import parse_vernacular_intent

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIH Health-Aware Router API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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

@app.post("/voice-apply", response_model=FullApplicationResponse)
def process_voice_application(request: RawVoiceRequest, db: Session = Depends(get_db)):
    # 1. Convert raw text to structured JSON
    structured_data = parse_vernacular_intent(
        request.translated_text, 
        request.latitude, 
        request.longitude
    )
    
    # 2. Run simulation
    sim_result = simulate_loan_terms(structured_data)
    
    # 3. Route to partners
    partners = []
    if sim_result.is_eligible:
        partners = find_optimal_partners(db, structured_data)
        
    return FullApplicationResponse(
        simulation=sim_result,
        recommended_partners=partners
    )