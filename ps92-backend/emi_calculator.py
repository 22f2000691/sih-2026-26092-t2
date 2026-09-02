def calculate_emi(principal: float, annual_interest_rate: float, tenure_years: int, moratorium_months: int = 0):
    """
    Standard EMI formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    where r = monthly interest rate, n = number of monthly installments.

    principal: loan amount in rupees
    annual_interest_rate: e.g. 6.5 for 6.5%
    tenure_years: repayment period in years
    moratorium_months: months before EMI payments begin (informational only,
                        doesn't change the EMI amount itself, just when it starts)
    """
    if principal <= 0 or tenure_years <= 0:
        raise ValueError("principal and tenure_years must be positive")

    monthly_rate = (annual_interest_rate / 100) / 12
    num_months = tenure_years * 12

    if monthly_rate == 0:
        emi = principal / num_months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** num_months / \
              ((1 + monthly_rate) ** num_months - 1)

    total_payment = emi * num_months
    total_interest = total_payment - principal

    return {
        "monthly_emi": round(emi, 2),
        "total_months": num_months,
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "moratorium_months": moratorium_months,
        "note": f"First EMI due after {moratorium_months} month moratorium period" if moratorium_months else None
    }


if __name__ == "__main__":
    # test with Micro Finance Scheme figures
    result = calculate_emi(principal=125000, annual_interest_rate=6.5, tenure_years=3, moratorium_months=3)
    print(result)