from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import HTTPException

from app.db.cache import CacheStore
from app.schemas.market import PricePoint, StockHistory, StockQuote


QUOTE_TTL_SECONDS = 60
HISTORY_TTL_SECONDS = 15 * 60


class MarketDataService:
    def __init__(self, cache: CacheStore | None = None) -> None:
        self.cache = cache or CacheStore()

    def get_quote(self, symbol: str) -> StockQuote:
        normalized = self._normalize_symbol(symbol)
        cache_key = f"quote:{normalized}"
        cached = self.cache.get(cache_key)
        if cached:
            return StockQuote(**cached)

        ticker = self._ticker(normalized)
        info = ticker.fast_info
        price = self._number(info.get("lastPrice") or info.get("last_price"))
        previous_close = self._number(
            info.get("previousClose")
            or info.get("regularMarketPreviousClose")
            or info.get("previous_close")
        )
        change = self._difference(price, previous_close)
        quote = StockQuote(
            symbol=normalized,
            name=self._safe_info(ticker, "shortName"),
            exchange=self._safe_info(ticker, "exchange"),
            currency=info.get("currency"),
            price=price,
            previous_close=previous_close,
            change=change,
            change_percent=self._percent(change, previous_close),
            market_state=self._safe_info(ticker, "marketState"),
        )
        self.cache.set(cache_key, quote.model_dump(), QUOTE_TTL_SECONDS)
        return quote

    def get_history(self, symbol: str, period: str = "6mo", interval: str = "1d") -> StockHistory:
        normalized = self._normalize_symbol(symbol)
        cache_key = f"history:{normalized}:{period}:{interval}"
        cached = self.cache.get(cache_key)
        if cached:
            return StockHistory(**cached)

        ticker = self._ticker(normalized)
        frame = ticker.history(period=period, interval=interval, auto_adjust=False)
        if frame.empty:
            raise HTTPException(status_code=404, detail=f"No history found for {normalized}")

        points: list[PricePoint] = []
        for index, row in frame.reset_index().iterrows():
            date_value = row.get("Date") or row.get("Datetime") or index
            if isinstance(date_value, datetime):
                date_text = date_value.date().isoformat()
            else:
                date_text = str(date_value)[:10]
            points.append(
                PricePoint(
                    date=date_text,
                    open=self._number(row.get("Open")),
                    high=self._number(row.get("High")),
                    low=self._number(row.get("Low")),
                    close=self._number(row.get("Close")),
                    volume=self._integer(row.get("Volume")),
                )
            )

        history = StockHistory(symbol=normalized, period=period, interval=interval, points=points)
        self.cache.set(cache_key, history.model_dump(), HISTORY_TTL_SECONDS)
        return history

    def _ticker(self, symbol: str) -> Any:
        try:
            import yfinance as yf
        except ImportError as exc:
            raise HTTPException(status_code=500, detail="yfinance is not installed") from exc
        return yf.Ticker(symbol)

    def _normalize_symbol(self, symbol: str) -> str:
        cleaned = symbol.strip().upper()
        if not cleaned:
            raise HTTPException(status_code=400, detail="Symbol is required")
        return cleaned

    def _safe_info(self, ticker: Any, key: str) -> str | None:
        try:
            value = ticker.info.get(key)
        except Exception:
            return None
        return str(value) if value else None

    def _number(self, value: Any) -> float | None:
        if value is None:
            return None
        try:
            return round(float(value), 4)
        except (TypeError, ValueError):
            return None

    def _integer(self, value: Any) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _difference(self, first: float | None, second: float | None) -> float | None:
        if first is None or second is None:
            return None
        return round(first - second, 4)

    def _percent(self, change: float | None, base: float | None) -> float | None:
        if change is None or not base:
            return None
        return round((change / base) * 100, 4)
