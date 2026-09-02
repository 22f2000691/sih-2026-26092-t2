import { t } from '../i18n/strings';

export default function NoMatchResults({ language, data, onRetry }) {
  return (
    <div className="mx-auto max-w-lg px-4 py-10 text-center">
      <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-sage-100">
        <svg
          className="h-8 w-8 text-sage-600"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
          />
        </svg>
      </div>
      <h2 className="text-xl font-bold text-slate-800">
        {t(language, 'noMatchTitle')}
      </h2>
      <p className="mt-3 text-base leading-relaxed text-slate-600">
        {data.message || t(language, 'noMatchHint')}
      </p>
      {data.message && (
        <p className="mt-4 text-sm text-slate-500">{t(language, 'noMatchHint')}</p>
      )}
      <button
        type="button"
        onClick={onRetry}
        className="mt-8 w-full rounded-xl bg-warm-500 px-6 py-3.5 text-base font-semibold text-white shadow-md transition hover:bg-warm-600 focus:outline-none focus:ring-2 focus:ring-warm-500 focus:ring-offset-2 sm:w-auto"
      >
        {t(language, 'backButton')}
      </button>
    </div>
  );
}
