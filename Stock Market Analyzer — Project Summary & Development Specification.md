# Stock Market Analyzer
### Python for Data Science Project

## 1. Project Overview

**Stock Market Analyzer** is a data-driven web application that allows users to search for a publicly listed company and receive a complete analysis of its stock.

The system will collect real-time and historical market data through APIs, analyze the company's fundamentals and stock performance, calculate technical indicators, evaluate risk, perform sentiment analysis on recent news, and use machine-learning models to estimate future price trends.

An LLM will be used as an intelligent explanation layer to convert complex financial data into simple, understandable insights.

The application will ultimately generate an **explainable investment signal** such as:

- 🟢 Strong Buy
- 🟢 Buy
- 🟡 Hold
- 🔴 Sell
- 🔴 Strong Sell

The system will not simply provide a recommendation. It will explain **why** the signal was generated using measurable financial and technical factors.

---

# 2. Main Objective

The main objective is to build an interactive Data Science application that combines:

- Data collection
- Data cleaning
- Exploratory Data Analysis
- Financial analysis
- Technical analysis
- Statistical analysis
- Machine Learning
- Natural Language Processing
- Sentiment analysis
- LLM-based explanation
- Data visualization

The project should demonstrate that Python can be used to collect, process, analyze, visualize and interpret large amounts of financial data.

---

# 3. Overall User Flow

The application will follow this workflow:

```text
                    USER
                      │
                      ▼
              Search Stock
                      │
                      ▼
             Select Company
                      │
                      ▼
          Fetch Data from APIs
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
  Fundamental      Technical        News
   Analysis        Analysis       Analysis
       │              │              │
       ▼              ▼              ▼
 Financial        Indicators      Sentiment
 Metrics          & Trends        Analysis
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                Risk Analysis
                      │
                      ▼
              ML Price Prediction
                      │
                      ▼
             Scoring Engine
                      │
                      ▼
              Investment Signal
                      │
                      ▼
               LLM Explanation
                      │
                      ▼
             Complete Dashboard
```

---

# 4. Application Structure

The application should have the following major sections:

### 1. Dashboard / Overview
### 2. Fundamental Analysis
### 3. Technical Analysis
### 4. Prediction & Machine Learning
### 5. News & Sentiment
### 6. Risk Analysis
### 7. Company Information
### 8. Stock Comparison
### 9. AI Insights
### 10. Portfolio / Investment Simulator

The first version can focus on sections 1–7 and add the remaining sections as advanced features.

---

# 5. Dashboard / Overview

The dashboard will be the first screen after the user searches for a company.

For example:

```text
┌──────────────────────────────────────────────────────────────┐
│  STOCKIQ                                     🔍 Search Stock │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  RELIANCE INDUSTRIES                         🟢 BUY         │
│  NSE: RELIANCE                                               │
│                                                              │
│  ₹2,845.20       +1.42%       Market Cap: ₹19.3T             │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Overview | Fundamentals | Technical | Prediction | News     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                     PRICE CHART                              │
│                                                              │
│            ╭──────╮                                          │
│       ╭────╯      ╰────╮                                    │
│  ─────╯                 ╰────────                             │
│                                                              │
├─────────────────────┬────────────────────────────────────────┤
│ Fundamental Score   │ Technical Score                        │
│       82/100        │       76/100                           │
├─────────────────────┼────────────────────────────────────────┤
│ Risk                │ ML Trend                               │
│ Moderate            │ Bullish                                │
└─────────────────────┴────────────────────────────────────────┘
```

The dashboard should immediately communicate:

- Current price
- Daily price change
- Market capitalization
- Overall investment signal
- Fundamental score
- Technical score
- Risk level
- Predicted trend
- Recent news
- AI-generated summary

---

# 6. Fundamental Analysis

The Fundamental Analysis section will focus on the actual company rather than short-term stock movements.

## Company Information

Display:

- Company name
- Stock symbol
- Sector
- Industry
- Founded year
- Founder
- Current CEO/Managing Director
- Headquarters
- Number of employees
- Website
- Business segments
- Major subsidiaries

## Company History

The system will provide a summarized history of the company.

The LLM can convert structured company information into an easy-to-read timeline:

```text
1966
│
├── Company Founded
│
├── Major Expansion
│
├── Entry into New Industry
│
├── Major Acquisition
│
├── International Expansion
│
└── Current Position
```

