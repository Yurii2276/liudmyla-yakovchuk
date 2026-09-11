from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

CRITICAL = r'''<style id="final-critical-v9">
html,body{max-width:100%;overflow-x:hidden!important}.site-header{position:sticky;top:0;z-index:50}.mobile-menu-toggle,.mobile-menu{display:none}
@media(max-width:1050px){.site-header{grid-template-columns:minmax(0,1fr) auto auto!important;gap:12px!important}.site-header>.nav{display:none!important}.mobile-menu-toggle{display:flex!important;width:44px;height:44px;padding:10px;border:0;background:transparent;cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:5px;z-index:52}.mobile-menu-toggle span{width:24px;height:2px;background:#4c1d25;display:block;transition:.18s}.mobile-menu-toggle[aria-expanded="true"] span:nth-child(1){transform:translateY(7px) rotate(45deg)}.mobile-menu-toggle[aria-expanded="true"] span:nth-child(2){opacity:0}.mobile-menu-toggle[aria-expanded="true"] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}.mobile-menu{display:block;position:fixed;z-index:49;left:0;right:0;top:76px;bottom:0;background:#fffdf9;padding:18px 28px 28px;opacity:0;visibility:hidden;pointer-events:none;transform:translateY(-10px);transition:opacity .18s,transform .18s;overflow:auto}.mobile-menu.open{opacity:1!important;visibility:visible!important;pointer-events:auto!important;transform:none!important}.mobile-nav{display:flex;flex-direction:column}.mobile-nav a{display:flex;align-items:center;justify-content:space-between;min-height:58px;padding:12px 2px;border-bottom:1px solid #eadfd6;color:#4c1d25;font:500 26px/1.1 Georgia,"Times New Roman",serif}.mobile-nav a:after{content:'→';font-size:18px;color:#b59887}.mobile-menu-footer{display:flex;flex-direction:column;gap:6px;padding-top:24px;color:#8b7b72;font-size:12px}.mobile-menu-footer a{font:16px Georgia,"Times New Roman",serif;color:#4c1d25}.brand{min-width:0}.lang-switch{white-space:nowrap}.novel-band{overflow:hidden}.novel-art:before{inset:10% 0 0 0!important}}
@media(max-width:680px){.site-header{height:72px!important;padding-left:16px!important;padding-right:10px!important}.mobile-menu{top:72px}.brand-name{font-size:clamp(21px,6.8vw,28px)!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.brand-tag{font-size:6.8px!important;letter-spacing:.20em!important}.lang-switch{font-size:12px!important;gap:3px!important}.hero-skyline{left:0!important;right:0!important}.mobile-menu-toggle{width:42px;height:42px;padding:9px}}
body.menu-open{overflow:hidden}
</style>'''

BURGER = '<button class="mobile-menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>'

HOME_MENU = '''<div class="mobile-menu" id="mobile-menu" aria-hidden="true"><nav class="mobile-nav" aria-label="Mobile navigation"><a href="#home" class="active" data-en="Home" data-uk="Головна">Home</a><a href="#book" data-en="Book" data-uk="Книга">Book</a><a href="#author" data-en="Author" data-uk="Авторка">Author</a><a href="#trailer" data-en="Trailer" data-uk="Трейлер">Trailer</a><a href="media.html" data-en="Media" data-uk="Медіа">Media</a><a href="#contact" data-en="Contact" data-uk="Контакти">Contact</a></nav><div class="mobile-menu-footer"><span data-en="Official author website" data-uk="Офіційний сайт авторки">Official author website</span><a href="mailto:aly2@ukr.net">aly2@ukr.net</a></div></div>'''

MEDIA_MENU = '''<div class="mobile-menu" id="mobile-menu" aria-hidden="true"><nav class="mobile-nav" aria-label="Mobile navigation"><a href="index.html" data-en="Home" data-uk="Головна">Home</a><a href="index.html#book" data-en="Book" data-uk="Книга">Book</a><a href="index.html#author" data-en="Author" data-uk="Авторка">Author</a><a href="index.html#trailer" data-en="Trailer" data-uk="Трейлер">Trailer</a><a href="media.html" class="active" data-en="Media" data-uk="Медіа">Media</a><a href="#contact" data-en="Contact" data-uk="Контакти">Contact</a></nav><div class="mobile-menu-footer"><span data-en="Official author website" data-uk="Офіційний сайт авторки">Official author website</span><a href="mailto:aly2@ukr.net">aly2@ukr.net</a></div></div>'''

