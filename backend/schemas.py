from pydantic import BaseModel
from typing import List

class LoanApplicationRequest(BaseModel):
    business_type: str = "General"
    loan_type: str | None = None
    capital_required: float = 0.0
    annual_income: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    education_status: str | None = None

class ApplyRequest(BaseModel):
    input_mode: str = "text"
    language: str | None = "en"
    translated_text: str | None = None
    loan_type: str | None = None
    capital_required: float | None = None
    annual_income: float | None = None
    latitude: float = 0.0
    longitude: float = 0.0

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

class TranslationRequest(BaseModel):
    texts: dict[str, str]
    target_language: str
    source_language: str = "en"

class TranslationResponse(BaseModel):
    translations: dict[str, str]
    target_language: str