The LLM should primarily summarize verified information rather than independently inventing company facts.

---

# 7. Financial Analysis

The application should display important financial metrics.

### Revenue

Show several years of revenue and visualize the growth.

### Net Sales

Display historical net sales.

### Net Profit

Display:

- Net profit
- Profit growth
- Profit margin

### Other Important Metrics

- EBITDA
- EPS
- P/E Ratio
- P/B Ratio
- ROE
- ROCE
- Debt-to-Equity
- Dividend
- Dividend Yield
- Free Cash Flow
- Operating Margin
- Net Profit Margin

The system should provide charts such as:

- Revenue over time
- Profit over time
- EPS growth
- Debt growth
- Profit margin
- Cash flow

---

# 8. Fundamental Score

The application should convert fundamental metrics into a score.

Example:

```text
Fundamental Analysis

Revenue Growth       █████████░  90
Profit Growth        ████████░░  82
ROE                  ████████░░  81
Debt                 █████████░  91
Valuation            ██████░░░░  63

Overall Fundamental Score: 82/100
```

The score should be based on predefined rules rather than an LLM's opinion.

---

# 9. Technical Analysis

This section will analyze historical stock-price data.

The application will collect:

- Open
- High
- Low
- Close
- Adjusted Close
- Volume

The user should be able to select:

- 1 Day
- 1 Week
- 1 Month
- 6 Months
- 1 Year
- 5 Years
- Maximum available history

---

# 10. Interactive Stock Charts

The main technical chart should be a professional interactive candlestick chart.

It should allow the user to:

- Zoom
- Pan
- Change time range
- View exact prices
- View volume
- Add indicators

Possible chart:

```text
Price
 │
 │          ╭──╮
 │     ╭────╯  ╰────╮
 │ ────╯             ╰────
 │
 └────────────────────────── Time
```

Plotly should be used for interactive financial visualizations.

---

# 11. Technical Indicators

The system should calculate several technical indicators.

### Moving Averages

- SMA 20
- SMA 50
- SMA 100
- SMA 200
- EMA 20
- EMA 50

### Momentum

- RSI
- MACD
- Stochastic Oscillator

### Volatility

- Bollinger Bands
- ATR

### Volume

- Volume Moving Average
- OBV

The application should explain each indicator in simple language.

For example:

```text
RSI: 72

Interpretation:
The stock is currently in an overbought region.
```

---

# 12. Technical Signal Generation

The application can combine multiple technical indicators.

Example:

```text
SMA 50 > SMA 200             ✓ Bullish
RSI = 58                     ✓ Neutral/Bullish
MACD > Signal                ✓ Bullish
Price > SMA 200              ✓ Bullish
Volume increasing            ✓ Positive

Technical Score: 81/100
```

This produces a measurable technical score.

---

# 13. Risk Analysis

Risk analysis will be a separate section.

The system should calculate:

- Historical volatility
- Annualized volatility
- Beta
- Maximum drawdown
- Sharpe ratio
- Downside risk
- 52-week high/low
- Historical worst decline

Example:

```text
Risk Level

███████░░░  Moderate

Volatility:       21.4%
Beta:              1.08
Max Drawdown:    -23.7%
Sharpe Ratio:      1.21
```

The application should explain what these numbers mean.

---

# 14. Machine Learning Prediction

Machine Learning will be one of the most important Data Science components.

Instead of claiming that the system can perfectly predict the future price, the system should estimate **future price trends and ranges**.

## Short-Term Prediction

Possible prediction horizons:

- Next day
- Next 7 days
- Next 30 days

## Long-Term Prediction

Possible horizons:

- 3 months
- 6 months
- 1 year

The output could look like:

```text
Short-Term Outlook

Current Price: ₹2,845

Predicted Trend:
📈 Bullish

Estimated Range:
₹2,760 – ₹2,930

Model Confidence:
68%
```

The prediction should always be presented as a model estimate rather than a guaranteed future price.

---

# 15. Machine Learning Models

Multiple models should be tested.

## Model 1 — Linear Regression

Used as a baseline model.

## Model 2 — Random Forest

Features can include:

- Open
- High
- Low
- Close
- Volume
- SMA20
- SMA50
- SMA200
- RSI
- MACD
- Bollinger Bands
- Volatility

## Model 3 — XGBoost

Used as an advanced model if permitted by the project requirements.

The application should compare the models.

Example:

