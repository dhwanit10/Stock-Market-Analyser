from __future__ import annotations

import requests

from app.core.config import get_settings
from app.schemas.market import SuggestionResponse


class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def status(self) -> dict[str, str | bool]:
        return {
            "provider": "gemini",
            "model": self.settings.gemini_model,
            "available": bool(self.settings.gemini_api_key),
        }

    def suggest(self, symbol: str, context: str) -> SuggestionResponse:
        prompt = (
            "You are helping summarize stock-market research "
            "Do not give financial advice. Use the supplied facts and mention uncertainty.\n\n"
            f"Symbol: {symbol.upper()}\n"
            f"Context:\n{context}\n\n"
            "Write a concise summary and a few watch-points.Respond using plain text only. Do NOT use any Markdown formatting. This means absolutely no asterisks (*), no hashtags/headers (#), no backticks (`), no bulleted dashes (-), and no bold or italic syntax. Write your response entirely in natural, unformatted paragraphs."
        )
        model = self.settings.gemini_model
        response_data = SuggestionResponse(
            provider="gemini",
            model=model,
            available=False,
            suggestion="Gemini is not configured. Set GEMINI_API_KEY to enable summaries.",
        )
        if not self.settings.gemini_api_key:
            return response_data

        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                params={"key": self.settings.gemini_api_key},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=30,
            )
            response.raise_for_status()
            candidates = response.json().get("candidates", [])
            suggestion = (
                candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                if candidates
                else ""
            )
            return SuggestionResponse(
                provider="gemini",
                model=model,
                available=True,
                suggestion=suggestion or "Gemini returned an empty response.",
            )
        except (requests.RequestException, ValueError, IndexError, AttributeError):
            return SuggestionResponse(
                provider="gemini",
                model=model,
                available=False,
                suggestion="Gemini is temporarily unavailable. Check the API key and configured model.",
            )
