from Scheme_Data import SCHEMES, EDUCATION_SCHEME_ID

INCOME_CAP = 500000  # ₹5.00 lakh, applies to all schemes
LOAN_FUNDING_PERCENT = 0.90  # NSFDC funds up to 90% of project cost / course fee


def filter_eligible_schemes(income: float, amount_needed: float, category: str, purpose: str = ""):
    """
    income: annual family income
    amount_needed: project cost (for business/general schemes) OR course fee (for education)
    category: must be 'SC' for any scheme to apply
    purpose: free-text purpose, used only to route education vs general schemes

    Returns each eligible scheme as a copy with an added "quoted_loan_amount" field:
    the actual loan amount this specific user would be quoted (90% of what they
    asked for, capped at the scheme's max loan limit) — NOT just the scheme's
    flat maximum, which is only correct when the user asks for the max project cost.
    """
    if category.upper() != "SC":
        return []

    if income > INCOME_CAP:
        return []

    is_education = "education" in purpose.lower() or "course" in purpose.lower() or "study" in purpose.lower()

    eligible = []
    for scheme in SCHEMES:
        if scheme["id"] == EDUCATION_SCHEME_ID:
            if is_education and amount_needed <= scheme["max_loan_amount"]:
                quoted = round(min(amount_needed * LOAN_FUNDING_PERCENT, scheme["max_loan_amount"]), 2)
                eligible.append({**scheme, "quoted_loan_amount": quoted})
            continue

        if is_education:
            continue

        if scheme["max_project_cost"] is not None and amount_needed <= scheme["max_project_cost"]:
            quoted = round(min(amount_needed * LOAN_FUNDING_PERCENT, scheme["max_loan_amount"]), 2)
            eligible.append({**scheme, "quoted_loan_amount": quoted})

    return eligible