```text
Model Comparison

                    MAE       RMSE
Linear Regression   82.4      114.2
Random Forest       61.7       88.5
XGBoost             55.2       79.1
```

The best-performing model can be selected for the final prediction.

---

# 16. ML Evaluation

This is important for making the project academically strong.

The system should show:

- MAE
- MSE
- RMSE
- R²
- Directional Accuracy

The project should also include train/test splitting or time-series-aware validation so that future data is not accidentally used to predict the past.

---

# 17. News Analysis

The application can collect recent company-related news.

For each article:

```text
📰 Company announces major expansion

Source: News Source
Date: 18 Aug 2026

Sentiment:
🟢 Positive
```

The system can analyze multiple articles.

---

# 18. Sentiment Analysis

Use NLP to classify news into:

- Positive
- Neutral
- Negative

Example:

```text
News Sentiment

Positive   ████████████░░  62%
Neutral    █████░░░░░░░░░  25%
Negative   ███░░░░░░░░░░░  13%
```

Possible technologies:

- NLTK
- VADER
- Hugging Face Transformers

For the first implementation, VADER can provide a simple baseline.

---

# 19. LLM Integration

The LLM should not be the actual financial calculation engine.

Instead, Python should first calculate the facts:

```text
Revenue Growth: 14.2%
ROE: 18.5%
RSI: 64
SMA50 > SMA200
Volatility: 21%
News Sentiment: Positive
ML Trend: Bullish
```

Then the LLM receives these results and generates a human-readable explanation.

Example:

> The company shows healthy revenue growth and strong profitability. Its long-term technical trend is positive because the stock is trading above its major moving averages. However, the current RSI suggests that the stock may be approaching an overbought region.

This creates an excellent combination of:

**Python → Data → Analysis → ML → LLM → Human-readable explanation**

---

# 20. Overall Investment Score

The final signal should come from a transparent scoring engine.

Example:

```text
Fundamental Analysis      82/100
Technical Analysis        76/100
ML Prediction             71/100
Risk                       68/100
Sentiment                  80/100
--------------------------------
Overall Score              76/100
```

Possible classification:

```text
85–100    STRONG BUY
70–84     BUY
55–69     HOLD
40–54     SELL
0–39      STRONG SELL
```

The exact thresholds should be documented and tested.

---

# 21. Explainable BUY/HOLD/SELL Result

The application should never display only:

```text
BUY
```

Instead:

```text
╔══════════════════════════════════╗
║          🟢 BUY                  ║
║          Score: 76/100           ║
╚══════════════════════════════════╝

WHY?

✓ Revenue growth is strong
✓ ROE is healthy
✓ Long-term trend is bullish
✓ MACD indicates positive momentum
✓ News sentiment is positive

⚠ Valuation is relatively high
⚠ RSI indicates elevated momentum
⚠ Historical volatility is moderate
```

This makes the recommendation explainable.

---

# 22. Stock Comparison

Users should be able to compare multiple companies.

Example:

```text
Compare:

[ TCS ] [ Infosys ] [ HCL Tech ]
```

Then show:

| Metric | TCS | Infosys | HCL Tech |
|---|---:|---:|---:|
| Market Cap | ... | ... | ... |
| P/E | ... | ... | ... |
| ROE | ... | ... | ... |
| Revenue Growth | ... | ... | ... |
| Debt/Equity | ... | ... | ... |
| 1Y Return | ... | ... | ... |
| Volatility | ... | ... | ... |
| Fundamental Score | ... | ... | ... |
| Technical Score | ... | ... | ... |

This allows users to compare companies within the same sector.

---

# 23. Sector Analysis

The application should also show how the selected stock performs relative to its sector.

For example:

```text
IT Sector Performance

TCS             +18.4%
Infosys         +15.2%
HCL Tech        +13.8%
Wipro            +9.7%

NIFTY IT        +14.1%
NIFTY 50        +10.2%
```

This provides market context.

---

# 24. Investment Simulator

A very good additional feature would be:

### "What If I Invested?"

The user enters:

```text
Investment Amount:
₹1,00,000

Investment Date:
1 January 2021
```

The application calculates:

```text
Initial Investment     ₹1,00,000
Current Value          ₹1,84,600
Total Return              84.6%
CAGR                       XX%
```

This can be displayed through an attractive growth chart.

This feature demonstrates practical data analysis without requiring the model to make future predictions.

---

# 25. Portfolio Feature

