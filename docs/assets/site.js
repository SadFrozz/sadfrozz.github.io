'use strict';
const themeToggle = document.querySelector('.theme-toggle');
if (themeToggle) {
  const root = document.documentElement;
  const systemTheme = matchMedia('(prefers-color-scheme: dark)');
  const currentTheme = () => root.dataset.theme || (systemTheme.matches ? 'dark' : 'light');
  const refreshTheme = () => {
    const dark = currentTheme() === 'dark';
    themeToggle.setAttribute('aria-pressed', String(dark));
    themeToggle.title = root.lang === 'ru'
      ? (dark ? 'Включить светлую тему' : 'Включить тёмную тему')
      : (dark ? 'Switch to light theme' : 'Switch to dark theme');
  };
  themeToggle.addEventListener('click', () => {
    root.dataset.theme = currentTheme() === 'dark' ? 'light' : 'dark';
    try {
      localStorage.setItem('sadfrozz-theme', root.dataset.theme);
    } catch {
      // Keep the selected theme for this page when storage is unavailable.
    }
    refreshTheme();
  });
  systemTheme.addEventListener('change', refreshTheme);
  refreshTheme();
  themeToggle.hidden = false;
}

const controls = document.querySelector('.catalogue-controls');
if (controls) {
  controls.hidden = false;
  const cards = [...document.querySelectorAll('.project-card')];
  const filters = [...controls.querySelectorAll('[data-filter]')];
  const input = controls.querySelector('input');
  const empty = document.querySelector('.no-results');
  const result = document.querySelector('.filter-result');
  let category = 'all';
  function update() {
    const query = input.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const card of cards) {
      card.hidden = !((category === 'all' || card.dataset.category === category) && card.dataset.search.toLocaleLowerCase().includes(query));
      if (!card.hidden) visible++;
    }
    empty.hidden = visible !== 0;
    result.textContent = document.documentElement.lang === 'ru' ? `Найдено проектов: ${visible}` : `Projects found: ${visible}`;
    for (const button of filters) button.setAttribute('aria-pressed', String(button.dataset.filter === category));
  }
  filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
  input.addEventListener('input', update);
}
