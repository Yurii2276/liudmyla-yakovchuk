const langButtons = document.querySelectorAll('.lang');
const translated = document.querySelectorAll('[data-en][data-uk]');

function setLanguage(lang) {
  document.documentElement.lang = lang;
  translated.forEach(el => { el.innerHTML = el.dataset[lang]; });
  langButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.lang === lang));
  try { localStorage.setItem('liudmyla-site-lang', lang); } catch (e) {}
}

langButtons.forEach(btn => btn.addEventListener('click', () => setLanguage(btn.dataset.lang)));
let savedLang = 'en';
try { savedLang = localStorage.getItem('liudmyla-site-lang') || 'en'; } catch (e) {}
setLanguage(savedLang);

const navLinks = document.querySelectorAll('.nav a[href]');
navLinks.forEach(a => {
  a.addEventListener('click', () => {
    navLinks.forEach(x => x.classList.remove('active'));
    a.classList.add('active');
  });
});

// GitHub Pages image fallbacks. The original full-resolution images remain in the repo,
// while these small embedded WebP versions guarantee that every image renders even if
// a binary asset was corrupted during connector upload.
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
