/* Cardiff learning resource UI v1.0.
 * Paste once into Xerte project Script. No script tags are needed there.
 * Initialisation is repeat-safe; notes live only in this open player. */
(function () {
  'use strict';
  if (window.CUAssessmentUI) { window.CUAssessmentUI.init(); return; }
  const mounted = new WeakSet(), state = new Map();
  const all = (root, selector) => Array.from(root.querySelectorAll(selector));
  function enhance(root) { all(root, '[data-cu-enhance]').forEach(el => el.hidden = false); }
  async function copy(root, value) {
    const status = root.querySelector('[data-cu-status]');
    const manual = root.querySelector('[data-cu-manual]');
    try {
      await navigator.clipboard.writeText(value);
      status.textContent = 'Copied.'; manual.hidden = true;
    } catch (error) {
      manual.hidden = false; manual.value = value; manual.focus(); manual.select();
      status.textContent = 'Clipboard unavailable. The text below is selected; copy it manually.';
    }
  }
  function conversation(root) {
    if (mounted.has(root)) return;
    mounted.add(root);
    const key = root.dataset.cuConversation;
    const articles = all(root, '[data-cu-question]');
    if (!state.has(key)) state.set(key, { step: 0, notes: articles.map(() => '') });
    const saved = state.get(key);
    saved.step = Math.min(saved.step, articles.length - 1);
    const fields = all(root, '[data-cu-note]');
    fields.forEach((field, i) => { field.value = saved.notes[i] || ''; });
    const buttons = all(root, '[data-cu-step]');
    const count = root.querySelector('[data-cu-count]');
    count.hidden = false;
    root.querySelector('.cu-stage').setAttribute('data-enhanced', '');
    root.querySelector('.cu-conversation-grid').setAttribute('data-enhanced', '');
    function render(focus) {
      articles.forEach((article, i) => { article.hidden = i !== saved.step; });
      buttons.forEach((button, i) => {
        button.setAttribute('aria-current', i === saved.step ? 'step' : 'false');
        button.dataset.noted = String(Boolean((saved.notes[i] || '').trim()));
      });
      count.textContent = `Question ${saved.step + 1} of ${articles.length}`;
      root.querySelector('[data-cu-prev]').disabled = saved.step === 0;
      root.querySelector('[data-cu-next]').disabled = saved.step === articles.length - 1;
      if (focus) articles[saved.step].querySelector('h3').focus({ preventScroll: true });
    }
    root.addEventListener('input', event => {
      const field = event.target.closest('[data-cu-note]');
      if (!field) return;
      saved.notes[Number(field.dataset.cuNote)] = field.value;
      buttons[Number(field.dataset.cuNote)].dataset.noted = String(Boolean(field.value.trim()));
    });
    root.addEventListener('click', event => {
      const button = event.target.closest('button');
      if (!button || !root.contains(button)) return;
      if (button.hasAttribute('data-cu-export')) {
        const lines = ['Assessment Menu · Design notes'];
        articles.forEach((article, i) => lines.push('', `${i + 1}. ${article.querySelector('h3').textContent}`, saved.notes[i] || '(No note added)'));
        lines.push('', 'Discussion notes, not an assessment or lane recommendation.');
        copy(root, lines.join('\n')); return;
      }
      if (button.hasAttribute('data-cu-step')) saved.step = Number(button.dataset.cuStep);
      else if (button.hasAttribute('data-cu-prev')) saved.step = Math.max(0, saved.step - 1);
      else if (button.hasAttribute('data-cu-next')) saved.step = Math.min(articles.length - 1, saved.step + 1);
      else return;
      render(true);
    });
    enhance(root); render(false);
  }
  function discovery(root) {
    if (mounted.has(root)) return;
    mounted.add(root); enhance(root);
    const search = root.querySelector('[data-cu-search]'), results = root.querySelector('.cu-results');
    const types = all(root, '[data-cu-type]');
    let category = 'all', timer;
    function render() {
      const query = search.value.trim().toLocaleLowerCase();
      let count = 0;
      types.forEach(type => {
        type.hidden = !(category === 'all' || type.dataset.category === category) || !type.dataset.search.toLocaleLowerCase().includes(query);
        if (!type.hidden) count++;
      });
      all(root, '[data-cu-cat]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.cuCat === category)));
      root.querySelector('[data-cu-result-count]').textContent = `${count} of ${types.length} types`;
      root.querySelector('[data-cu-empty]').hidden = count !== 0;
      root.querySelector('[data-cu-copy-types]').disabled = count === 0;
    }
    search.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(render, 150); });
    root.addEventListener('click', event => {
      const button = event.target.closest('button');
      if (!button || !root.contains(button)) return;
      if (button.hasAttribute('data-cu-view')) {
        results.dataset.view = button.dataset.cuView;
        all(root, '[data-cu-view]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      } else if (button.hasAttribute('data-cu-cat')) { category = button.dataset.cuCat; render(); }
      else if (button.hasAttribute('data-cu-reset')) { search.value = ''; category = 'all'; render(); search.focus(); }
      else if (button.hasAttribute('data-cu-copy-types')) {
        copy(root, ['Assessment Menu · Visible types', ...types.filter(t => !t.hidden).map(t => `${t.querySelector('h3').textContent} — ${t.querySelector('a').getAttribute('href')}`)].join('\n'));
      }
    });
    render();
  }
  function init() {
    document.querySelectorAll('.cu-resource [data-cu-conversation]').forEach(conversation);
    document.querySelectorAll('.cu-resource [data-cu-discovery]').forEach(discovery);
  }
  window.CUAssessmentUI = { init, version: '1.0.0' };
  // Xerte Bootstrap emits this jQuery event after inserting a page's content.
  if (window.jQuery) window.jQuery(document).on('contentLoaded.cuAssessment', init);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  init();
}());
