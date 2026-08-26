# Stock Market Analyzer

Root-level full-stack project split into:

- `backend/` - FastAPI APIs, SQLite cache, market data services and local Ollama integration.
- `frontend/` - React/Vite dashboard.

Phase 1 uses only free local/open-source resources:

- Market data: `yfinance`
- Database: SQLite for local development
- Deployment database target: PostgreSQL
- LLM provider: local Ollama models

Phase 2 adds explainable analysis:

- Company profile and available fundamental metrics
- Technical indicators: SMA, EMA, RSI, MACD and Bollinger Bands
- Risk metrics: 30-day volatility, max drawdown and average volume
- RSS headline sentiment using VADER
- Transparent BUY/HOLD/SELL scoring with an educational disclaimer

## Run Locally

Start the backend:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

Useful backend endpoints:

- `GET /api/health`
- `GET /api/stocks/{symbol}/quote`
- `GET /api/stocks/{symbol}/history`
- `GET /api/stocks/{symbol}/analysis`
- `GET /api/llm/status`
- `POST /api/llm/suggest`
