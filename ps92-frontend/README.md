# ps92-frontend

AI-powered frontend for matching SC beneficiaries with NSFDC concessional loan schemes.

## Quick start

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Mock vs live API

All API calls go through `src/api.js`. During development, mock data is used by default.

**To switch to the live backend:**

1. Open `src/api.js`
2. Set `USE_MOCK = false`
3. Ensure FastAPI is running at `http://localhost:8000`

## Testing different response states (mock mode)

Type keywords in the input textarea:

| Keyword in input | Result |
|------------------|--------|
| *(default)* | Success with 4 schemes |
| `incomplete` or `missing` | Incomplete input state |
| `no match` or `no scheme` | No match state |
| `error` or `fail` | Error state |

Or change `MOCK_SCENARIO` in `src/data/mockData.js`.

## Project structure

```
src/
├── api.js                 # Isolated fetch — toggle USE_MOCK here
├── data/mockData.js       # Hardcoded mock responses
├── i18n/strings.js        # English + Hindi UI strings
├── utils/formatters.js    # Currency, labels, summaries
└── components/
    ├── LandingScreen.jsx
    ├── LoadingScreen.jsx
    ├── SuccessResults.jsx
    ├── SchemeCard.jsx
    ├── IncompleteResults.jsx
    ├── NoMatchResults.jsx
    ├── ErrorScreen.jsx
    └── LanguageSelector.jsx
```

## Tech stack

- React 19 + Vite
- Tailwind CSS v4
