"""Small, auditable scheme catalogue used by the recommender.

Replace these seeded demo values with the latest official circulars before a
production launch.  Keeping policy values in one place makes that review easy.
"""

SCHEMES = {
    "Microfinance": {
        "name": "Micro Finance Scheme",
        "max_project_cost": 140000.0,
        "interest_rate": 6.5,
        "moratorium_months": 3,
        "tenure_months": 36,
        "category": "enterprise",
    },
    "Term Loan": {
        "name": "Term Loan Scheme",
        "max_project_cost": 5000000.0,
        "interest_rate": 8.0,
        "moratorium_months": 6,
        "tenure_months": 60,
        "category": "enterprise",
    },
    "Education Loan": {
        "name": "Educational Loan Scheme",
        "max_project_cost": 2000000.0,
        "interest_rate": 7.5,
        "moratorium_months": 6,
        "tenure_months": 84,
        "category": "education",
    },
}

INCOME_CEILING = 500000.0
BENEFICIARY_CONTRIBUTION = 0.10
