from __future__ import annotations

from urllib.parse import quote_plus

from app.schemas.market import NewsItem, SentimentSummary


NEWS_TTL_SECONDS = 30 * 60


class NewsSentimentService:
    def get_sentiment(self, symbol: str, company_name: str | None = None) -> SentimentSummary:
        try:
            import feedparser
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        except ImportError:
            return SentimentSummary(average_score=None, label="unavailable", articles=[])

        query = quote_plus(company_name or symbol)
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={query}%20stock&hl=en-US&gl=US&ceid=US:en")
        analyzer = SentimentIntensityAnalyzer()
        articles: list[NewsItem] = []

        for entry in feed.entries[:8]:
            title = str(getattr(entry, "title", "")).strip()
            if not title:
                continue
            score = round(analyzer.polarity_scores(title)["compound"], 4)
            articles.append(
                NewsItem(
                    title=title,
                    source=self._source(entry),
                    published=str(getattr(entry, "published", "") or "") or None,
                    link=str(getattr(entry, "link", "") or "") or None,
                    sentiment=score,
                    label=self._label(score),
                )
            )

        if not articles:
            return SentimentSummary(average_score=None, label="no recent headlines", articles=[])

        average = round(sum(article.sentiment for article in articles) / len(articles), 4)
        return SentimentSummary(average_score=average, label=self._label(average), articles=articles)

    def _label(self, score: float) -> str:
        if score >= 0.2:
            return "positive"
        if score <= -0.2:
            return "negative"
        return "neutral"

    def _source(self, entry: object) -> str | None:
        source = getattr(entry, "source", None)
        if isinstance(source, dict):
            return source.get("title")
        return None
