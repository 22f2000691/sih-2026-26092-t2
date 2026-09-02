import { t } from '../i18n/strings';
import { formatMissingFields } from '../utils/formatters';

export default function IncompleteResults({ language, data, onRetry }) {
  const missingLabels = formatMissingFields(data.missing_fields ?? [], language);

  return (
    <div className="mx-auto max-w-lg px-4 py-10">
      <div className="mb-6 inline-flex h-14 w-14 items-center justify-center rounded-full bg-amber-50">
        <svg
          className="h-7 w-7 text-warm-600"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
          />
        </svg>
      </div>
      <h2 className="text-xl font-bold text-slate-800">
        {t(language, 'incompleteTitle')}
      </h2>
      {data.message && (
        <p className="mt-3 text-base leading-relaxed text-slate-600">
          {data.message}
        </p>
      )}
      {missingLabels.length > 0 && (
        <div className="mt-6 rounded-2xl border border-warm-200 bg-warm-50 p-5">
          <p className="mb-3 text-sm font-medium text-slate-700">
            {t(language, 'incompleteHint')}
          </p>
          <ul className="space-y-2">
            {missingLabels.map((label) => (
              <li
                key={label}
                className="flex items-center gap-2 text-base text-slate-800"
              >
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-warm-200 text-xs font-bold text-warm-700">
                  !
                </span>
                {label}
              </li>
            ))}
          </ul>
        </div>
      )}
      <button
        type="button"
        onClick={onRetry}
        className="mt-8 w-full rounded-xl bg-warm-500 px-6 py-3.5 text-base font-semibold text-white shadow-md transition hover:bg-warm-600 focus:outline-none focus:ring-2 focus:ring-warm-500 focus:ring-offset-2"
      >
        {t(language, 'backButton')}
      </button>
    </div>
  );
}
