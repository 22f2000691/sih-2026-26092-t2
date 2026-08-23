from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found — check your .env file exists and has the key set")

client = genai.Client(api_key=api_key)


def parse_user_input(text: str):
    prompt = f"""Extract these fields from the user's message as JSON only, no other text, no markdown formatting:
{{"income": <number or null>, "amount_needed": <number or null>, "category": "<SC or other, null if not mentioned>", "purpose": "<short description of what the money is for>"}}

Rules:
- "income" is annual family income in rupees (convert lakh/crore to full numbers, e.g. "3.5 lakh" = 350000)
- "amount_needed" is the project cost OR course fee they need funded, also in full rupees
- "category" should be "SC" only if explicitly mentioned, otherwise null
- "purpose" should be a short phrase describing the business/project/education purpose

User message: "{text}"

Respond with ONLY the JSON object, nothing else, no ```json fences."""

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
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"Failed to parse model output as JSON. Raw output was:\n{raw}")
        raise


if __name__ == "__main__":
    test_input = "need help getting a loan for college, my family makes about 4 lakhs a year, and I need 3.5 lakh for tuition fees. I'm from an SC background."
    result = parse_user_input(test_input)
    print(result)


