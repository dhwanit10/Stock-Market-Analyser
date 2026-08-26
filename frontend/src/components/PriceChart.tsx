import type { PricePoint } from '../types';

type PriceChartProps = {
  points: PricePoint[];
};

export function PriceChart({ points }: PriceChartProps) {
  const closes = points.filter((point) => point.close !== null);
  if (closes.length === 0) {
    return <div className="empty-state">No price history available.</div>;
  }

  const values = closes.map((point) => point.close as number);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const width = 720;
  const height = 260;
  const padding = 24;

  const path = closes
    .map((point, index) => {
      const x = padding + (index / Math.max(closes.length - 1, 1)) * (width - padding * 2);
      const y = height - padding - (((point.close as number) - min) / range) * (height - padding * 2);
      return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(' ');

  const latest = closes[closes.length - 1];
  const first = closes[0];
  const trendClass = (latest.close ?? 0) >= (first.close ?? 0) ? 'positive' : 'negative';

  return (
    <div className="chart-panel">
      <div className="chart-meta">
        <span>{first.date}</span>
        <span className={trendClass}>{latest.date}</span>
      </div>
      <svg className="price-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Closing price chart">
        <line x1={padding} x2={width - padding} y1={height - padding} y2={height - padding} />
        <line x1={padding} x2={padding} y1={padding} y2={height - padding} />
        <path d={path} />
      </svg>
      <div className="chart-range">
        <span>Low {min.toFixed(2)}</span>
        <span>High {max.toFixed(2)}</span>
      </div>
    </div>
  );
}
