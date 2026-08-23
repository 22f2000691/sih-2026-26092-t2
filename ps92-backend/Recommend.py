from parser import parse_user_input
from Eligibility import filter_eligible_schemes


def get_recommendations(user_text: str):
    parsed = parse_user_input(user_text)

    if not parsed.get("category") or not parsed.get("income") or not parsed.get("amount_needed"):
        return {"error": "missing required info", "parsed": parsed}

    eligible = filter_eligible_schemes(
        income=parsed["income"],
        amount_needed=parsed["amount_needed"],
        category=parsed["category"],
        purpose=parsed.get("purpose", "")
    )
    return {"parsed_input": parsed, "eligible_schemes": eligible}


if __name__ == "__main__":
    result = get_recommendations("I earn 3.5 lakh a year, need 1.2 lakh for a dairy business, I'm SC category")
    print(result)