from pydantic import AliasChoices, BaseModel, Field
from typing import List

class LoanApplicationRequest(BaseModel):
    business_type: str = "General"
    loan_type: str | None = None
    capital_required: float = 0.0
    annual_income: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    education_status: str | None = None
    preferred_language: str = "en"

class ApplyRequest(BaseModel):
    input_mode: str = "text"
    translated_text: str | None = None
    loan_type: str | None = None
    capital_required: float | None = None
    annual_income: float | None = None
    latitude: float = 0.0
    longitude: float = 0.0
    preferred_language: str = Field("en", validation_alias=AliasChoices("preferred_language", "language"))

class FinancialSimulationResult(BaseModel):
    is_eligible: bool
    rejection_reason: str | None = None
    missing_fields: List[str] = []
    clarification_prompt: str | None = None
    scheme_category: str | None = None
    scheme_name: str | None = None
    match_reasons: List[str] = []
    total_project_cost: float | None = None
    concessional_loan_amount: float | None = None
    beneficiary_margin_money: float | None = None
    interest_rate: float | None = None
    moratorium_months: int | None = None
    repayment_tenure_months: int | None = None
    estimated_emi: float | None = None
    total_payable: float | None = None

class PartnerMatch(BaseModel):
    partner_id: int
    name: str
    type: str
    distance_km: float
    health_status: str
    remaining_capacity: float
    supported_schemes: List[str]
    latitude: float
    longitude: float

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
