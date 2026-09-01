from schemas import LoanApplicationRequest, FinancialSimulationResult

INCOME_CEILING = 500000.0
MICROFINANCE_LIMIT = 140000.0
TERM_LOAN_LIMIT = 5000000.0

def simulate_loan_terms(request: LoanApplicationRequest) -> FinancialSimulationResult:
    # Step 2: Rule-Based Eligibility Diagnostic[cite: 1]
    if request.annual_income > INCOME_CEILING:
        return FinancialSimulationResult(
            is_eligible=False,
            rejection_reason=f"Annual income exceeds the ₹5.00 Lakh ceiling."
        )
    
    if request.capital_required > TERM_LOAN_LIMIT:
        return FinancialSimulationResult(
            is_eligible=False,
            rejection_reason="Requested capital exceeds maximum limit of ₹50.00 Lakh."
        )

    # Match project to the right product category[cite: 1]
    if request.capital_required <= MICROFINANCE_LIMIT:
        scheme = "Microfinance"
        interest = 6.5
        moratorium = 3
    else:
        scheme = "Term Loan"
        interest = 8.0
        moratorium = 6 # Can scale up to 12 months based on specific rules[cite: 1]

    # Step 3: Concessional Amortization Simulation[cite: 1]
    loan_amount = request.capital_required * 0.90  # 90% Concessional Loan
    margin_money = request.capital_required * 0.10 # 10% Beneficiary Margin
    
    return FinancialSimulationResult(
        is_eligible=True,
        scheme_category=scheme,
        total_project_cost=request.capital_required,
        concessional_loan_amount=loan_amount,
        beneficiary_margin_money=margin_money,
        interest_rate=interest,
        moratorium_months=moratorium
    )