As an advanced feature, users can create a virtual portfolio.

Example:

```text
MY PORTFOLIO

TCS              ₹50,000
RELIANCE         ₹30,000
INFOSYS          ₹20,000

Total Investment: ₹1,00,000
Current Value:    ₹1,18,400
Return:              18.4%
```

The system can calculate:

- Portfolio return
- Portfolio volatility
- Sector allocation
- Individual stock contribution
- Risk level

---

# 26. UI/UX Design

The application should look like a professional financial analytics platform rather than a typical college dashboard.

The design inspiration should be closer to:

- Bloomberg-style financial dashboards
- TradingView-style charts
- Modern fintech dashboards
- Professional analytics platforms

## Design Philosophy

Use:

**Dark professional theme**

with:

- Deep charcoal/navy background
- White/light-gray text
- Green for positive movement
- Red for negative movement
- Yellow/orange for warnings
- Subtle borders
- Rounded cards
- Minimal gradients
- Clean typography

Avoid excessive animations, bright colors, huge buttons and unnecessary decoration.

---

# 27. UI Layout

### Top Navigation

```text
┌────────────────────────────────────────────────────────────┐
│ 📈 STOCKIQ       Search stock...       Dashboard  Compare  │
└────────────────────────────────────────────────────────────┘
```

### Stock Header

```text
RELIANCE INDUSTRIES
NSE: RELIANCE

₹2,845.20
+₹39.80  (+1.42%)

🟢 BUY
Score: 76/100
```

### Navigation Tabs

```text
Overview
Fundamentals
Technical
Prediction
News
Risk
Compare
AI Insights
```

---

# 28. Cards

Use cards for important metrics:

```text
┌──────────────┐
│ Market Cap   │
│ ₹19.3 Trillion│
└──────────────┘

┌──────────────┐
│ P/E Ratio    │
│ 25.4         │
└──────────────┘

┌──────────────┐
│ ROE          │
│ 18.5%        │
└──────────────┘
```

Cards should have consistent spacing and typography.

---

# 29. Professional Color System

Use colors semantically:

```text
Green   → Positive / Buy / Growth
Red     → Negative / Sell / Loss
Yellow  → Warning / Hold / Risk
Blue    → Information
Gray    → Neutral
```

Do not use colors randomly.

---

# 30. Charts

Charts should occupy a significant portion of the interface.

Recommended:

### Plotly

For:

- Candlestick charts
- Line charts
- Volume charts
- Technical indicators
- Interactive comparisons

### Matplotlib

For:

- ML evaluation
- Static statistical visualizations
- Model comparison

### Seaborn

For:

- Correlation matrices
- Statistical visualization
- Exploratory Data Analysis

---

# 31. Required Technology Stack and Free-Only Policy

## Architecture Requirement

The application must be a separated frontend and backend application. The two top-level folders are mandatory:

```text
stock-market-analyzer/
├── backend/     # FastAPI APIs and all Python/data-science code
└── frontend/    # React web application
```

- The **backend** owns data retrieval, caching, analysis, scoring, ML, persistence and REST API endpoints.
- The **frontend** owns the user interface, client-side state and chart rendering. It must call the backend through HTTP; it must not import or run Python analysis code.
- FastAPI must expose documented REST endpoints, using Pydantic schemas and CORS configuration for the React development origin.

## Backend

- **Python 3.11+**
- **FastAPI** and Uvicorn
- Pandas and NumPy for data processing
- Scikit-learn for ML
- SQLAlchemy with SQLite for persistence and cache metadata
- Plotly-compatible JSON data returned from APIs, with chart rendering performed in React

## Frontend

- **React** with Vite
- TypeScript preferred
- React Router for page navigation
- TanStack Query (or an equivalent free library) for API state/caching
- Plotly.js / react-plotly.js or Lightweight Charts for interactive charts
- Tailwind CSS or plain CSS modules for the dark financial dashboard

## Data Processing

- Pandas
- NumPy

## Visualization

- Plotly
- Matplotlib
- Seaborn

## Machine Learning

- Scikit-learn
- XGBoost

## Technical Analysis

- pandas-ta or equivalent technical-analysis tooling
- Alternatively implement important indicators manually to demonstrate understanding

## Financial Data

Use free, no-key sources first:

- Yahoo Finance through `yfinance` for current and historical price data
- Public company pages and exchange/company disclosures for company information where permitted
- RSS feeds from reputable publishers for news headlines

