import { t } from '../i18n/strings';

export default function ErrorScreen({ language, onRetry }) {
  return (
    <div className="mx-auto max-w-lg px-4 py-10 text-center">
      <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-red-50">
        <svg
          className="h-8 w-8 text-red-500"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
          />
        </svg>
      </div>
      <h2 className="text-xl font-bold text-slate-800">
        {t(language, 'errorTitle')}
      </h2>
      <p className="mt-3 text-base leading-relaxed text-slate-600">
        {t(language, 'errorHint')}
      </p>
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
