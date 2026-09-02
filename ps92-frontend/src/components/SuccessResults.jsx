import { t } from '../i18n/strings';
import { buildParsedSummary } from '../utils/formatters';
import SchemeCard from './SchemeCard';

export default function SuccessResults({ language, data, onRetry }) {
  const { parsed_input, recommendations = [] } = data;
  const summary = buildParsedSummary(parsed_input, language);

  const handleFindBranch = (scheme) => {
    // Placeholder — map/branch finder to be wired later
    console.log('Find branch for:', scheme.scheme_id);
  };

  return (
    <div className="mx-auto max-w-2xl px-4 py-8">
      <div className="mb-2 flex items-center justify-between gap-4">
        <h2 className="text-xl font-bold text-slate-800 sm:text-2xl">
          {language === 'Hindi' ? 'आपके लिए योजनाएं' : 'Schemes for you'}
        </h2>
        <button
          type="button"
          onClick={onRetry}
          className="shrink-0 text-sm font-medium text-warm-600 underline-offset-2 hover:underline focus:outline-none focus:ring-2 focus:ring-warm-500 focus:ring-offset-2 rounded"
        >
          {t(language, 'backButton')}
        </button>
      </div>

      <p className="mb-6 rounded-xl bg-sage-50 px-4 py-3 text-sm leading-relaxed text-sage-700 sm:text-base">
        {summary}
      </p>

      <div className="flex flex-col gap-5">
        {recommendations.map((scheme, index) => (
          <SchemeCard
            key={scheme.scheme_id}
            scheme={scheme}
            language={language}
            amountNeeded={parsed_input.amount_needed}
            isBestFit={index === 0}
            onFindBranch={handleFindBranch}
          />
        ))}
      </div>
    </div>
  );
}
