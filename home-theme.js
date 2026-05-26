(() => {
  const root = document.documentElement;
  const themeBar = document.querySelector('.theme-bar');

  if (themeBar && !themeBar.querySelector('[data-theme="win96"]')) {
    const button = document.createElement('button');
    button.className = 'theme';
    button.type = 'button';
    button.dataset.theme = 'win96';
    button.innerHTML = '<i></i>Windows 96';
    themeBar.appendChild(button);
  }

  const themes = document.querySelectorAll('.theme');
  const allowed = new Set(['spring', 'midnight', 'blossom', 'ocean', 'neon', 'win96']);

  const style = document.createElement('style');
  style.textContent = `
    .theme[data-theme="win96"] i{background:#008080;border:1px solid #000;border-radius:0}
    [data-theme="win96"]{--bg:#008080;--surface:#c0c0c0;--surface-2:#d4d0c8;--text:#000;--muted:#202020;--accent:#000080;--accent-2:#ffff00;--line:#808080;--hero:#008080;--shadow:inset -2px -2px #808080,inset 2px 2px #fff;--glow:rgba(255,255,255,.18)}
    [data-theme="win96"] body{font-family:Tahoma,Arial,sans-serif}
    [data-theme="win96"] .theme-bar,[data-theme="win96"] .site-header,[data-theme="win96"] .preview,[data-theme="win96"] .feature-grid article,[data-theme="win96"] .room-grid a,[data-theme="win96"] footer{box-shadow:inset -2px -2px #808080,inset 2px 2px #fff;border-radius:0}
    [data-theme="win96"] .nav-action,[data-theme="win96"] .primary,[data-theme="win96"] .secondary,[data-theme="win96"] .theme,[data-theme="win96"] .assistant{border-radius:0;box-shadow:inset -1px -1px #000,inset 1px 1px #fff}
    [data-theme="win96"] .hero h1,[data-theme="win96"] .section h2,[data-theme="win96"] .brand,[data-theme="win96"] .footer-inner strong{font-family:Tahoma,Arial,sans-serif}
    [data-theme="win96"] .hero h1 em{color:#ffff00;background:#000080;padding:0 .12em}
  `;
  document.head.appendChild(style);

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
    document.querySelectorAll('.theme').forEach((button) => {
      button.classList.toggle('active', button.dataset.theme === selected);
    });
    localStorage.setItem('spring-office-theme', selected);
    try {
      const officeState = JSON.parse(localStorage.getItem('springOfficePro') || '{}');
      officeState.theme = selected;
      localStorage.setItem('springOfficePro', JSON.stringify(officeState));
    } catch {}
  }

  document.querySelectorAll('.theme').forEach((button) => {
    button.addEventListener('click', () => apply(button.dataset.theme));
  });

  apply(stored);
})();