RUNTIME = r'''<script id="final-runtime-v9">
(()=>{'use strict';const OK=new Set(['en','uk']);function initial(){try{const u=new URL(location.href).searchParams.get('lang');if(OK.has(u))return u;const s=localStorage.getItem('liudmyla-site-lang');return OK.has(s)?s:'en'}catch(e){return'en'}}function syncLinks(lang){document.querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href')||'';if(!h||h[0]==='#'||h.startsWith('mailto:')||h.startsWith('tel:')||/^https?:/i.test(h))return;try{const u=new URL(h,location.href),f=u.pathname.split('/').pop();if(f===''||f==='index.html'||f==='media.html'){u.searchParams.set('lang',lang);a.setAttribute('href',(f||'index.html')+u.search+u.hash)}}catch(e){}})}function setLang(lang){if(!OK.has(lang))lang='en';document.documentElement.lang=lang==='uk'?'uk':'en';document.querySelectorAll('[data-en][data-uk]').forEach(e=>e.innerHTML=e.dataset[lang]);document.querySelectorAll('.lang[data-lang]').forEach(b=>{const on=b.dataset.lang===lang;b.classList.toggle('active',on);b.setAttribute('aria-pressed',on?'true':'false')});try{localStorage.setItem('liudmyla-site-lang',lang);const u=new URL(location.href);u.searchParams.set('lang',lang);history.replaceState(null,'',u.pathname+u.search+u.hash)}catch(e){}syncLinks(lang)}setLang(initial());document.addEventListener('click',e=>{const b=e.target.closest('.lang[data-lang]');if(b){e.preventDefault();setLang(b.dataset.lang)}});const t=document.querySelector('.mobile-menu-toggle'),m=document.querySelector('.mobile-menu');function close(){if(!m||!t)return;m.classList.remove('open');document.body.classList.remove('menu-open');m.setAttribute('aria-hidden','true');t.setAttribute('aria-expanded','false')}if(t&&m)t.addEventListener('click',()=>{const o=!m.classList.contains('open');m.classList.toggle('open',o);document.body.classList.toggle('menu-open',o);m.setAttribute('aria-hidden',o?'false':'true');t.setAttribute('aria-expanded',o?'true':'false')});m?.addEventListener('click',e=>{if(e.target.closest('a'))close()});document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});window.addEventListener('resize',()=>{if(innerWidth>1050)close()})})();
</script>'''

def base_patch(text: str, menu: str) -> str:
    text = text.replace('<html lang="en">', '<html lang="en" translate="no" class="notranslate">', 1)
    if 'name="google" content="notranslate"' not in text:
        text = text.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="google" content="notranslate">\n  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">', 1)
    if 'id="final-critical-v9"' not in text:
        text = text.replace('</head>', CRITICAL + '\n</head>', 1)
    if 'class="mobile-menu-toggle"' not in text:
        text = text.replace('</header>', '  ' + BURGER + '\n</header>', 1)
    if 'id="mobile-menu"' not in text:
        text = text.replace('</header>', '</header>\n' + menu, 1)
    text = re.sub(r'<script\s+src=["\']assets/site\.js(?:\?[^"\']*)?["\']\s*></script>', '', text, flags=re.I)
    if 'id="final-runtime-v9"' not in text:
        text = text.replace('</body>', RUNTIME + '\n</body>', 1)
    return text

def patch_media(text: str) -> str:
    text = base_patch(text, MEDIA_MENU)
    replacements = {
        r'<img\s+id="mediaHero"[^>]*>': '<img src="assets/author-white.jpeg" alt="Liudmyla Yakovchuk">',
        r'<img\s+id="eventTalk"[^>]*>': '<img src="assets/media-event-talk.jpg" alt="Book presentation event">',
        r'<img\s+id="signing"[^>]*>': '<img src="assets/media-signing.jpg" alt="Liudmyla Yakovchuk signing copies">',
        r'<img\s+id="portraitDesk"[^>]*>': '<img src="assets/media-portrait-desk.jpg" alt="Author portrait at a writing desk">',
        r'<img\s+id="terrace"[^>]*>': '<img src="assets/media-terrace.jpg" alt="Liudmyla Yakovchuk on a terrace">',
        r'<img\s+id="embroidered"[^>]*>': '<img src="assets/media-embroidered.jpg" alt="Author portrait in embroidered clothing">',
    }
    for pat, repl in replacements.items():
        text = re.sub(pat, repl, text, count=1, flags=re.I)
    text = re.sub(r'<script\s+src=["\']assets/media-sprite-hq\.js["\']\s*></script>\s*<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', '', text, count=1, flags=re.S|re.I)
    repair = '<script src="assets/img-author-white.js?v=final9"></script><script src="assets/img-media-a.js?v=final9"></script><script src="assets/img-media-b.js?v=final9"></script>'
    if 'img-media-a.js?v=final9' not in text:
        text = text.replace(RUNTIME, repair + '\n' + RUNTIME, 1)
    return text

def patch_home(text: str) -> str:
    return base_patch(text, HOME_MENU)

for name, fn in [('index.html', patch_home), ('media.html', patch_media)]:
    p = ROOT / name
    original = p.read_text(encoding='utf-8')
    new = fn(original)
    p.write_text(new, encoding='utf-8')

# Static acceptance checks: fail the workflow instead of publishing a broken navigation/media build.
home = (ROOT/'index.html').read_text(encoding='utf-8')
media = (ROOT/'media.html').read_text(encoding='utf-8')
assert 'class="mobile-menu-toggle"' in home and 'class="mobile-menu-toggle"' in media
assert home.count('class="mobile-nav"') == 1 and media.count('class="mobile-nav"') == 1
assert 'id="final-runtime-v9"' in home and 'id="final-runtime-v9"' in media
assert 'assets/media-event-talk.jpg' in media and 'assets/media-embroidered.jpg' in media
assert 'img-media-a.js?v=final9' in media and 'img-media-b.js?v=final9' in media
assert 'media-sprite-hq.js' not in media
print('Final site patch checks: PASS')
