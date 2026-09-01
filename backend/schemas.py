from pydantic import BaseModel
from typing import List

class LoanApplicationRequest(BaseModel):
    business_type: str
    capital_required: float
    annual_income: float
    latitude: float
    longitude: float

class FinancialSimulationResult(BaseModel):
    is_eligible: bool
    rejection_reason: str | None = None
    scheme_category: str | None = None
    total_project_cost: float | None = None
    concessional_loan_amount: float | None = None
    beneficiary_margin_money: float | None = None
    interest_rate: float | None = None
    moratorium_months: int | None = None

class PartnerMatch(BaseModel):
    partner_id: int
    name: str
    type: str
    distance_km: float
    health_status: str

class FullApplicationResponse(BaseModel):
    simulation: FinancialSimulationResult
    recommended_partners: List[PartnerMatch]

class RawVoiceRequest(BaseModel):
    translated_text: str
    latitude: float
    longitude: float