from __future__ import annotations

import requests

from app.core.config import get_settings
from app.schemas.market import SuggestionResponse


class OllamaService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def status(self) -> dict[str, str | bool]:
        try:
            response = requests.get(f"{self.settings.ollama_base_url}/api/tags", timeout=2)
            response.raise_for_status()
            models = response.json().get("models", [])
            configured = self.settings.ollama_model
            has_model = any(model.get("name", "").startswith(configured) for model in models)
            return {
                "provider": "ollama",
                "model": configured,
                "available": has_model,
            }
        except requests.RequestException:
            return {
                "provider": "ollama",
                "model": self.settings.ollama_model,
                "available": False,
            }

    def suggest(self, symbol: str, context: str) -> SuggestionResponse:
        prompt = (
            "You are helping summarize stock-market research for education only. "
            "Do not give financial advice. Use the supplied facts and mention uncertainty.\n\n"
            f"Symbol: {symbol.upper()}\n"
            f"Context:\n{context}\n\n"
            "Write a concise summary and a few watch-points."
        )
        try:
            response = requests.post(
                f"{self.settings.ollama_base_url}/api/generate",
                json={"model": self.settings.ollama_model, "prompt": prompt, "stream": False},
                timeout=30,
            )
            response.raise_for_status()
            suggestion = response.json().get("response", "").strip()
            return SuggestionResponse(
                provider="ollama",
                model=self.settings.ollama_model,
                available=True,
                suggestion=suggestion or "Ollama returned an empty response.",
            )
        except requests.RequestException:
            return SuggestionResponse(
                provider="ollama",
                model=self.settings.ollama_model,
                available=False,
                suggestion="Local Ollama is not reachable yet. Start Ollama and pull the configured model to enable summaries.",
            )
