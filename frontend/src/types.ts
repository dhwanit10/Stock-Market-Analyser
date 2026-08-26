export type StockQuote = {
  symbol: string;
  name: string | null;
  exchange: string | null;
  currency: string | null;
  price: number | null;
  previous_close: number | null;
  change: number | null;
  change_percent: number | null;
  market_state: string | null;
  source: string;
};

export type PricePoint = {
  date: string;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  volume: number | null;
};

export type StockHistory = {
  symbol: string;
  period: string;
  interval: string;
  points: PricePoint[];
  source: string;
};

export type LlmStatus = {
  provider: string;
  model: string;
  available: boolean;
};

export type CompanyProfile = {
  symbol: string;
  name: string | null;
  sector: string | null;
  industry: string | null;
  country: string | null;
  website: string | null;
  market_cap: number | null;
  summary: string | null;
};

export type FundamentalMetrics = {
  trailing_pe: number | null;
  forward_pe: number | null;
  price_to_book: number | null;
  debt_to_equity: number | null;
  profit_margin: number | null;
  revenue_growth: number | null;
};

export type TechnicalIndicators = {
  sma_20: number | null;
  sma_50: number | null;
  ema_20: number | null;
  rsi_14: number | null;
  macd: number | null;
  macd_signal: number | null;
  bollinger_upper: number | null;
  bollinger_lower: number | null;
};

export type RiskMetrics = {
  volatility_30d: number | null;
  max_drawdown_1y: number | null;
  average_volume_30d: number | null;
};

export type NewsItem = {
  title: string;
  source: string | null;
  published: string | null;
  link: string | null;
  sentiment: number;
  label: string;
};

export type SentimentSummary = {
  average_score: number | null;
  label: string;
  articles: NewsItem[];
};

export type ScoreComponent = {
  name: string;
  score: number;
  label: string;
  rationale: string;
};

export type StockAnalysis = {
  symbol: string;
  profile: CompanyProfile;
  fundamentals: FundamentalMetrics;
  technicals: TechnicalIndicators;
  risk: RiskMetrics;
  sentiment: SentimentSummary;
  components: ScoreComponent[];
  final_score: number;
  signal: string;
  explanation: string;
  disclaimer: string;
};
