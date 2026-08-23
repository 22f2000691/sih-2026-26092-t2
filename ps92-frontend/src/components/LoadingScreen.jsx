import { t } from '../i18n/strings';

export default function LoadingScreen({ language }) {
  return (
    <div
      className="flex min-h-[50vh] flex-col items-center justify-center gap-6 px-4 py-16"
      role="status"
      aria-live="polite"
      aria-label={t(language, 'loadingTitle')}
    >
      <div className="relative h-16 w-16">
        <div className="absolute inset-0 rounded-full border-4 border-warm-100" />
        <div className="absolute inset-0 animate-spin rounded-full border-4 border-transparent border-t-warm-500" />
      </div>
      <div className="text-center">
        <p className="text-lg font-semibold text-slate-800">
          {t(language, 'loadingTitle')}
        </p>
        <p className="mt-1 text-base text-slate-600">
          {t(language, 'loadingSubtitle')}
        </p>
      </div>
    </div>
  );
}
