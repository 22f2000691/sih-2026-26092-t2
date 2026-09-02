SCHEMES = [
    {
        "id": "micro_finance",
        "name": "Micro Finance Scheme",
        "max_project_cost": 140000,
        "max_loan_amount": 125000,       # 90% of project cost
        "interest_rate": 6.5,             # beneficiary-facing rate
        "repayment_years": 3,
        "moratorium_months": 3,
        "channel_type": "SCA/PSB/RRB",
        "description": "Small-scale self-employment and micro enterprise projects for SC individuals"
    },
    {
        "id": "term_loan",
        "name": "Term Loan Scheme",
        "max_project_cost": 5000000,
        "max_loan_amount": 4500000,
        "interest_rate": 8.0,
        "repayment_years": 7,
        "moratorium_months": 6,           # 12 months for plantation/construction — handled as override below
        "channel_type": "SCA/PSB/RRB",
        "description": "Larger project financing, business expansion, manufacturing, agriculture and allied activities"
    },
    {
        "id": "education_loan",
        "name": "Educational Loan Scheme (ELS)",
        "max_project_cost": None,          # not applicable — based on course fee, not project cost
        "max_loan_amount": 4000000,        # 40 lakh or 90% of course fee, whichever is less
        "interest_rate": 6.5,
        "repayment_years": 12,             # if repayment not started; 10 years if already started
        "moratorium_months": None,         # variable: course period + 1yr (not started) OR 6 months (started)
        "channel_type": "SCA/PSB/RRB",
        "description": "Domestic and abroad higher education, professional and technical courses for SC students"
    },
    {
        "id": "aajeevika_microfinance",
        "name": "Aajeevika Microfinance Yojana (AMY)",
        "max_project_cost": 140000,
        "max_loan_amount": 125000,
        "interest_rate": 15.0,
        "repayment_years": 3,
        "moratorium_months": 3,
        "channel_type": "NBFC-MFI",
        "description": "Microfinance for SC beneficiaries, implemented through NBFC-MFIs"
    },
    {
        "id": "udyam_nidhi",
        "name": "Udyam Nidhi Yojana (UNY)",
        "max_project_cost": 500000,
        "max_loan_amount": 450000,
        "interest_rate": 13.0,
        "repayment_years": 5,
        "moratorium_months": 3,
        "channel_type": "Co-operative Society/Bank",
        "description": "Implemented through Co-operative Societies/Co-operative Banks for SC beneficiaries"
    },
]

EDUCATION_SCHEME_ID = "education_loan"