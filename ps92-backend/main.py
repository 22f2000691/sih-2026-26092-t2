from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from parser import parse_user_input
from Eligibility import filter_eligible_schemes
from explain import explain_recommendation
from emi_calculator import calculate_emi

app = FastAPI(title="PS92 Scheme Recommender API")

# Allow frontend (running on a different port during dev) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your actual frontend URL before final submission
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendRequest(BaseModel):
    text: str
    language: str = "English"


class EMIRequest(BaseModel):
    principal: float
    annual_interest_rate: float
    tenure_years: int
    moratorium_months: int = 0


@app.get("/")
def root():
    return {"status": "PS92 backend is running"}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    try:
        parsed = parse_user_input(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse input: {str(e)}")

    missing = [f for f in ["income", "amount_needed", "category"] if not parsed.get(f)]
    if missing:
        return {
            "status": "incomplete",
            "missing_fields": missing,
            "parsed_input": parsed,
            "message": "Some required details are missing. Please provide: " + ", ".join(missing)
        }

    eligible = filter_eligible_schemes(
        income=parsed["income"],
        amount_needed=parsed["amount_needed"],
        category=parsed["category"],
        purpose=parsed.get("purpose", "")
    )

    if not eligible:
        return {
            "status": "no_match",
            "parsed_input": parsed,
            "message": "No matching schemes were found for the details provided."
        }

    try:
        explained = explain_recommendation(eligible, language=req.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate explanations: {str(e)}")

    return {
        "status": "success",
        "parsed_input": parsed,
        "recommendations": explained
    }


@app.post("/calculate-emi")
def calculate_emi_endpoint(req: EMIRequest):
    try:
        result = calculate_emi(
            principal=req.principal,
            annual_interest_rate=req.annual_interest_rate,
            tenure_years=req.tenure_years,
            moratorium_months=req.moratorium_months
        )
        return {"status": "success", **result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)