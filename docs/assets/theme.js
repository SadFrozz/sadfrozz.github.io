'use strict';
try {
  const savedTheme = localStorage.getItem('sadfrozz-theme');
  if (savedTheme === 'light' || savedTheme === 'dark') {
    document.documentElement.dataset.theme = savedTheme;
  }
} catch {
  // The system preference still applies when browser storage is unavailable.
}
