from fastapi import APIRouter, Query

from app.core.config import get_settings
from app.schemas.market import HealthResponse, StockAnalysis, StockHistory, StockQuote, SuggestionRequest, SuggestionResponse
from app.services.analysis import AnalysisService
from app.services.market_data import MarketDataService
from app.services.gemini import GeminiService

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        environment=settings.app_env,
        database="sqlite-local",
        llm_provider="gemini",
    )


@router.get("/stocks/{symbol}/quote", response_model=StockQuote)
def stock_quote(symbol: str) -> StockQuote:
    return MarketDataService().get_quote(symbol)


@router.get("/stocks/{symbol}/history", response_model=StockHistory)
def stock_history(
    symbol: str,
    period: str = Query(default="6mo", pattern="^(1mo|3mo|6mo|1y|2y|5y)$"),
    interval: str = Query(default="1d", pattern="^(1d|1wk|1mo)$"),
) -> StockHistory:
    return MarketDataService().get_history(symbol, period, interval)


@router.get("/stocks/{symbol}/analysis", response_model=StockAnalysis)
def stock_analysis(symbol: str) -> StockAnalysis:
    return AnalysisService().get_analysis(symbol)


@router.get("/llm/status")
def llm_status() -> dict[str, str | bool]:
    return GeminiService().status()


@router.post("/llm/suggest", response_model=SuggestionResponse)
def llm_suggest(request: SuggestionRequest) -> SuggestionResponse:
    return GeminiService().suggest(request.symbol, request.context)
