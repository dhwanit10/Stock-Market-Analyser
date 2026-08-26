import type { LlmStatus, StockAnalysis, StockHistory, StockQuote } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail ?? `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function getQuote(symbol: string): Promise<StockQuote> {
  return request<StockQuote>(`/api/stocks/${encodeURIComponent(symbol)}/quote`);
}

export function getHistory(symbol: string, period = '6mo'): Promise<StockHistory> {
  return request<StockHistory>(`/api/stocks/${encodeURIComponent(symbol)}/history?period=${period}&interval=1d`);
}

export function getAnalysis(symbol: string): Promise<StockAnalysis> {
  return request<StockAnalysis>(`/api/stocks/${encodeURIComponent(symbol)}/analysis`);
}

export function getLlmStatus(): Promise<LlmStatus> {
  return request<LlmStatus>('/api/llm/status');
}

export function getLlmSuggestion(symbol: string, context: string): Promise<{ suggestion: string; available: boolean }> {
  return request('/api/llm/suggest', {
    method: 'POST',
    body: JSON.stringify({ symbol, context }),
  });
}