Free services can change, rate-limit, delay or omit data. The backend must cache results, communicate unavailable fields clearly and never depend on a paid plan, paid API key or paid trial credit. Do not scrape a source in a way that violates its terms of use.

## NLP

- NLTK
- VADER
- Transformers

## LLM

The project should support LLM-powered summaries, suggestions and explanation text, but phase 1 must use a local Ollama model only. Do not use paid LLM APIs or cloud API keys during local development. The backend should keep calculations deterministic and use the LLM only to translate verified facts, metrics and scores into human-readable educational commentary.

Ollama should be treated as optional at runtime: if it is not running, the dashboard should still load market data and clearly show that local LLM summaries are unavailable.

## Database

Use **SQLite** for phase 1 local development and cache storage.

For deployment, plan to migrate persistence to **PostgreSQL** while keeping the same backend service boundary.

Store:

- Search history
- Cached stock data
- User watchlists
- Portfolio data
- Model results

---

# 32. Dependency Baseline

`backend/requirements.txt` should begin with free and open-source packages only:

```text
fastapi
uvicorn[standard]
pandas
numpy
yfinance
scikit-learn
requests
feedparser
nltk
vaderSentiment
sqlalchemy
aiosqlite
python-dotenv
```

`frontend/package.json` should contain the React/Vite application dependencies, for example React, TypeScript, Plotly charting, React Router and a query client. Add XGBoost, Transformers, or a local-model runtime only after the baseline works and only when the package/license and machine-resource requirements are suitable.

---

# 33. Project Architecture

A clean separated project structure should be maintained.

```text
stock-market-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application and CORS
│   │   ├── api/routes/             # stocks, analysis, news and health endpoints
│   │   ├── schemas/                # Pydantic request/response models
│   │   ├── services/               # data providers, cache and orchestration
│   │   ├── analysis/               # fundamentals, technicals, risk, sentiment
│   │   ├── ml/                     # features, training, evaluation, prediction
│   │   ├── scoring/                # explainable investment score
│   │   ├── explanations/           # rule/template-based explanations
│   │   └── db/                     # SQLite models and session
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example                # optional settings only; no secrets required
├── frontend/
│   ├── src/
│   │   ├── api/                    # typed FastAPI client
│   │   ├── components/
│   │   ├── features/               # overview, fundamentals, technical, news, risk
│   │   ├── pages/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.ts
├── docs/
├── .gitignore
└── README.md
```

---

# 34. Data Pipeline

The complete Data Science pipeline should be:

```text
DATA SOURCE
     ↓
API REQUEST
     ↓
RAW DATA
     ↓
DATA CLEANING
     ↓
MISSING VALUE HANDLING
     ↓
DATA TRANSFORMATION
     ↓
FEATURE ENGINEERING
     ↓
EDA
     ↓
TECHNICAL ANALYSIS
     ↓
MACHINE LEARNING
     ↓
MODEL EVALUATION
     ↓
SCORING
     ↓
VISUALIZATION
     ↓
LLM EXPLANATION
     ↓
USER
```

This pipeline should be clearly explained in the project report.

---

# 35. Data Cleaning

The project should demonstrate actual Data Science preprocessing.

Handle:

- Missing values
- Duplicate records
- Incorrect data types
- Date conversion
- Missing trading days
- Outliers where appropriate
- Null financial metrics
- API failures
- Inconsistent company information

Pandas will be the primary tool for this.

---

# 36. Feature Engineering

Create features such as:

```text
Daily Return
Weekly Return
Monthly Return
SMA20
SMA50
SMA200
EMA20
RSI
MACD
Bollinger Width
Volatility
Volume Change
Price Momentum
High-Low Range
```

These features can then be used for ML models.

---

# 37. Caching

Stock APIs can have rate limits.

Therefore, the application should cache frequently requested data.

For example:

```text
User searches TCS
       ↓
Check cache
       ↓
Data available?
  ↙          ↘
YES           NO
 ↓             ↓
Use cache    API request
               ↓
             Cache
```

Implement the cache in the FastAPI backend (for example, an in-memory TTL cache backed by SQLite metadata). The React frontend may cache API responses for the active browser session, but it must treat the backend as the source of truth.

---

# 38. Error Handling

The application should gracefully handle:

- Invalid stock symbols
- API failure
- Internet failure
- Missing financial information
- Rate limits
- Unsupported stocks
- optional local-explanation component failure
- Insufficient historical data

