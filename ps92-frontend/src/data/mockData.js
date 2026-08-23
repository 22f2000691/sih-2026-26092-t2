/**
 * Mock responses for development — swap USE_MOCK to false in api.js for live API.
 */

export const MOCK_SUCCESS_RESPONSE = {
  status: 'success',
  parsed_input: {
    income: 350000,
    amount_needed: 120000,
    category: 'SC',
    purpose: 'dairy business',
  },
  recommendations: [
    {
      scheme_id: 'micro_finance',
      scheme_name: 'Micro Finance Scheme',
      max_loan_amount: 125000,
      interest_rate: 6.5,
      repayment_years: 3,
      channel_type: 'SCA/PSB/RRB',
      blurb:
        'This loan is perfect for starting your small business easily, offering low interest rates and a comfortable three-month break before repayments begin.',
    },
    {
      scheme_id: 'term_loan',
      scheme_name: 'Term Loan Scheme',
      max_loan_amount: 4500000,
      interest_rate: 8,
      repayment_years: 7,
      channel_type: 'SCA/PSB/RRB',
      blurb:
        'This scheme is great for expanding your business or farm, giving you large funding at low interest with seven comfortable years to pay back.',
    },
    {
      scheme_id: 'aajeevika_microfinance',
      scheme_name: 'Aajeevika Microfinance Yojana (AMY)',
      max_loan_amount: 125000,
      interest_rate: 15,
      repayment_years: 3,
      channel_type: 'NBFC-MFI',
      blurb:
        'This friendly loan gives SC entrepreneurs up to 1.25 lakh to start a small business, with a three-month break before repayments begin.',
    },
    {
      scheme_id: 'udyam_nidhi',
      scheme_name: 'Udyam Nidhi Yojana (UNY)',
      max_loan_amount: 450000,
      interest_rate: 13,
      repayment_years: 5,
      channel_type: 'Co-operative Society/Bank',
      blurb:
        'This scheme is wonderful for SC entrepreneurs as friendly local cooperative banks provide up to 4.5 lakh rupees with five flexible years to repay.',
    },
  ],
};

export const MOCK_INCOMPLETE_RESPONSE = {
  status: 'incomplete',
  missing_fields: ['income', 'amount_needed', 'category'],
  parsed_input: {
    income: null,
    amount_needed: null,
    category: null,
    purpose: 'business',
  },
  message:
    'Some required details are missing. Please provide: income, amount_needed, category',
};

export const MOCK_NO_MATCH_RESPONSE = {
  status: 'no_match',
  parsed_input: {
    income: 800000,
    amount_needed: 200000,
    category: 'SC',
    purpose: 'shop',
  },
  message: 'No matching schemes were found for the details provided.',
};

/** Simulated network delay in milliseconds */
export const MOCK_DELAY_MS = 1200;

/**
 * Dev helper: change this to test different response states.
 * Options: 'success' | 'incomplete' | 'no_match' | 'error'
 */
export const MOCK_SCENARIO = 'success';
