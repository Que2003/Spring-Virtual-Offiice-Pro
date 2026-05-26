(() => {
  const root = document.documentElement;
  const themes = document.querySelectorAll('.theme');
  const allowed = new Set(['spring', 'midnight', 'blossom', 'ocean', 'neon']);
  const stored = localStorage.getItem('spring-office-theme');

  function apply(theme) {
    const selected = allowed.has(theme) ? theme : 'spring';
    root.dataset.theme = selected;
    themes.forEach((button) => button.classList.toggle('active', button.dataset.theme === selected));
    localStorage.setItem('spring-office-theme', selected);
  }

  themes.forEach((button) => {
    button.addEventListener('click', () => apply(button.dataset.theme));
  });

  if (stored) apply(stored);
})();
