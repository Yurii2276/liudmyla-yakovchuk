(() => {
  'use strict';

  const mobileCss = document.createElement('link');
  mobileCss.rel = 'stylesheet';
  mobileCss.href = 'assets/mobile.css';
  document.head.appendChild(mobileCss);

  document.documentElement.setAttribute('translate', 'no');
  document.documentElement.classList.add('notranslate');
  if (!document.querySelector('meta[name="google"][content="notranslate"]')) {
    const meta = document.createElement('meta');
    meta.name = 'google';
    meta.content = 'notranslate';
    document.head.appendChild(meta);
  }

  const header = document.querySelector('.site-header');
  const desktopNav = header?.querySelector('.nav');

  let menuToggle = header?.querySelector('.mobile-menu-toggle');
  let mobileMenu = document.querySelector('.mobile-menu');
  if (header && desktopNav && !menuToggle) {
    menuToggle = document.createElement('button');
    menuToggle.className = 'mobile-menu-toggle';
    menuToggle.type = 'button';
    menuToggle.setAttribute('aria-label', 'Open menu');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-controls', 'mobile-menu');
    menuToggle.innerHTML = '<span></span><span></span><span></span>';
    header.appendChild(menuToggle);
  }
  if (header && desktopNav && !mobileMenu) {
    mobileMenu = document.createElement('div');
    mobileMenu.className = 'mobile-menu';
    mobileMenu.id = 'mobile-menu';
    mobileMenu.setAttribute('aria-hidden', 'true');
    mobileMenu.innerHTML = `
      <nav class="mobile-nav" aria-label="Mobile navigation">${desktopNav.innerHTML}</nav>
      <div class="mobile-menu-footer">
        <span data-en="Official author website" data-uk="Офіційний сайт авторки">Official author website</span>
        <a href="mailto:aly2@ukr.net">aly2@ukr.net</a>
      </div>`;
    header.insertAdjacentElement('afterend', mobileMenu);
  }

  const VALID_LANGS = new Set(['en', 'uk']);

  function languageFromCookie() {
    try {
      const m = document.cookie.match(/(?:^|;\s*)liudmyla-site-lang=(en|uk)(?:;|$)/);
      return m ? m[1] : null;
    } catch (_) { return null; }
  }

  function storedLanguage() {
    try {
      const v = localStorage.getItem('liudmyla-site-lang');
      return VALID_LANGS.has(v) ? v : null;
    } catch (_) { return null; }
  }

  function languageFromUrl() {
    try {
      const v = new URL(window.location.href).searchParams.get('lang');
      return VALID_LANGS.has(v) ? v : null;
    } catch (_) { return null; }
  }

  function persistLanguage(lang) {
    try { localStorage.setItem('liudmyla-site-lang', lang); } catch (_) {}
    try { document.cookie = `liudmyla-site-lang=${lang}; path=/; max-age=31536000; SameSite=Lax`; } catch (_) {}
  }

  function syncUrlLanguage(lang) {
    try {
      const url = new URL(window.location.href);
      url.searchParams.set('lang', lang);
      history.replaceState(null, '', url.pathname + url.search + url.hash);
    } catch (_) {}
  }

  function isInternalSiteLink(a) {
    const raw = a.getAttribute('href') || '';
    if (!raw || raw.startsWith('#') || raw.startsWith('mailto:') || raw.startsWith('tel:') || raw.startsWith('javascript:')) return false;
    if (/^https?:/i.test(raw)) {
      try { return new URL(raw).origin === window.location.origin; } catch (_) { return false; }
    }
    return true;
  }

  function syncInternalLinks(lang) {
    document.querySelectorAll('a[href]').forEach(a => {
      if (!isInternalSiteLink(a)) return;
      const raw = a.getAttribute('href');
      try {
        const url = new URL(raw, window.location.href);
        if (url.origin !== window.location.origin && window.location.protocol !== 'file:') return;
        const file = url.pathname.split('/').pop();
        if (file === '' || file === 'index.html' || file === 'media.html') {
          url.searchParams.set('lang', lang);
          if (window.location.protocol === 'file:') a.href = url.href;
          else a.setAttribute('href', url.pathname + url.search + url.hash);
        }
      } catch (_) {}
    });
  }

  function updateActiveNav() {
    const page = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    const hash = location.hash || '#home';
    document.querySelectorAll('.nav a, .mobile-nav a').forEach(a => {
      const href = (a.getAttribute('href') || '').toLowerCase();
      let active = false;
      if (page === 'media.html') active = href.includes('media.html');
      else if (href.startsWith('#')) active = href === hash.toLowerCase();
      else if (href.includes('index.html#')) active = href.endsWith(hash.toLowerCase());
      else if (href.includes('media.html')) active = false;
      else active = hash === '#home' && (href === 'index.html' || href === './' || href === '/');
      a.classList.toggle('active', active);
    });
  }

  function setLanguage(lang, {updateUrl = true} = {}) {
    if (!VALID_LANGS.has(lang)) lang = 'en';
    document.documentElement.lang = lang === 'uk' ? 'uk' : 'en';
    document.documentElement.dataset.siteLang = lang;
    document.querySelectorAll('[data-en][data-uk]').forEach(el => {
      const value = el.dataset[lang];
      if (typeof value === 'string') el.innerHTML = value;
    });
    document.querySelectorAll('.lang[data-lang]').forEach(btn => {
      const active = btn.dataset.lang === lang;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    persistLanguage(lang);
    if (updateUrl) syncUrlLanguage(lang);
    syncInternalLinks(lang);
    updateActiveNav();
    if (menuToggle && menuToggle.getAttribute('aria-expanded') !== 'true') {
      menuToggle.setAttribute('aria-label', lang === 'uk' ? 'Відкрити меню' : 'Open menu');
    }
  }

  const initialLang = languageFromUrl() || storedLanguage() || languageFromCookie() || 'en';
  setLanguage(initialLang, {updateUrl: true});

  document.addEventListener('click', event => {
    const langButton = event.target.closest('.lang[data-lang]');
    if (langButton) {
      event.preventDefault();
      setLanguage(langButton.dataset.lang, {updateUrl: true});
    }
  });

  function closeMenu({restoreFocus = false} = {}) {
    if (!mobileMenu || !menuToggle) return;
    mobileMenu.classList.remove('open');
    document.body.classList.remove('menu-open');
    mobileMenu.setAttribute('aria-hidden', 'true');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', document.documentElement.dataset.siteLang === 'uk' ? 'Відкрити меню' : 'Open menu');
    if (restoreFocus) menuToggle.focus();
  }

  function openMenu() {
    if (!mobileMenu || !menuToggle) return;
    mobileMenu.classList.add('open');
    document.body.classList.add('menu-open');
    mobileMenu.setAttribute('aria-hidden', 'false');
    menuToggle.setAttribute('aria-expanded', 'true');
    menuToggle.setAttribute('aria-label', document.documentElement.dataset.siteLang === 'uk' ? 'Закрити меню' : 'Close menu');
  }

  menuToggle?.addEventListener('click', () => {
    mobileMenu?.classList.contains('open') ? closeMenu() : openMenu();
  });
  mobileMenu?.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mobileMenu?.classList.contains('open')) closeMenu({restoreFocus: true});
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 1050) closeMenu(); });
  window.addEventListener('hashchange', updateActiveNav);

  [
    'assets/img-author-white.js',
    'assets/img-author-gray.js',
    'assets/img-cover.js',
    'assets/img-books.js',
    'assets/img-media-a.js',
    'assets/img-media-b.js'
  ].forEach(src => {
    const script = document.createElement('script');
    script.src = src;
    script.defer = true;
    document.head.appendChild(script);
  });
})();
