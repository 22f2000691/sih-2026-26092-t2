from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found — check your .env file exists and has the key set")

client = genai.Client(api_key=api_key)


def explain_recommendation(eligible_schemes, language="English"):
    if not eligible_schemes:
        return []
 
    # Build a numbered summary of all schemes to send in ONE request
    scheme_list_text = "\n".join(
        f"{i+1}. id={s['id']}, name={s['name']}, max_loan={s['max_loan_amount']}, "
        f"interest_rate={s['interest_rate']}%, repayment_years={s['repayment_years']}, "
        f"channel_type={s['channel_type']}"
        for i, s in enumerate(eligible_schemes)
    )
 
    prompt = f"""Below is a list of {len(eligible_schemes)} loan schemes. For EACH one,
write ONE short, warm sentence (max 25 words) in {language} explaining why it suits
someone, in plain conversational language, no jargon, no markdown, no formatting symbols.
 
Schemes:
{scheme_list_text}
 
Respond with ONLY a JSON array, one object per scheme, in the same order as listed,
in this exact shape, no other text, no markdown fences:
[{{"id": "<scheme id>", "blurb": "<your sentence>"}}, ...]"""
 
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    raw = response.text.strip()
 
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
 
    try:
        blurbs = json.loads(raw)
    except json.JSONDecodeError:
        print(f"Failed to parse blurb JSON. Raw output was:\n{raw}")
        # fallback: return schemes without blurbs rather than crashing entirely
        blurbs = [{"id": s["id"], "blurb": ""} for s in eligible_schemes]
 
    blurb_map = {b["id"]: b["blurb"] for b in blurbs}
 
    results = []
    for scheme in eligible_schemes:
        results.append({
            "scheme_id": scheme["id"],
            "scheme_name": scheme["name"],
            "max_loan_amount": scheme["max_loan_amount"],
            "interest_rate": scheme["interest_rate"],
            "repayment_years": scheme["repayment_years"],
            "channel_type": scheme["channel_type"],
            "blurb": blurb_map.get(scheme["id"], "")
        })
    return results


if __name__ == "__main__":
    from Recommend import get_recommendations

    result = get_recommendations("I earn 3.5 lakh a year, need 1.2 lakh for a dairy business, I'm SC category")
    explanation = explain_recommendation(result["eligible_schemes"], language="Hindi")
    print(explanation)