Instead of crashing:

```text
❌ Error

Unable to retrieve data for this stock.
Please check the symbol and try again.
```

---

# 39. Security

The baseline must require no paid API keys. If an optional provider is ever added, its key must never be hardcoded: load it from a local `.env` file, publish only `.env.example`, and add `.env` to `.gitignore`. Never upload keys to GitHub.

---

# 40. Performance

The application should avoid making unnecessary API calls.

Use:

- Caching
- Data reuse
- Batch requests where supported
- Lazy loading
- Limited historical ranges when appropriate

This will make the dashboard feel much faster.

---

# 41. Final Dashboard Experience

A user should be able to complete the following journey:

```text
1. Open Stock Market Analyzer

              ↓

2. Search "RELIANCE"

              ↓

3. System retrieves market data

              ↓

4. Dashboard displays current price

              ↓

5. User opens Fundamentals

              ↓

6. User sees company information
   + financial performance

              ↓

7. User opens Technical Analysis

              ↓

8. User sees candlestick chart
   + RSI + MACD + moving averages

              ↓

9. User opens Prediction

              ↓

10. ML model shows predicted trend

              ↓

11. User opens News

              ↓

12. Sentiment analysis is displayed

              ↓

13. System calculates overall score

              ↓

14. User sees:

       🟢 BUY
       Score: 76/100

              ↓

15. AI explains WHY
```

---

# 42. Final Project Architecture

The complete system can be represented as:

```text
                       ┌───────────────┐
                       │     USER      │
                       └───────┬───────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │ REACT FRONTEND   │
                     │    DASHBOARD     │
                     └────────┬─────────┘
                              │ HTTP / JSON
                              ▼
                     ┌──────────────────┐
                     │ FASTAPI BACKEND  │
                     │ APIs + SERVICES  │
                     └────────┬─────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │ Stock API  │  │ News API   │  │ Company    │
       │            │  │            │  │ Data       │
       └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
             │               │                │
             └───────────────┼────────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Data Processing │
                    │ Pandas / NumPy  │
                    └────────┬────────┘
                             │
          ┌──────────────────┼───────────────────┐
          ▼                  ▼                   ▼
 ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
 │ Fundamental    │ │ Technical      │ │ Sentiment      │
 │ Analysis       │ │ Analysis       │ │ Analysis       │
 └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            ▼
                   ┌─────────────────┐
                   │ Risk Analysis   │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Machine Learning│
                   │ Models          │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Scoring Engine  │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Rule-Based      │
                   │ Explanation     │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Final Dashboard │
                   │ BUY/HOLD/SELL   │
                   └─────────────────┘
```

---

# 43. Development Phases

The project must be completed in exactly three phases. Each phase has a demonstrable completion gate before the next begins.

## Phase 1 — Foundation and Market Dashboard

- Create root-level `backend/` and `frontend/` applications.
- Set up FastAPI, CORS, health endpoint, typed API schemas, SQLite cache and automated backend tests.
- Set up React/Vite, routing, a neutral analytics dashboard shell, loading/error/empty states and typed API client.
- Implement stock-symbol search, yfinance-backed current/historical prices, cached API responses and interactive price/volume charts.
- Deliverable: a user can search a supported symbol in React and view its current price and historical chart through FastAPI, without any key or paid service.

## Phase 2 — Explainable Analysis and Signal

- Add company profile, available financial metrics, fundamental scoring, technical indicators (SMA, EMA, RSI, MACD and Bollinger Bands) and risk metrics.
- Add free RSS news ingestion and VADER sentiment; display source, timestamp and sentiment breakdown.
- Implement transparent technical, fundamental, risk and sentiment scoring plus the final BUY/HOLD/SELL mapping.
- Generate the explanation using verified facts and deterministic templates; add an educational/not-financial-advice disclaimer.
- Deliverable: the dashboard presents an explainable analysis with clear missing-data handling, local Ollama-powered summary support and no paid API.

## Phase 3 — ML, Quality and Release

- Implement time-series-safe feature engineering, baseline regression/classification models, evaluation (MAE, RMSE, R² and directional accuracy) and model comparison.
- Show trend/range estimates as uncertain analytical outputs, never guaranteed predictions.
- Add stock comparison and, if time permits, the investment simulator; defer portfolio/watchlist/local-model enhancements unless core quality is complete.
- Complete unit/integration tests, frontend tests, accessibility and responsive checks, provider-failure tests, documentation and a free deployment option.
- Deliverable: a tested end-to-end application, reproducible setup instructions, and a final demonstration using only free/open-source resources.

