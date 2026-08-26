from __future__ import annotations

import math
from typing import Any

import pandas as pd
from fastapi import HTTPException

from app.db.cache import CacheStore
from app.schemas.market import (
    CompanyProfile,
    FundamentalMetrics,
    RiskMetrics,
    ScoreComponent,
    SentimentSummary,
    StockAnalysis,
    TechnicalIndicators,
)
from app.services.market_data import MarketDataService
from app.services.news_sentiment import NEWS_TTL_SECONDS, NewsSentimentService


ANALYSIS_TTL_SECONDS = 15 * 60


class AnalysisService:
    def __init__(self, cache: CacheStore | None = None) -> None:
        self.cache = cache or CacheStore()
        self.market_data = MarketDataService(self.cache)
        self.news = NewsSentimentService()

    def get_analysis(self, symbol: str) -> StockAnalysis:
        normalized = symbol.strip().upper()
        if not normalized:
            raise HTTPException(status_code=400, detail="Symbol is required")
        cache_key = f"analysis:{normalized}"
        cached = self.cache.get(cache_key)
        if cached:
            return StockAnalysis(**cached)

        ticker = self.market_data._ticker(normalized)
        info = self._info(ticker)
        frame = ticker.history(period="1y", interval="1d", auto_adjust=False)
        if frame.empty:
            raise HTTPException(status_code=404, detail=f"No analysis data found for {normalized}")

        profile = self._profile(normalized, info)
        fundamentals = self._fundamentals(info)
        technicals = self._technicals(frame)
        risk = self._risk(frame)
        sentiment = self._cached_sentiment(normalized, profile.name)
        components = self._score_components(fundamentals, technicals, risk, sentiment)
        final_score = round(sum(component.score for component in components) / len(components), 2)

        analysis = StockAnalysis(
            symbol=normalized,
            profile=profile,
            fundamentals=fundamentals,
            technicals=technicals,
            risk=risk,
            sentiment=sentiment,
            components=components,
            final_score=final_score,
            signal=self._signal(final_score),
            explanation=self._explanation(normalized, components, sentiment),
            disclaimer="Educational analysis only. This is not financial advice.",
        )
        self.cache.set(cache_key, analysis.model_dump(), ANALYSIS_TTL_SECONDS)
        return analysis

    def _cached_sentiment(self, symbol: str, company_name: str | None) -> SentimentSummary:
        cache_key = f"news:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return SentimentSummary(**cached)
        sentiment = self.news.get_sentiment(symbol, company_name)
        self.cache.set(cache_key, sentiment.model_dump(), NEWS_TTL_SECONDS)
        return sentiment

    def _info(self, ticker: Any) -> dict[str, Any]:
        try:
            return dict(ticker.info)
        except Exception:
            return {}

    def _profile(self, symbol: str, info: dict[str, Any]) -> CompanyProfile:
        return CompanyProfile(
            symbol=symbol,
            name=self._text(info.get("shortName") or info.get("longName")),
            sector=self._text(info.get("sector")),
            industry=self._text(info.get("industry")),
            country=self._text(info.get("country")),
            website=self._text(info.get("website")),
            market_cap=self._number(info.get("marketCap")),
            summary=self._text(info.get("longBusinessSummary")),
        )

    def _fundamentals(self, info: dict[str, Any]) -> FundamentalMetrics:
        return FundamentalMetrics(
            trailing_pe=self._number(info.get("trailingPE")),
            forward_pe=self._number(info.get("forwardPE")),
            price_to_book=self._number(info.get("priceToBook")),
            debt_to_equity=self._number(info.get("debtToEquity")),
            profit_margin=self._number(info.get("profitMargins")),
            revenue_growth=self._number(info.get("revenueGrowth")),
        )

    def _technicals(self, frame: pd.DataFrame) -> TechnicalIndicators:
        close = frame["Close"].dropna()
        if close.empty:
            return TechnicalIndicators()
        ema_12 = close.ewm(span=12, adjust=False).mean()
        ema_26 = close.ewm(span=26, adjust=False).mean()
        macd_series = ema_12 - ema_26
        macd_signal = macd_series.ewm(span=9, adjust=False).mean()
        sma_20 = close.rolling(20).mean()
        sma_50 = close.rolling(50).mean()
        rolling_std = close.rolling(20).std()

        return TechnicalIndicators(
            sma_20=self._series_last(sma_20),
            sma_50=self._series_last(sma_50),
            ema_20=self._series_last(close.ewm(span=20, adjust=False).mean()),
            rsi_14=self._rsi(close),
            macd=self._series_last(macd_series),
            macd_signal=self._series_last(macd_signal),
            bollinger_upper=self._series_last(sma_20 + rolling_std * 2),
            bollinger_lower=self._series_last(sma_20 - rolling_std * 2),
        )

    def _risk(self, frame: pd.DataFrame) -> RiskMetrics:
        close = frame["Close"].dropna()
        volume = frame["Volume"].dropna() if "Volume" in frame else pd.Series(dtype=float)
        if close.empty:
            return RiskMetrics()
        returns = close.pct_change().dropna()
        volatility = returns.tail(30).std() * math.sqrt(252) if not returns.empty else None
        drawdown = (close / close.cummax() - 1).min() if len(close) > 1 else None
        return RiskMetrics(
            volatility_30d=self._number(volatility),
            max_drawdown_1y=self._number(drawdown),
            average_volume_30d=self._number(volume.tail(30).mean()) if not volume.empty else None,
        )

    def _score_components(
        self,
        fundamentals: FundamentalMetrics,
        technicals: TechnicalIndicators,
        risk: RiskMetrics,
        sentiment: SentimentSummary,
    ) -> list[ScoreComponent]:
        return [
            self._fundamental_score(fundamentals),
            self._technical_score(technicals),
            self._risk_score(risk),
            self._sentiment_score(sentiment),
        ]

    def _fundamental_score(self, metrics: FundamentalMetrics) -> ScoreComponent:
        score = 50.0
        reasons: list[str] = []
        if metrics.trailing_pe is not None:
            if metrics.trailing_pe <= 20:
                score += 15
                reasons.append("valuation is moderate by trailing P/E")
            elif metrics.trailing_pe >= 45:
                score -= 15
                reasons.append("valuation looks stretched by trailing P/E")
        if metrics.profit_margin is not None:
            if metrics.profit_margin >= 0.15:
                score += 15
                reasons.append("profit margin is strong")
            elif metrics.profit_margin <= 0:
                score -= 15
                reasons.append("profit margin is weak")
        if metrics.revenue_growth is not None:
            if metrics.revenue_growth >= 0.08:
                score += 10
                reasons.append("revenue growth is positive")
            elif metrics.revenue_growth < 0:
                score -= 10
                reasons.append("revenue growth is negative")
        return self._component("Fundamentals", score, reasons or ["limited fundamental data was available"])

    def _technical_score(self, indicators: TechnicalIndicators) -> ScoreComponent:
        score = 50.0
        reasons: list[str] = []
        if indicators.sma_20 is not None and indicators.sma_50 is not None:
            if indicators.sma_20 > indicators.sma_50:
                score += 20
                reasons.append("20-day average is above the 50-day average")
            else:
                score -= 15
                reasons.append("20-day average is below the 50-day average")
        if indicators.rsi_14 is not None:
            if 40 <= indicators.rsi_14 <= 65:
                score += 10
                reasons.append("RSI is in a balanced range")
            elif indicators.rsi_14 > 75:
                score -= 10
                reasons.append("RSI may be overheated")
            elif indicators.rsi_14 < 30:
                score -= 5
                reasons.append("RSI shows weak momentum")
        if indicators.macd is not None and indicators.macd_signal is not None:
            if indicators.macd > indicators.macd_signal:
                score += 10
                reasons.append("MACD is above signal")
            else:
                score -= 10
                reasons.append("MACD is below signal")
        return self._component("Technicals", score, reasons or ["limited technical history was available"])

    def _risk_score(self, metrics: RiskMetrics) -> ScoreComponent:
        score = 60.0
        reasons: list[str] = []
        if metrics.volatility_30d is not None:
            if metrics.volatility_30d <= 0.25:
                score += 15
                reasons.append("recent volatility is relatively controlled")
            elif metrics.volatility_30d >= 0.55:
                score -= 20
                reasons.append("recent volatility is elevated")
        if metrics.max_drawdown_1y is not None:
            if metrics.max_drawdown_1y <= -0.35:
                score -= 15
                reasons.append("one-year drawdown is deep")
            elif metrics.max_drawdown_1y > -0.15:
                score += 10
                reasons.append("one-year drawdown is contained")
        return self._component("Risk", score, reasons or ["risk data was limited"])

    def _sentiment_score(self, sentiment: SentimentSummary) -> ScoreComponent:
        score = 50.0
        reasons = [f"headline sentiment is {sentiment.label}"]
        if sentiment.average_score is not None:
            score += sentiment.average_score * 60
        return self._component("Sentiment", score, reasons)

    def _component(self, name: str, score: float, reasons: list[str]) -> ScoreComponent:
        bounded = max(0.0, min(100.0, round(score, 2)))
        label = "strong" if bounded >= 70 else "weak" if bounded < 45 else "mixed"
        return ScoreComponent(name=name, score=bounded, label=label, rationale="; ".join(reasons))

    def _signal(self, score: float) -> str:
        if score >= 68:
            return "BUY"
        if score <= 44:
            return "SELL"
        return "HOLD"

    def _explanation(self, symbol: str, components: list[ScoreComponent], sentiment: SentimentSummary) -> str:
        strongest = max(components, key=lambda component: component.score)
        weakest = min(components, key=lambda component: component.score)
        return (
            f"{symbol} is currently rated from transparent rule-based scoring. "
            f"The strongest area is {strongest.name.lower()} because {strongest.rationale}. "
            f"The weakest area is {weakest.name.lower()} because {weakest.rationale}. "
            f"Recent news sentiment is {sentiment.label} based on {len(sentiment.articles)} headlines."
        )

    def _rsi(self, close: pd.Series) -> float | None:
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        if not gain.dropna().empty and self._series_last(loss) == 0:
            latest_gain = self._series_last(gain)
            if latest_gain and latest_gain > 0:
                return 100.0
            return 50.0
        relative_strength = gain / loss.replace(0, pd.NA)
        rsi = 100 - (100 / (1 + relative_strength))
        return self._series_last(rsi)

    def _series_last(self, series: pd.Series) -> float | None:
        cleaned = series.dropna()
        if cleaned.empty:
            return None
        return self._number(cleaned.iloc[-1])

    def _number(self, value: Any) -> float | None:
        if value is None or value is pd.NA:
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if math.isnan(number) or math.isinf(number):
            return None
        return round(number, 4)

    def _text(self, value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None
