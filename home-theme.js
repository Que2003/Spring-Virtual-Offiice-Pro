(() => {
  const root = document.documentElement;
  const themeBar = document.querySelector('.theme-bar');
  const labels = {
    spring: 'Spring', midnight: 'Midnight', blossom: 'Blossom', ocean: 'Ocean', neon: 'Neon Black', win96: 'Windows 96', flux: 'Flux AI', aqua2001: 'Aqua 2001', neural: 'Neural Teal', cybercube: 'Cyber Cube', redplanet: 'Red Planet'
  };
  const allowed = new Set(Object.keys(labels));

  if (themeBar) {
    Object.entries(labels).forEach(([key, label]) => {
      if (!themeBar.querySelector(`[data-theme="${key}"]`)) {
        const button = document.createElement('button');
        button.className = 'theme';
        button.type = 'button';
        button.dataset.theme = key;
        button.innerHTML = `<i></i>${label}`;
        themeBar.appendChild(button);
      }
    });
  }

  const style = document.createElement('style');
  style.textContent = `
    .theme[data-theme="win96"] i{background:#008080;border-radius:0}.theme[data-theme="flux"] i{background:#c026ff}.theme[data-theme="aqua2001"] i{background:#38bdf8}.theme[data-theme="neural"] i{background:#14f1e5}.theme[data-theme="cybercube"] i{background:#ff00cc}.theme[data-theme="redplanet"] i{background:#dc2626}
    [data-theme="win96"]{--bg:#008080;--surface:#c0c0c0;--surface-2:#d4d0c8;--text:#000;--muted:#202020;--accent:#000080;--accent-2:#ffff00;--line:#808080;--hero:#008080;--shadow:inset -2px -2px #808080,inset 2px 2px #fff;--glow:rgba(255,255,255,.18)}
    [data-theme="flux"]{--bg:#03040c;--surface:#070816;--surface-2:#100b2b;--text:#f7f3ff;--muted:#a39bbd;--accent:#c026ff;--accent-2:#24e7ff;--line:#2d1559;--hero:#05020d;--shadow:0 0 40px rgba(192,38,255,.22);--glow:rgba(36,231,255,.18)}
    [data-theme="aqua2001"]{--bg:#67d8ff;--surface:#dff8ff;--surface-2:#b8ecff;--text:#003049;--muted:#23576a;--accent:#0077b6;--accent-2:#9be564;--line:#7acbe8;--hero:#5dcfff;--shadow:0 28px 60px rgba(0,119,182,.18);--glow:rgba(255,255,255,.28)}
    [data-theme="neural"]{--bg:#02171d;--surface:#06242b;--surface-2:#09313a;--text:#eaffff;--muted:#8dd6db;--accent:#00e5d4;--accent-2:#46f0ff;--line:#0b6470;--hero:#041f27;--shadow:0 0 44px rgba(0,229,212,.18);--glow:rgba(0,229,212,.2)}
    [data-theme="cybercube"]{--bg:#050018;--surface:#0d0228;--surface-2:#16033d;--text:#ffffff;--muted:#c3a6ff;--accent:#ff00cc;--accent-2:#00e5ff;--line:#40116b;--hero:#080019;--shadow:0 0 54px rgba(255,0,204,.24);--glow:rgba(0,229,255,.22)}
    [data-theme="redplanet"]{--bg:#090706;--surface:#12100e;--surface-2:#21150f;--text:#fff7ed;--muted:#b79b8a;--accent:#dc2626;--accent-2:#f97316;--line:#3b2416;--hero:#0d0907;--shadow:0 0 50px rgba(249,115,22,.2);--glow:rgba(220,38,38,.18)}
    [data-theme="flux"] body:before,[data-theme="neural"] body:before,[data-theme="cybercube"] body:before,[data-theme="redplanet"] body:before,[data-theme="aqua2001"] body:before{content:"";position:fixed;inset:-20%;background:radial-gradient(circle at 25% 35%,var(--glow),transparent 28%),radial-gradient(circle at 75% 20%,color-mix(in srgb,var(--accent) 25%,transparent),transparent 28%),radial-gradient(circle at 50% 90%,color-mix(in srgb,var(--accent-2) 25%,transparent),transparent 32%);animation:homeFloat 8s linear infinite;will-change:transform;pointer-events:none;z-index:-1}
    [data-theme="flux"] .hero,[data-theme="neural"] .hero,[data-theme="cybercube"] .hero,[data-theme="redplanet"] .hero,[data-theme="aqua2001"] .hero{background:radial-gradient(circle at 50% 45%,var(--glow),transparent 38%),linear-gradient(135deg,var(--hero),var(--bg))}
    [data-theme="cybercube"] .hero:after,[data-theme="flux"] .hero:after,[data-theme="neural"] .hero:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(115deg,transparent 0 18px,color-mix(in srgb,var(--accent-2) 18%,transparent) 19px,transparent 22px);animation:homeLines 6s linear infinite;will-change:transform;pointer-events:none;opacity:.7}
    [data-theme="aqua2001"] .hero:after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 20% 80%,rgba(255,255,255,.45) 0 10px,transparent 12px),radial-gradient(circle at 70% 30%,rgba(255,255,255,.35) 0 14px,transparent 16px);animation:homeFloat 7s linear infinite;will-change:transform;pointer-events:none}
    [data-theme="win96"] body,[data-theme="win96"] .hero h1,[data-theme="win96"] .section h2,[data-theme="win96"] .brand{font-family:Tahoma,Arial,sans-serif}
    [data-theme="win96"] .theme-bar,[data-theme="win96"] .site-header,[data-theme="win96"] .preview,[data-theme="win96"] .feature-grid article{box-shadow:inset -2px -2px #808080,inset 2px 2px #fff;border-radius:0}
    @keyframes homeFloat{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(3%,2%,0) scale(1.04)}100%{transform:translate3d(0,0,0) scale(1)}}
    @keyframes homeLines{0%{transform:translate3d(0,0,0)}100%{transform:translate3d(70px,-40px,0)}}
  `;
  document.head.appendChild(style);

  const officeTheme = localStorage.getItem('springOfficePro') ? (() => { try { return JSON.parse(localStorage.getItem('springOfficePro')).theme; } catch { return null; } })() : null;
  const stored = officeTheme || localStorage.getItem('spring-office-theme') || 'spring';
  function apply(theme) {
    const selected = allowed.has(theme) ? theme : 'spring';
    root.dataset.theme = selected;
    document.querySelectorAll('.theme').forEach(button => button.classList.toggle('active', button.dataset.theme === selected));
    localStorage.setItem('spring-office-theme', selected);
    try { const officeState = JSON.parse(localStorage.getItem('springOfficePro') || '{}'); officeState.theme = selected; localStorage.setItem('springOfficePro', JSON.stringify(officeState)); } catch {}
  }
  document.querySelectorAll('.theme').forEach(button => button.addEventListener('click', () => apply(button.dataset.theme)));
  apply(stored);
})();