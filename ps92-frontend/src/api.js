/**
 * API layer — isolated fetch logic.
 *
 * TO SWITCH TO LIVE API:
 *   1. Set USE_MOCK = false
 *   2. Ensure backend is running at API_BASE_URL
 */

import {
  MOCK_SUCCESS_RESPONSE,
  MOCK_INCOMPLETE_RESPONSE,
  MOCK_NO_MATCH_RESPONSE,
  MOCK_DELAY_MS,
  MOCK_SCENARIO,
} from './data/mockData';

/** Toggle this single flag to use live API instead of mock data */
export const USE_MOCK = false;

export const API_BASE_URL = 'https://sih-ps92.onrender.com/';

/**
 * POST /recommend — fetch loan scheme recommendations.
 * @param {{ text: string, language: string }} payload
 * @returns {Promise<object>}
 */
export async function fetchRecommendations({ text, language }) {
  if (USE_MOCK) {
    return getMockResponse({ text, language });
  }

  const response = await fetch(`${API_BASE_URL}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language }),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const message =
      errorBody.detail || `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return response.json();
}

/**
 * POST /calculate-emi — compute EMI for a scheme.
 * @param {{ principal: number, annual_interest_rate: number, tenure_years: number, moratorium_months: number }} payload
 * @returns {Promise<{ monthly_emi: number, total_payment: number, total_interest: number }>}
 */
export async function fetchCalculateEmi({
  principal,
  annual_interest_rate,
  tenure_years,
  moratorium_months = 0,
}) {
  const response = await fetch(`${API_BASE_URL}/calculate-emi`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      principal,
      annual_interest_rate,
      tenure_years,
      moratorium_months,
    }),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const message =
      errorBody.detail || `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return response.json();
}

async function getMockResponse({ text, language }) {
  await delay(MOCK_DELAY_MS);

  // Simple keyword triggers for manual testing without changing MOCK_SCENARIO
  const lower = text.toLowerCase();
  if (lower.includes('incomplete') || lower.includes('missing')) {
    return { ...MOCK_INCOMPLETE_RESPONSE };
  }
  if (lower.includes('no match') || lower.includes('no scheme')) {
    return { ...MOCK_NO_MATCH_RESPONSE };
  }
  if (lower.includes('error') || lower.includes('fail')) {
    throw new Error('Failed to generate explanations: API quota exceeded (mock)');
  }

  switch (MOCK_SCENARIO) {
    case 'incomplete':
      return { ...MOCK_INCOMPLETE_RESPONSE };
    case 'no_match':
      return { ...MOCK_NO_MATCH_RESPONSE };
    case 'error':
      throw new Error('Failed to generate explanations: API quota exceeded (mock)');
    case 'success':
    default:
      return { ...MOCK_SUCCESS_RESPONSE };
  }
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
