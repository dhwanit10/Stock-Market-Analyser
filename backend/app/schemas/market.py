from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
    database: str
    llm_provider: str


class StockQuote(BaseModel):
    symbol: str
    name: str | None = None
    exchange: str | None = None
    currency: str | None = None
    price: float | None = None
    previous_close: float | None = None
    change: float | None = None
    change_percent: float | None = None
    market_state: str | None = None
    source: str = "yfinance"


class PricePoint(BaseModel):
    date: str
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    volume: int | None = None


class StockHistory(BaseModel):
    symbol: str
    period: str
    interval: str
    points: list[PricePoint]
    source: str = "yfinance"


class SuggestionRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=16)
    context: str = Field(min_length=1, max_length=4000)


class SuggestionResponse(BaseModel):
    provider: str
    model: str
    available: bool
    suggestion: str


class CompanyProfile(BaseModel):
    symbol: str
    name: str | None = None
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    website: str | None = None
    market_cap: float | None = None
    summary: str | None = None


class FundamentalMetrics(BaseModel):
    trailing_pe: float | None = None
    forward_pe: float | None = None
    price_to_book: float | None = None
    debt_to_equity: float | None = None
    profit_margin: float | None = None
    revenue_growth: float | None = None


class TechnicalIndicators(BaseModel):
    sma_20: float | None = None
    sma_50: float | None = None
    ema_20: float | None = None
    rsi_14: float | None = None
    macd: float | None = None
    macd_signal: float | None = None
    bollinger_upper: float | None = None
    bollinger_lower: float | None = None


class RiskMetrics(BaseModel):
    volatility_30d: float | None = None
    max_drawdown_1y: float | None = None
    average_volume_30d: float | None = None


class NewsItem(BaseModel):
    title: str
    source: str | None = None
    published: str | None = None
    link: str | None = None
    sentiment: float
    label: str


class SentimentSummary(BaseModel):
    average_score: float | None = None
    label: str
    articles: list[NewsItem]


class ScoreComponent(BaseModel):
    name: str
    score: float
    label: str
    rationale: str


class StockAnalysis(BaseModel):
    symbol: str
    profile: CompanyProfile
    fundamentals: FundamentalMetrics
    technicals: TechnicalIndicators
    risk: RiskMetrics
    sentiment: SentimentSummary
    components: list[ScoreComponent]
    final_score: float
    signal: str
    explanation: str
    disclaimer: str
