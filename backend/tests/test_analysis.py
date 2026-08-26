import pandas as pd

from app.schemas.market import FundamentalMetrics, RiskMetrics, SentimentSummary, TechnicalIndicators
from app.services.analysis import AnalysisService


def test_technical_indicator_calculation() -> None:
    service = AnalysisService()
    frame = pd.DataFrame(
        {
            "Close": [float(value) for value in range(100, 170)],
            "Volume": [1000 for _ in range(70)],
        }
    )

    indicators = service._technicals(frame)

    assert indicators.sma_20 is not None
    assert indicators.sma_50 is not None
    assert indicators.rsi_14 is not None
    assert indicators.macd is not None


def test_scoring_outputs_signal_components() -> None:
    service = AnalysisService()
    components = service._score_components(
        FundamentalMetrics(trailing_pe=18, profit_margin=0.2, revenue_growth=0.12),
        TechnicalIndicators(sma_20=120, sma_50=100, rsi_14=55, macd=2, macd_signal=1),
        RiskMetrics(volatility_30d=0.2, max_drawdown_1y=-0.1),
        SentimentSummary(average_score=0.3, label="positive", articles=[]),
    )

    assert len(components) == 4
    assert service._signal(75) == "BUY"
    assert service._signal(50) == "HOLD"
    assert service._signal(35) == "SELL"
