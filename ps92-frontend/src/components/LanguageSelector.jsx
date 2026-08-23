import { LANGUAGES } from '../i18n/strings';

export default function LanguageSelector({ value, onChange, label }) {
  return (
    <div className="w-full">
      <label
        htmlFor="language-select"
        className="mb-2 block text-sm font-medium text-slate-600"
      >
        {label}
      </label>
      <select
        id="language-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-xl border border-warm-200 bg-white px-4 py-3 text-base text-slate-800 shadow-sm transition focus:border-warm-500 focus:outline-none focus:ring-2 focus:ring-warm-500/30"
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.label}
          </option>
        ))}
      </select>
    </div>
  );
}
