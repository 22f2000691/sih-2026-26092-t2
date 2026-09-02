try:
    from schemas import LoanApplicationRequest, FinancialSimulationResult
except ModuleNotFoundError:
    from ..schemas import LoanApplicationRequest, FinancialSimulationResult

INCOME_CEILING = 500000.0
MICROFINANCE_LIMIT = 140000.0
TERM_LOAN_LIMIT = 5000000.0
EDUCATION_LOAN_LIMIT = 2000000.0


def simulate_loan_terms(request: LoanApplicationRequest) -> FinancialSimulationResult:
    loan_type = (request.loan_type or request.business_type or "General").strip()
    if loan_type == "Education":
        request.business_type = "Education"
        request.education_status = "student"

    # Step 1: Income ceiling check for welfare-oriented concessional schemes
    if request.annual_income > INCOME_CEILING:
        return FinancialSimulationResult(
            is_eligible=False,
            rejection_reason="Annual income exceeds the ₹5.00 lakh ceiling for SC concessional schemes."
        )

    # Step 2: Match borrower intent to the appropriate scheme category
    if request.business_type == "Education" or request.education_status:
        if request.capital_required > EDUCATION_LOAN_LIMIT:
            return FinancialSimulationResult(
                is_eligible=False,
                rejection_reason="Educational loan request exceeds the supported eligibility ceiling."
            )

        scheme = "Education Loan"
        interest = 7.5
        moratorium = 6
        loan_amount = request.capital_required * 0.90
        margin_money = request.capital_required * 0.10

        return FinancialSimulationResult(
            is_eligible=True,
            scheme_category=scheme,
            total_project_cost=request.capital_required,
            concessional_loan_amount=loan_amount,
            beneficiary_margin_money=margin_money,
            interest_rate=interest,
            moratorium_months=moratorium,
        )

    if request.capital_required > TERM_LOAN_LIMIT:
        return FinancialSimulationResult(
            is_eligible=False,
            rejection_reason="Requested capital exceeds the maximum scheme limit of ₹50.00 lakh."
        )

    # Match project to the right product category
    if request.capital_required <= MICROFINANCE_LIMIT:
        scheme = "Microfinance"
        interest = 6.5
        moratorium = 3
    else:
        scheme = "Term Loan"
        interest = 8.0
        moratorium = 6

    # Step 3: Concessional amortization sim
    loan_amount = request.capital_required * 0.90
    margin_money = request.capital_required * 0.10

    return FinancialSimulationResult(
        is_eligible=True,
        scheme_category=scheme,
        total_project_cost=request.capital_required,
        concessional_loan_amount=loan_amount,
        beneficiary_margin_money=margin_money,
        interest_rate=interest,
        moratorium_months=moratorium,
    )