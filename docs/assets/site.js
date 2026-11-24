'use strict';
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
