# backend/services/nlp.py
import re
from schemas import LoanApplicationRequest


def _normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = text.replace('₹', ' rupees ')
    text = text.replace(',', '')
    text = text.replace('lac', 'lakh')
    text = text.replace('lacs', 'lakh')
    text = text.replace('lakhs', 'lakh')
    text = re.sub(r'\s+', ' ', text)
    return text


def _extract_amount(text: str) -> float:
    text = _normalize_text(text)

    for pattern, multiplier in [
        (r'(\d+(?:\.\d+)?)\s*(?:crore|cr)', 10000000),
        (r'(\d+(?:\.\d+)?)\s*(?:lakh)', 100000),
        (r'(\d+(?:\.\d+)?)\s*(?:rupees|rs|inr)', 1),
        (r'(\d+(?:\.\d+)?)', 1),
    ]:
        match = re.search(pattern, text)
        if match:
            return float(match.group(1)) * multiplier

    return 0.0


def parse_vernacular_intent(text: str, lat: float, lon: float) -> LoanApplicationRequest:
    """
    Simulates the Bhashini/IndicTrans2 pipeline parsing an intent.
    Handles Indian number format variations such as 30 lakh, 3 lac, 3000000, and rupee strings.
    """
    text = _normalize_text(text)

    capital = 0.0
    for pattern, multiplier in [
        (r'(\d+(?:\.\d+)?)\s*(?:crore|cr)', 10000000),
        (r'(\d+(?:\.\d+)?)\s*(?:lakh)', 100000),
        (r'(\d+(?:\.\d+)?)\s*(?:rupees|rs|inr)', 1),
        (r'(\d+(?:\.\d+)?)', 1),
    ]:
        match = re.search(pattern, text)
        if match:
            capital = float(match.group(1)) * multiplier
            break

    income = 0.0
    income_patterns = [
        r'(?:family|annual|yearly|income|earns|earning|salary)\s*(?:is|of)?\s*(\d+(?:\.\d+)?)\s*(?:lakh|crore|cr|rupees|rs)?',
        r'(?:earns|income is|income\s+of|family earns|earning\s+is)\s*(\d+(?:\.\d+)?)',
    ]
    for pattern in income_patterns:
        match = re.search(pattern, text)
        if match:
            candidate = _extract_amount(match.group(0))
            if candidate > 0:
                income = candidate
                break

    education_status = None
    if any(keyword in text for keyword in [
        'education', 'student', 'college', 'school', 'course', 'study',
        'tuition', 'higher education', 'degree', 'engineering', 'medical', 'university'
    ]):
        education_status = 'student'

    business_type = 'General'
    if education_status:
        business_type = 'Education'
    elif any(keyword in text for keyword in ['tailor', 'tailoring', 'sewing', 'stitching', 'garment', 'dressmaker']):
        business_type = 'Tailoring'
    elif any(keyword in text for keyword in ['farm', 'farmer', 'tractor', 'agriculture', 'cultivation', 'field']):
        business_type = 'Farming'
    elif any(keyword in text for keyword in ['weld', 'welding', 'fabrication', 'metal', 'workshop']):
        business_type = 'Welding'
    elif any(keyword in text for keyword in ['dairy', 'milk', 'cattle', 'poultry', 'cow', 'buffalo']):
        business_type = 'Dairy'

    return LoanApplicationRequest(
        business_type=business_type,
        capital_required=capital or 50000.0,
        annual_income=income or 100000.0,
        latitude=lat,
        longitude=lon,
        education_status=education_status,
    )