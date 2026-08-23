const FIELD_LABELS = {
  income: { en: 'your annual income', hi: 'आपकी वार्षिक आय' },
  amount_needed: { en: 'how much you need', hi: 'आपको कितनी राशि चाहिए' },
  category: { en: 'your category (SC/ST/OBC)', hi: 'आपकी श्रेणी (SC/ST/OBC)' },
  purpose: { en: 'what you need the loan for', hi: 'ऋण का उद्देश्य' },
};

export function formatCurrency(amount) {
  if (amount == null) return '—';
  if (amount >= 100000) {
    const lakhs = amount / 100000;
    const formatted = lakhs % 1 === 0 ? lakhs.toFixed(0) : lakhs.toFixed(1);
    return `₹${formatted}L`;
  }
  return `₹${amount.toLocaleString('en-IN')}`;
}

/** Full rupee amount with optional decimals — for EMI breakdowns */
export function formatAmount(amount) {
  if (amount == null) return '—';
  return `₹${Number(amount).toLocaleString('en-IN', {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  })}`;
}

export function formatIncome(amount) {
  return formatCurrency(amount);
}

export function getFieldLabel(field, language = 'English') {
  const lang = language === 'Hindi' ? 'hi' : 'en';
  return FIELD_LABELS[field]?.[lang] ?? field.replace(/_/g, ' ');
}

export function formatMissingFields(missingFields, language = 'English') {
  return missingFields.map((f) => getFieldLabel(f, language));
}

export function formatChannelType(channelType) {
  const map = {
    'SCA/PSB/RRB': 'via Public Sector Bank',
    'NBFC-MFI': 'via Microfinance Institution',
    'Co-operative Society/Bank': 'via Co-operative Bank',
  };
  return map[channelType] ?? channelType;
}

export function buildParsedSummary(parsedInput, language = 'English') {
  const { income, amount_needed, purpose } = parsedInput;
  const incomeStr = formatIncome(income);
  const amountStr = formatCurrency(amount_needed);

  if (language === 'Hindi') {
    return `आपकी जानकारी के अनुसार: आय ${incomeStr}, ${purpose} के लिए ${amountStr} की जरूरत`;
  }
  return `Based on what you told us: Income ${incomeStr}, Need ${amountStr} for ${purpose}`;
}
