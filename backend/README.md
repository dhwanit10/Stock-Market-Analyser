# Backend

FastAPI service for the Stock Market Analyzer.

## Local Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000` and exposes docs at `http://localhost:8000/docs`.

SQLite is used for phase 1 local caching. PostgreSQL is the planned deployment database.

## Phase 2 Analysis

`GET /api/stocks/{symbol}/analysis` returns:

- Company profile and available fundamental metrics
- SMA, EMA, RSI, MACD and Bollinger Bands
- 30-day volatility, max drawdown and average volume
- RSS headline sentiment scored with VADER
- Transparent score components and a BUY/HOLD/SELL signal

## Gemini summaries

Set `GEMINI_API_KEY` and `GEMINI_MODEL` in `backend/.env`. The API key is read only
by the backend and is never sent to the frontend.