---

# 44. Final Technology Stack

| Component | Technology |
|---|---|
| Backend language/framework | Python + FastAPI |
| Frontend | React + Vite + Tailwind CSS (or CSS modules) |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly.js in React; Matplotlib/Seaborn for analysis artifacts |
| Stock Data | yfinance (free, no key) |
| News | Free RSS feeds from reputable publishers |
| Technical Analysis | pandas-ta |
| Machine Learning | Scikit-learn |
| Advanced ML | Optional XGBoost (free/open-source) |
| NLP | NLTK / VADER |
| Advanced NLP | Optional local Transformers model |
| Explanations | Deterministic calculations plus local Ollama summaries/suggestions |
| Database | SQLite for local development; PostgreSQL planned for deployment |
| Environment | python-dotenv for optional configuration only |
| Version Control | Git + GitHub |
| Deployment | Free-tier/static frontend + free FastAPI-compatible hosting, or local Docker deployment |
| Cost policy | No paid dependency, paid API key, paid trial credit or required subscription |
| Documentation | Markdown |

---

# 45. What Makes This Project Different

The project should not be presented as:

> "A website that displays stock prices."

Instead, present it as:

> **"An AI-assisted financial data analytics platform that integrates market data, fundamental analysis, technical indicators, machine learning, sentiment analysis and explainable scoring to provide a comprehensive view of a company's stock."**

The key innovation is the combination of multiple analytical approaches:

```text
Fundamental Analysis
        +
Technical Analysis
        +
Risk Analysis
        +
Sentiment Analysis
        +
Machine Learning
        +
LLM Explanation
        ↓
Explainable Investment Signal
```

---

# 46. Important Academic/Data Science Components

For the Python for Data Science subject, the project should explicitly demonstrate:

### Data Collection
APIs and external datasets

### Data Cleaning
Pandas and NumPy

### EDA
Statistical summaries and visualizations

### Data Visualization
Interactive charts

### Feature Engineering
Technical and statistical features

### Machine Learning
Regression/classification models

### Model Evaluation
MAE, RMSE, R² and directional accuracy

### NLP
News sentiment analysis

### AI
LLM-based interpretation

### Data-driven Decision Making
Investment scoring system

This makes the project strongly aligned with a **Data Science curriculum**, rather than simply being a web development project.

---

# 47. Final Project Goal

The finished application should allow a user to enter a stock symbol and receive a complete, professional analysis within a few seconds.

The final result should answer:

> **What is this company?**

> **How financially healthy is it?**

> **How has its stock performed historically?**

> **What is its current technical trend?**

> **How risky is the stock?**

> **What is the current market/news sentiment?**

> **What does the ML model predict about the future trend?**

> **What are the strengths and weaknesses of the stock?**

> **Why did the system generate its final BUY/HOLD/SELL signal?**

The application should emphasize that predictions and signals are **analytical estimates, not guaranteed outcomes or personalized financial advice**.

---

# 48. Proposed Project Name

A professional name would make the project feel more complete.

Possible names:

- **StockIQ**
- **MarketMind**
- **EquityLens**
- **StockSense**
- **MarketPulse**
- **EquiVision**
- **AlphaLens**
- **StockScope**
- **FinSight**
- **MarketIntel**

My preference for the UI would be **StockIQ** or **EquityLens**.

A tagline could be:

> **StockIQ — Understand the Market. Analyze the Data.**

or:

> **EquityLens — Data-Driven Stock Intelligence.**

---

# 49. Final Recommended Scope

The ideal final version should contain:

### Core

- Stock search
- Live/current market information
- Historical prices
- Interactive charts
- Company profile
- Company history
- Financial metrics
- Fundamental score
- Technical indicators
- Technical score
- Risk analysis
- ML prediction
- News
- Sentiment analysis
- Overall BUY/HOLD/SELL signal
- Explanation of the signal

### Advanced

- Stock comparison
- Sector comparison
- Investment simulator
- Portfolio tracker
- AI-generated complete report
- Downloadable analysis report
- Watchlist
- Historical backtesting

The **core features should be completed first**. Advanced features should only be added after the fundamental data pipeline, technical analysis and ML system are working correctly.
