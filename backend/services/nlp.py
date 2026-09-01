# backend/services/nlp.py
import re
from schemas import LoanApplicationRequest

def parse_vernacular_intent(text: str, lat: float, lon: float) -> LoanApplicationRequest:
    """
    Simulates the Bhashini/IndicTrans2 pipeline parsing an intent.
    Example input: "I need 1.2 lakh rupees for a tailoring shop. My family earns 150000 a year."
    """
    text = text.lower()
    
    # 1. Extract Capital Required
    capital = 0.0
    if "lakh" in text:
        match = re.search(r'([\d\.]+)\s*lakh', text)
        if match:
            capital = float(match.group(1)) * 100000
    else:
        match = re.search(r'(?:rs|₹|rupees)?\s*(\d+[,0-9]*)', text.replace(',', ''))
        if match:
            capital = float(match.group(1))

    # 2. Extract Income
    income = 0.0
    income_match = re.search(r'(?:earns|income is)\s*(\d+[,0-9]*)', text.replace(',', ''))
    if income_match:
        income = float(income_match.group(1))
        
    # 3. Extract Business Type (Simple keyword matching for prototype)
    business_type = "General"
    if "tailor" in text or "sewing" in text:
        business_type = "Tailoring"
    elif "farm" in text or "tractor" in text:
        business_type = "Farming"
    elif "weld" in text:
        business_type = "Welding"
        
    return LoanApplicationRequest(
        business_type=business_type,
        capital_required=capital or 50000.0, # Fallback default
        annual_income=income or 100000.0,    # Fallback default
        latitude=lat,
        longitude=lon
    )