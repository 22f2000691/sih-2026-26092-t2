import { t } from '../i18n/strings';
import LanguageSelector from './LanguageSelector';

export default function LandingScreen({
  language,
  onLanguageChange,
  text,
  onTextChange,
  onSubmit,
  isSubmitting,
}) {
  const canSubmit = text.trim().length > 0 && !isSubmitting;

  return (
    <div className="mx-auto max-w-xl px-4 py-8 sm:py-12">
      <header className="mb-10 text-center">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-warm-100 px-4 py-1.5 text-sm font-medium text-warm-700">
          <span className="h-2 w-2 rounded-full bg-warm-500" aria-hidden="true" />
          {t(language, 'tagline')}
        </div>
        <h1 className="text-2xl font-bold leading-tight text-slate-800 sm:text-3xl">
          {t(language, 'heroTitle')}
        </h1>
        <p className="mt-4 text-base leading-relaxed text-slate-600 sm:text-lg">
          {t(language, 'heroSubtitle')}
        </p>
      </header>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (canSubmit) onSubmit();
        }}
        className="space-y-5"
      >
        <LanguageSelector
          value={language}
          onChange={onLanguageChange}
          label={t(language, 'languageLabel')}
        />

        <div>
          <label
            htmlFor="situation-input"
            className="mb-2 block text-sm font-medium text-slate-600"
          >
            {t(language, 'inputLabel')}
          </label>
          <textarea
            id="situation-input"
            rows={6}
            value={text}
            onChange={(e) => onTextChange(e.target.value)}
            placeholder={t(language, 'inputPlaceholder')}
            className="w-full resize-none rounded-2xl border border-warm-200 bg-white px-4 py-4 text-base leading-relaxed text-slate-800 shadow-sm placeholder:text-slate-400 transition focus:border-warm-500 focus:outline-none focus:ring-2 focus:ring-warm-500/30"
            disabled={isSubmitting}
          />
        </div>

        <button
          type="submit"
          disabled={!canSubmit}
          className="w-full rounded-xl bg-warm-500 px-6 py-4 text-base font-semibold text-white shadow-md transition hover:bg-warm-600 focus:outline-none focus:ring-2 focus:ring-warm-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {t(language, 'submitButton')}
        </button>
      </form>
    </div>
  );
}
