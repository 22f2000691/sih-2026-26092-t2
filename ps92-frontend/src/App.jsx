import { useState, useCallback } from 'react';
import { fetchRecommendations } from './api';
import { t } from './i18n/strings';
import LandingScreen from './components/LandingScreen';
import LoadingScreen from './components/LoadingScreen';
import SuccessResults from './components/SuccessResults';
import IncompleteResults from './components/IncompleteResults';
import NoMatchResults from './components/NoMatchResults';
import ErrorScreen from './components/ErrorScreen';

/** @typedef {'landing' | 'loading' | 'success' | 'incomplete' | 'no_match' | 'error'} AppView */

export default function App() {
  const [language, setLanguage] = useState('English');
  const [text, setText] = useState('');
  const [view, setView] = useState(/** @type {AppView} */ ('landing'));
  const [result, setResult] = useState(null);

  const handleSubmit = useCallback(async () => {
    setView('loading');
    try {
      const data = await fetchRecommendations({ text: text.trim(), language });
      setResult(data);

      switch (data.status) {
        case 'success':
          setView('success');
          break;
        case 'incomplete':
          setView('incomplete');
          break;
        case 'no_match':
          setView('no_match');
          break;
        default:
          setView('error');
      }
    } catch {
      setResult(null);
      setView('error');
    }
  }, [text, language]);

  const handleRetry = useCallback(() => {
    setView('landing');
    setResult(null);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-warm-50 to-sage-50">
      <div className="mx-auto min-h-screen max-w-3xl">
        {/* Top bar */}
        <nav className="flex items-center justify-between px-4 py-4 sm:px-6">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-warm-500 text-sm font-bold text-white">
              SF
            </div>
            <span className="text-base font-semibold text-slate-800">
              {t(language, 'appName')}
            </span>
          </div>
        </nav>

        <main>
          {view === 'landing' && (
            <LandingScreen
              language={language}
              onLanguageChange={setLanguage}
              text={text}
              onTextChange={setText}
              onSubmit={handleSubmit}
              isSubmitting={false}
            />
          )}

          {view === 'loading' && <LoadingScreen language={language} />}

          {view === 'success' && result && (
            <SuccessResults
              language={language}
              data={result}
              onRetry={handleRetry}
            />
          )}

          {view === 'incomplete' && result && (
            <IncompleteResults
              language={language}
              data={result}
              onRetry={handleRetry}
            />
          )}

          {view === 'no_match' && result && (
            <NoMatchResults
              language={language}
              data={result}
              onRetry={handleRetry}
            />
          )}

          {view === 'error' && (
            <ErrorScreen language={language} onRetry={handleRetry} />
          )}
        </main>

        <footer className="px-4 py-8 text-center text-xs text-slate-400">
          {t(language, 'footerNote')}
        </footer>
      </div>
    </div>
  );
}
