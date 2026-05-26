(() => {
  const root = document.documentElement;
  const themes = document.querySelectorAll('.theme');
  const allowed = new Set(['spring', 'midnight', 'blossom', 'ocean', 'neon', 'win96']);

  const officeTheme = localStorage.getItem('springOfficePro')
    ? (() => {
        try {
          return JSON.parse(localStorage.getItem('springOfficePro')).theme;
        } catch {
          return null;
        }
      })()
    : null;

  const stored = officeTheme || localStorage.getItem('spring-office-theme') || 'spring';

  function apply(theme) {
    const selected = allowed.has(theme) ? theme : 'spring';

    root.dataset.theme = selected;

    themes.forEach((button) => {
      button.classList.toggle('active', button.dataset.theme === selected);
    });

    localStorage.setItem('spring-office-theme', selected);

    try {
      const officeState = JSON.parse(localStorage.getItem('springOfficePro') || '{}');
      officeState.theme = selected;
      localStorage.setItem('springOfficePro', JSON.stringify(officeState));
    } catch {}
  }

  themes.forEach((button) => {
    button.addEventListener('click', () => apply(button.dataset.theme));
  });

  apply(stored);
})();