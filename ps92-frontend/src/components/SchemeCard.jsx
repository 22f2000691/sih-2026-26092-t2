import { useState } from 'react';
import { fetchCalculateEmi } from '../api';
import { t } from '../i18n/strings';
import {
  formatAmount,
  formatChannelType,
  formatCurrency,
} from '../utils/formatters';

export default function SchemeCard({
  scheme,
  language,
  amountNeeded,
  isBestFit = false,
  onFindBranch,
}) {
  const [emiOpen, setEmiOpen] = useState(false);
  const [emiLoading, setEmiLoading] = useState(false);
  const [emiResult, setEmiResult] = useState(null);
  const [emiError, setEmiError] = useState(null);
  const [emiPrincipal, setEmiPrincipal] = useState(null);

  const handleCalculateEmi = async () => {
    if (emiOpen && emiResult && !emiLoading) {
      setEmiOpen(false);
      return;
    }

    const principal = getEmiPrincipal(amountNeeded, scheme.max_loan_amount);
    if (principal == null) {
      setEmiOpen(true);
      setEmiResult(null);
      setEmiError(t(language, 'emiError'));
      return;
    }

    setEmiOpen(true);
    setEmiLoading(true);
    setEmiError(null);
    setEmiPrincipal(principal);

    try {
      const result = await fetchCalculateEmi({
        principal,
        annual_interest_rate: scheme.interest_rate,
        tenure_years: scheme.repayment_years,
        moratorium_months: 0,
      });
      setEmiResult(result);
    } catch {
      setEmiResult(null);
      setEmiError(t(language, 'emiError'));
    } finally {
      setEmiLoading(false);
    }
  };

  return (
    <article
      className={`relative flex flex-col rounded-2xl border bg-white p-5 shadow-sm transition ${
        isBestFit
          ? 'scale-[1.02] border-warm-500 shadow-lg ring-2 ring-warm-500/20'
          : 'border-warm-100 hover:shadow-md'
      }`}
    >
      {isBestFit && (
        <span className="absolute -top-3 left-4 rounded-full bg-warm-500 px-3 py-0.5 text-xs font-bold uppercase tracking-wide text-white">
          {t(language, 'bestFit')}
        </span>
      )}

      <h3 className="text-lg font-bold text-slate-800 sm:text-xl">
        {scheme.scheme_name}
      </h3>

      <div className="mt-4 grid grid-cols-3 gap-2">
        <StatBadge
          label={t(language, 'maxLoan')}
          value={formatCurrency(scheme.max_loan_amount)}
        />
        <StatBadge
          label={t(language, 'interestRate')}
          value={`${scheme.interest_rate}%`}
          sub={t(language, 'perYear')}
        />
        <StatBadge
          label={t(language, 'repayment')}
          value={`${scheme.repayment_years}`}
          sub={t(language, 'years')}
        />
      </div>

      <p className="mt-4 text-sm leading-relaxed text-slate-600 sm:text-base">
        {scheme.blurb}
      </p>

      <span className="mt-3 inline-flex w-fit items-center rounded-full bg-sage-100 px-3 py-1 text-xs font-medium text-sage-700">
        {formatChannelType(scheme.channel_type)}
      </span>

      <div className="mt-5 flex flex-col gap-2 sm:flex-row">
        <button
          type="button"
          onClick={handleCalculateEmi}
          disabled={emiLoading}
          aria-expanded={emiOpen}
          className="flex-1 rounded-xl border-2 border-warm-500 bg-white px-4 py-2.5 text-sm font-semibold text-warm-600 transition hover:bg-warm-50 focus:outline-none focus:ring-2 focus:ring-warm-500 focus:ring-offset-2 disabled:cursor-wait disabled:opacity-70"
        >
          {emiLoading ? t(language, 'emiLoading') : t(language, 'calculateEmi')}
        </button>
        <button
          type="button"
          onClick={() => onFindBranch?.(scheme)}
          className="flex-1 rounded-xl bg-sage-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-sage-700 focus:outline-none focus:ring-2 focus:ring-sage-600 focus:ring-offset-2"
        >
          {t(language, 'findBranch')}
        </button>
      </div>

      {emiOpen && (
        <EmiPanel
          language={language}
          loading={emiLoading}
          result={emiResult}
          error={emiError}
          principal={emiPrincipal}
        />
      )}
    </article>
  );
}

/** User's requested amount, capped at the scheme's maximum */
function getEmiPrincipal(amountNeeded, maxLoanAmount) {
  if (amountNeeded == null) return null;
  return Math.min(amountNeeded, maxLoanAmount);
}

function EmiPanel({ language, loading, result, error, principal }) {
  if (loading) {
    return (
      <div
        className="mt-4 flex items-center gap-3 rounded-xl border border-warm-200 bg-warm-50 px-4 py-4"
        role="status"
        aria-live="polite"
      >
        <div className="h-5 w-5 shrink-0 animate-spin rounded-full border-2 border-warm-200 border-t-warm-500" />
        <p className="text-sm font-medium text-slate-600">
          {t(language, 'emiLoading')}
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className="mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-4"
        role="alert"
      >
        <p className="text-sm text-red-700">{error}</p>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="mt-4 overflow-hidden rounded-xl border border-warm-200 bg-gradient-to-br from-warm-50 to-sage-50">
      <p className="border-b border-warm-200/80 bg-white/60 px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-slate-500">
        {t(language, 'emiBreakdown')}
      </p>
      <div className="px-4 py-4">
        {principal != null && (
          <p className="mb-3 text-xs text-slate-500 sm:text-sm">
            {t(language, 'emiBasedOn')}{' '}
            <span className="font-semibold text-slate-700">
              {formatAmount(principal)}
            </span>
          </p>
        )}
        <div className="rounded-xl bg-white px-4 py-3 shadow-sm ring-1 ring-warm-200/60">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
            {t(language, 'monthlyEmi')}
          </p>
          <p className="mt-1 text-2xl font-bold text-warm-600">
            {formatAmount(result.monthly_emi)}
          </p>
        </div>
        <div className="mt-3 grid grid-cols-2 gap-2">
          <EmiStat
            label={t(language, 'totalPayment')}
            value={formatAmount(result.total_payment)}
          />
          <EmiStat
            label={t(language, 'totalInterest')}
            value={formatAmount(result.total_interest)}
          />
        </div>
      </div>
    </div>
  );
}

function EmiStat({ label, value }) {
  return (
    <div className="rounded-xl bg-white/80 px-3 py-2.5 ring-1 ring-warm-100">
      <p className="text-[10px] font-medium uppercase tracking-wide text-slate-500 sm:text-xs">
        {label}
      </p>
      <p className="mt-0.5 text-sm font-bold text-slate-800 sm:text-base">
        {value}
      </p>
    </div>
  );
}

function StatBadge({ label, value, sub }) {
  return (
    <div className="rounded-xl bg-warm-50 px-2 py-2.5 text-center">
      <p className="text-[10px] font-medium uppercase tracking-wide text-slate-500 sm:text-xs">
        {label}
      </p>
      <p className="mt-0.5 text-sm font-bold text-slate-800 sm:text-base">
        {value}
        {sub && (
          <span className="ml-0.5 text-xs font-normal text-slate-500">
            {sub}
          </span>
        )}
      </p>
    </div>
  );
}
