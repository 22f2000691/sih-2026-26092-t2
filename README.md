# Scheme Matchmaker — SIH 26092

An explainable prototype for matching eligible applicants to concessional
enterprise or education schemes, estimating repayments, and routing them to
healthy channel partners.

## Run locally

Backend requires PostgreSQL with PostGIS enabled and the values in
`backend/database.py` replaced by your local `DATABASE_URL`.

```bash
cd backend
pip install -r requirements.txt
python migrate.py  # only when upgrading an existing database
python seed_db.py
uvicorn main:app --reload
```

```bash
cd frontend
npm install
VITE_API_URL=http://localhost:8000 npm run dev
```

## Important demo-data note

Scheme policies and partner records are clearly labelled demo data. Before a
real deployment, replace them with approved Ministry/National SC Finance and
Development Corporation circulars and authorized partner feeds. The prototype
does not submit a real loan application.

## Optional BHASHINI gateway

The API keeps BHASHINI credentials on the backend. Set `BHASHINI_GATEWAY_URL`
and `BHASHINI_API_KEY` to a small server-side gateway for your provisioned
BHASHINI translation/ASR pipeline. The gateway accepts `{text,
source_language, target_language}` and returns `{translated_text}`. If these
are absent or the provider is unavailable, Hindi/English rule parsing remains
available for the demo.
