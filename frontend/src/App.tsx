import { useEffect, useMemo, useState, type FormEvent } from 'react';
import { Activity, BarChart3, BrainCircuit, Newspaper, RefreshCw, Search, ShieldCheck } from 'lucide-react';
import { getAnalysis, getHistory, getLlmStatus, getLlmSuggestion, getQuote } from './api/client';
import { PriceChart } from './components/PriceChart';
import type { LlmStatus, StockAnalysis, StockHistory, StockQuote } from './types';

function formatCurrency(value: number | null, currency: string | null) {
  if (value === null) return 'N/A';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency ?? 'USD',
    maximumFractionDigits: 2,
  }).format(value);
}

function formatNumber(value: number | null, digits = 2) {
  if (value === null) return 'N/A';
  return value.toLocaleString('en-US', { maximumFractionDigits: digits });
}

function formatPercent(value: number | null) {
  if (value === null) return 'N/A';
  return `${(value * 100).toFixed(2)}%`;
}

function App() {
  const [symbol, setSymbol] = useState('AAPL');
  const [activeSymbol, setActiveSymbol] = useState('AAPL');
  const [quote, setQuote] = useState<StockQuote | null>(null);
  const [history, setHistory] = useState<StockHistory | null>(null);
  const [analysis, setAnalysis] = useState<StockAnalysis | null>(null);
  const [llmStatus, setLlmStatus] = useState<LlmStatus | null>(null);
  const [suggestion, setSuggestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggesting, setSuggesting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    getLlmStatus().then(setLlmStatus).catch(() => setLlmStatus({ provider: 'ollama', model: 'unknown', available: false }));
  }, []);

  useEffect(() => {
    async function loadMarketData() {
      setLoading(true);
      setError('');
      setSuggestion('');
      try {
        const [nextQuote, nextHistory, nextAnalysis] = await Promise.all([
          getQuote(activeSymbol),
          getHistory(activeSymbol),
          getAnalysis(activeSymbol),
        ]);
        setQuote(nextQuote);
        setHistory(nextHistory);
        setAnalysis(nextAnalysis);
      } catch (nextError) {
        setError(nextError instanceof Error ? nextError.message : 'Unable to load stock data.');
      } finally {
        setLoading(false);
      }
    }

    loadMarketData();
  }, [activeSymbol]);

  const marketContext = useMemo(() => {
    if (!quote) return '';
    return [
      `Current price: ${quote.price ?? 'unknown'} ${quote.currency ?? ''}`,
      `Previous close: ${quote.previous_close ?? 'unknown'}`,
      `Change percent: ${quote.change_percent ?? 'unknown'}`,
      `Exchange: ${quote.exchange ?? 'unknown'}`,
      analysis ? `Signal: ${analysis.signal} with score ${analysis.final_score}` : '',
      analysis ? `Explanation: ${analysis.explanation}` : '',
    ].join('\n');
  }, [quote, analysis]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = symbol.trim().toUpperCase();
    if (trimmed) setActiveSymbol(trimmed);
  }

  async function handleSuggestion() {
    if (!quote || !marketContext) return;
    setSuggesting(true);
    setSuggestion('');
    try {
      const response = await getLlmSuggestion(quote.symbol, marketContext);
      setSuggestion(response.suggestion);
    } catch (nextError) {
      setSuggestion(nextError instanceof Error ? nextError.message : 'Unable to get an Ollama summary.');
    } finally {
      setSuggesting(false);
    }
  }

  const changeClass = (quote?.change ?? 0) >= 0 ? 'positive' : 'negative';

  return (
    <main className="app-shell">
      <section className="toolbar">
        <div>
          <p className="eyebrow">Phase 2 Analysis Dashboard</p>
          <h1>Stock Market Analyzer</h1>
        </div>
        <form className="search-form" onSubmit={handleSubmit}>
          <Search size={18} aria-hidden="true" />
          <input value={symbol} onChange={(event) => setSymbol(event.target.value)} aria-label="Stock symbol" />
          <button type="submit">Analyze</button>
        </form>
      </section>

      {error && <div className="alert">{error}</div>}

      <section className="dashboard-grid">
        <div className="summary-panel">
          <div className="panel-title">
            <Activity size={20} />
            <span>Market Snapshot</span>
          </div>
          {loading ? (
            <div className="empty-state">Loading {activeSymbol}...</div>
          ) : quote ? (
            <>
              <div className="quote-heading">
                <div>
                  <h2>{quote.symbol}</h2>
                  <p>{quote.name ?? 'Company name unavailable'}</p>
                </div>
                <span>{quote.exchange ?? 'N/A'}</span>
              </div>
              <div className="price-row">
                <strong>{formatCurrency(quote.price, quote.currency)}</strong>
                <span className={changeClass}>
                  {quote.change === null ? 'N/A' : `${quote.change.toFixed(2)} (${quote.change_percent?.toFixed(2) ?? '0.00'}%)`}
                </span>
              </div>
              <dl className="metrics">
                <div>
                  <dt>Previous Close</dt>
                  <dd>{formatCurrency(quote.previous_close, quote.currency)}</dd>
                </div>
                <div>
                  <dt>Market State</dt>
                  <dd>{quote.market_state ?? 'Unknown'}</dd>
                </div>
                <div>
                  <dt>Source</dt>
                  <dd>{quote.source}</dd>
                </div>
              </dl>
            </>
          ) : (
            <div className="empty-state">Enter a ticker symbol to begin.</div>
          )}
        </div>

        <div className="chart-section">
          <div className="panel-title">
            <RefreshCw size={20} />
            <span>Six Month Price History</span>
          </div>
          {history ? <PriceChart points={history.points} /> : <div className="empty-state">Chart data will appear here.</div>}
        </div>

        <div className="score-panel">
          <div className="panel-title">
            <BarChart3 size={20} />
            <span>Explainable Signal</span>
          </div>
          {analysis ? (
            <>
              <div className={`signal-badge signal-${analysis.signal.toLowerCase()}`}>
                <span>{analysis.signal}</span>
                <strong>{analysis.final_score.toFixed(1)}</strong>
              </div>
              <p className="explanation-text">{analysis.explanation}</p>
              <div className="score-grid">
                {analysis.components.map((component) => (
                  <div className="score-card" key={component.name}>
                    <div>
                      <span>{component.name}</span>
                      <strong>{component.score.toFixed(1)}</strong>
                    </div>
                    <meter min="0" max="100" value={component.score} />
                    <p>{component.rationale}</p>
                  </div>
                ))}
              </div>
              <p className="disclaimer">{analysis.disclaimer}</p>
            </>
          ) : (
            <div className="empty-state">Analysis will appear here.</div>
          )}
        </div>

        <div className="detail-panel">
          <div className="panel-title">
            <ShieldCheck size={20} />
            <span>Fundamentals, Technicals and Risk</span>
          </div>
          {analysis ? (
            <div className="detail-grid">
              <dl>
                <dt>Sector</dt>
                <dd>{analysis.profile.sector ?? 'N/A'}</dd>
                <dt>Industry</dt>
                <dd>{analysis.profile.industry ?? 'N/A'}</dd>
                <dt>Market Cap</dt>
                <dd>{formatCurrency(analysis.profile.market_cap, quote?.currency ?? 'USD')}</dd>
              </dl>
              <dl>
                <dt>Trailing P/E</dt>
                <dd>{formatNumber(analysis.fundamentals.trailing_pe)}</dd>
                <dt>Profit Margin</dt>
                <dd>{formatPercent(analysis.fundamentals.profit_margin)}</dd>
                <dt>Revenue Growth</dt>
                <dd>{formatPercent(analysis.fundamentals.revenue_growth)}</dd>
              </dl>
              <dl>
                <dt>SMA 20 / SMA 50</dt>
                <dd>{formatNumber(analysis.technicals.sma_20)} / {formatNumber(analysis.technicals.sma_50)}</dd>
                <dt>RSI 14</dt>
                <dd>{formatNumber(analysis.technicals.rsi_14)}</dd>
                <dt>MACD / Signal</dt>
                <dd>{formatNumber(analysis.technicals.macd)} / {formatNumber(analysis.technicals.macd_signal)}</dd>
              </dl>
              <dl>
                <dt>30D Volatility</dt>
                <dd>{formatPercent(analysis.risk.volatility_30d)}</dd>
                <dt>1Y Max Drawdown</dt>
                <dd>{formatPercent(analysis.risk.max_drawdown_1y)}</dd>
                <dt>30D Avg Volume</dt>
                <dd>{formatNumber(analysis.risk.average_volume_30d, 0)}</dd>
              </dl>
            </div>
          ) : (
            <div className="empty-state">Metrics will appear here.</div>
          )}
        </div>

        <div className="news-panel">
          <div className="panel-title">
            <Newspaper size={20} />
            <span>News Sentiment</span>
          </div>
          {analysis ? (
            <>
              <p className="sentiment-summary">
                Headlines are {analysis.sentiment.label}
                {analysis.sentiment.average_score !== null ? ` with average VADER score ${analysis.sentiment.average_score.toFixed(2)}` : ''}.
              </p>
              <div className="news-list">
                {analysis.sentiment.articles.length === 0 ? (
                  <div className="empty-state">No recent RSS headlines found.</div>
                ) : (
                  analysis.sentiment.articles.slice(0, 5).map((article) => (
                    <a href={article.link ?? '#'} target="_blank" rel="noreferrer" className="news-item" key={`${article.title}-${article.published}`}>
                      <span className={article.label}>{article.label}</span>
                      <p>{article.title}</p>
                      <small>{article.source ?? 'RSS'} {article.published ? `· ${article.published}` : ''}</small>
                    </a>
                  ))
                )}
              </div>
            </>
          ) : (
            <div className="empty-state">Sentiment will appear here.</div>
          )}
        </div>

        <div className="llm-panel">
          <div className="panel-title">
            <BrainCircuit size={20} />
            <span>Local LLM Summary</span>
          </div>
          <p className="llm-status">
            Ollama {llmStatus?.available ? 'ready' : 'not connected'} · Model {llmStatus?.model ?? 'checking'}
          </p>
          <button className="secondary-action" type="button" onClick={handleSuggestion} disabled={!quote || suggesting}>
            {suggesting ? 'Summarizing...' : 'Ask Ollama for summary'}
          </button>
          <div className="suggestion-box">{suggestion || 'Local LLM suggestions will appear here when Ollama is running.'}</div>
        </div>
      </section>
    </main>
  );
}

export default App;
