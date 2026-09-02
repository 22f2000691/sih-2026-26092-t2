export const LANGUAGES = [
  { code: 'English', label: 'English' },
  { code: 'Hindi', label: 'हिंदी (Hindi)' },
];

export const strings = {
  English: {
    appName: 'Scheme Finder',
    tagline: 'Find the right NSFDC loan for you',
    heroTitle: 'Find the right loan scheme for your dream',
    heroSubtitle:
      'Tell us about yourself in your own words — your income, what you need money for, and how much. We will match you with government schemes made for SC beneficiaries.',
    languageLabel: 'Language',
    inputLabel: 'Describe your situation',
    inputPlaceholder:
      'Tell us about your income, what you need the loan for, and how much you need…\n\nExample: "I earn 3.5 lakh a year, need 1.2 lakh for a dairy business, I am SC category"',
    submitButton: 'Find My Scheme',
    loadingTitle: 'Finding schemes for you…',
    loadingSubtitle: 'This usually takes a few seconds',
    backButton: 'Try again',
    bestFit: 'Best fit',
    maxLoan: 'Max loan',
    interestRate: 'Interest',
    repayment: 'Repayment',
    years: 'years',
    perYear: 'p.a.',
    calculateEmi: 'Calculate EMI',
    emiBreakdown: 'EMI breakdown',
    emiBasedOn: 'Based on your loan amount of',
    monthlyEmi: 'Monthly EMI',
    totalPayment: 'Total payment',
    totalInterest: 'Total interest',
    emiLoading: 'Calculating EMI…',
    emiError: 'Could not calculate EMI. Please try again.',
    findBranch: 'Find Nearest Branch',
    incompleteTitle: 'We need a little more information',
    incompleteHint: 'Please include these details in your message:',
    noMatchTitle: 'No matching scheme right now',
    noMatchHint:
      'We could not find a scheme that fits your details. You can try again with different income, amount, or purpose — sometimes a small change helps.',
    errorTitle: 'Something went wrong',
    errorHint:
      'We could not process your request right now. Please check your connection and try again in a moment.',
    footerNote: 'NSFDC concessional loan schemes for SC beneficiaries',
  },
  Hindi: {
    appName: 'योजना खोजक',
    tagline: 'अपने लिए सही NSFDC ऋण खोजें',
    heroTitle: 'अपने सपने के लिए सही ऋण योजना खोजें',
    heroSubtitle:
      'अपनी बात अपने शब्दों में बताएं — आपकी आय, पैसे की जरूरत किस लिए है, और कितनी। हम SC लाभार्थियों के लिए सरकारी योजनाओं से मिलान करेंगे।',
    languageLabel: 'भाषा',
    inputLabel: 'अपनी स्थिति बताएं',
    inputPlaceholder:
      'अपनी आय, ऋण का उद्देश्य, और कितनी राशि चाहिए — बताएं…\n\nउदाहरण: "मेरी सालाना आय 3.5 लाख है, डेयरी व्यवसाय के लिए 1.2 लाख चाहिए, मैं SC श्रेणी से हूँ"',
    submitButton: 'मेरी योजना खोजें',
    loadingTitle: 'आपके लिए योजनाएं खोज रहे हैं…',
    loadingSubtitle: 'इसमें कुछ सेकंड लग सकते हैं',
    backButton: 'फिर से कोशिश करें',
    bestFit: 'सबसे उपयुक्त',
    maxLoan: 'अधिकतम ऋण',
    interestRate: 'ब्याज',
    repayment: 'चुकौती',
    years: 'वर्ष',
    perYear: 'प्रति वर्ष',
    calculateEmi: 'EMI गणना करें',
    emiBreakdown: 'EMI विवरण',
    emiBasedOn: 'आपकी ऋण राशि के आधार पर',
    monthlyEmi: 'मासिक EMI',
    totalPayment: 'कुल भुगतान',
    totalInterest: 'कुल ब्याज',
    emiLoading: 'EMI की गणना हो रही है…',
    emiError: 'EMI की गणना नहीं हो सकी। कृपया फिर कोशिश करें।',
    findBranch: 'नजदीकी शाखा खोजें',
    incompleteTitle: 'हमें थोड़ी और जानकारी चाहिए',
    incompleteHint: 'कृपया अपने संदेश में ये विवरण शामिल करें:',
    noMatchTitle: 'अभी कोई उपयुक्त योजना नहीं मिली',
    noMatchHint:
      'आपके विवरण के अनुसार कोई योजना नहीं मिली। अलग आय, राशि, या उद्देश्य के साथ फिर से कोशिश करें — कभी-कभी छोटा बदलाव मदद करता है।',
    errorTitle: 'कुछ गलत हो गया',
    errorHint:
      'हम अभी आपका अनुरोध संसाधित नहीं कर सके। कृपया अपना कनेक्शन जांचें और थोड़ी देर बाद फिर कोशिश करें।',
    footerNote: 'SC लाभार्थियों के लिए NSFDC रियायती ऋण योजनाएं',
  },
};

export function t(language, key) {
  const lang = language === 'Hindi' ? 'Hindi' : 'English';
  return strings[lang][key] ?? strings.English[key] ?? key;
}
