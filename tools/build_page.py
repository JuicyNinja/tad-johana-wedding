# -*- coding: utf-8 -*-
"""Transform original-index.html -> index.html (blue & gold edition).
Keeps all copy, fonts and layout; swaps palette, ornaments, photos, adds motion."""
import re, os, shutil

ROOT = r"C:\Users\tadti\Desktop\Claude Code\Workspace\websites\Tad & Johana Wedding"
os.chdir(ROOT)
src = open('original-index.html', encoding='utf-8').read()
out = src

# ---------- 1. photos + ornaments (data URIs in document order) ----------
os.makedirs('assets/img', exist_ok=True)
uris = list(re.finditer(r'data:image/webp;base64,[A-Za-z0-9+/=]+', out))
assert len(uris) == 5, len(uris)
repl = ['assets/img/photo-1.webp', 'assets/img/photo-2.webp', 'assets/img/photo-3.webp',
        'assets/img/garland.webp', 'assets/img/garland.webp']
for m, r in reversed(list(zip(uris, repl))):
    out = out[:m.start()] + r + out[m.end():]

# ---------- 1b. names order: Tad & Johana ----------
for a,b in [
    ('<title>Johana &amp; Tad ·','<title>Tad &amp; Johana ·'),
    ('Johana Castellanos y Tad Timothy','Tad Timothy y Johana Castellanos'),
    ('content="Johana & Tad ·','content="Tad & Johana ·'),
    ('<h1 class="names">Johana<span class="amp gilt">&amp;</span>Tad</h1>','<h1 class="names">Tad<span class="amp gilt">&amp;</span>Johana</h1>'),
    ('Matrimonio%20de%20Johana%20%26%20Tad','Matrimonio%20de%20Tad%20%26%20Johana'),
    ('<p class="yr">Johana &amp; Tad ·','<p class="yr">Tad &amp; Johana ·'),
    ("'RSVP — Johana & Tad' : 'Confirmación — Johana y Tad'","'RSVP — Tad & Johana' : 'Confirmación — Tad y Johana'"),
    ('alt="Johana y Tad"','alt="Tad y Johana"'),
]:
    assert a in out, a
    out = out.replace(a, b)

# ---------- 1c. one large photo (dropped in later) ----------
PHOTO = """<div class="photos">
      <div class="film" id="film">
        <video id="story-video" playsinline muted preload="metadata" poster="assets/img/story-poster.webp" aria-label="Tad y Johana"></video>
        <button type="button" class="film-tap" hidden><span data-es>Toca para ver</span><span data-en>Tap to play</span></button>
        <button type="button" class="film-sound" aria-pressed="false">
          <span class="turn-on"><span data-es>Activar sonido</span><span data-en>Sound on</span></span>
          <span class="turn-off"><span data-es>Silenciar</span><span data-en>Mute</span></span>
        </button>
        <div class="film-progress" aria-hidden="true"></div>
      </div>
    </div>"""
out = re.sub(r'<div class="photos">.*?</figure>\n    </div>', lambda m: PHOTO, out, count=1, flags=re.S)
assert out.count('<figure') == 0 and 'id="film"' in out

# ---------- 1d. 12-hour times (both languages) ----------
T12 = {'16:00':'4:00 PM','17:15':'5:15 PM','18:00':'6:00 PM','19:00':'7:00 PM','21:30':'9:30 PM'}
out = out.replace('16:00 h', '4:00 PM').replace('19:00 h', '7:00 PM')
n_before = len(re.findall(r'\b(?:16|17|18|19|21):(?:00|15|30)\b', out))
out = re.sub(r'\b(16:00|17:15|18:00|19:00|21:30)\b', lambda m: T12[m.group(1)], out)
out = out.replace('Ceremonia%2016%3A00', 'Ceremonia%204%3A00%20PM').replace('Recepci%C3%B3n%2019%3A00', 'Recepci%C3%B3n%207%3A00%20PM')
assert n_before == 13 and not re.search(r'\b(?:16|17|18|19|21):(?:00|15|30)\b', out), n_before

# ---------- 1e. RSVP / guest policy ----------
import sys; sys.path.insert(0, os.path.join(ROOT,'tools'))
import rsvp_edits
out = rsvp_edits.apply(out)

# ---------- 1f. Google Maps Static API key (user's own key, 2026-09-15) ----------
assert out.count('key=AIzaSyDHvvSNrU9n6i68eDZuDVJxM9xqr21FWus') == 2
out = out.replace('key=AIzaSyDHvvSNrU9n6i68eDZuDVJxM9xqr21FWus', 'key=AIzaSyCfXvFkUtKSzbDfaQEAQymGQk7Oagmdwh0')

# ---------- 2. palette ----------
out = out.replace('<meta name="theme-color" content="#2B0A2E">', '<meta name="theme-color" content="#0B1533">')
out = out.replace(
    "  --plum:#2B0A2E;\n  --plum-mid:#4A0E3C;\n  --pink:#7B1450;\n  --pink-deep:#5E0F42;",
    "  --navy-deep:#060B1F;\n  --navy:#0B1533;\n  --navy-mid:#12225C;\n  --royal:#1F3A93;\n  --royal-deep:#162B6E;\n  --royal-bright:#2749A8;")
assert '--navy-deep' in out
out = out.replace('var(--plum-mid)', 'var(--navy-mid)').replace('var(--plum)', 'var(--navy)')
out = out.replace('var(--pink-deep)', 'var(--royal-deep)').replace('var(--pink)', 'var(--royal)')
out = out.replace('--cream-dim:#C9AFBE;', '--cream-dim:#B9C1DC;')
out = out.replace('rgba(43,10,46,', 'rgba(11,21,51,')
out = out.replace('rgba(201,175,190,', 'rgba(185,193,220,')
out = out.replace('#3A0A2C', '#0B1533')
out = out.replace(
    "  background:linear-gradient(178deg,#220722 0%,var(--navy) 12%,var(--navy-mid) 38%,\n    var(--royal-deep) 66%,var(--royal) 88%,#8A1A58 100%);",
    "  background:linear-gradient(178deg,var(--navy-deep) 0%,var(--navy) 14%,var(--navy-mid) 40%,\n    var(--royal-deep) 66%,var(--royal) 88%,var(--royal-bright) 100%);")
assert 'var(--royal-bright) 100%' in out
# gilt: seamless shimmer-able gradient (period = element width)
out = out.replace(
    "  background:linear-gradient(160deg,var(--gold-pale) 0%,var(--gold) 34%,var(--gold-deep) 62%,var(--gold-pale) 100%);\n  -webkit-background-clip:text;background-clip:text;color:transparent;",
    "  background:linear-gradient(90deg,var(--gold-pale) 0%,var(--gold) 12%,var(--gold-deep) 25%,var(--gold) 38%,var(--gold-pale) 50%,var(--gold) 62%,var(--gold-deep) 75%,var(--gold) 88%,var(--gold-pale) 100%);\n  background-size:200% 100%;\n  -webkit-background-clip:text;background-clip:text;color:transparent;")
assert 'background-size:200% 100%' in out
# ornaments: the gold rose was a tall portrait; the garland is a wide swag
out = out.replace(".ornament-sm{width:74px;opacity:.9}", ".ornament-sm{width:min(72vw,300px);opacity:.95}")
out = out.replace(".ornament-lg{width:158px;opacity:.95}", ".ornament-lg{width:min(84vw,400px);opacity:1}")
out = out.replace("  .ornament-sm{width:62px}\n  .ornament-lg{width:126px}", "  .ornament-sm{width:76vw}\n  .ornament-lg{width:86vw}")

# ---------- 3. extra CSS ----------
CSS = r"""
/* ================= blue & gold edition: florals + motion ================= */
.gilt{animation:gilt 9s linear infinite}
@keyframes gilt{from{background-position:0% 50%}to{background-position:200% 50%}}
@media (prefers-reduced-motion:reduce){.gilt{animation:none}}

/* hero video */
.hero{background:linear-gradient(180deg,var(--navy) 0%,var(--navy) 55%,rgba(11,21,51,0) 100%)}
.hero-media{position:absolute;inset:0;z-index:0;overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 60%,transparent 100%);
  mask-image:linear-gradient(180deg,#000 0%,#000 60%,transparent 100%)}
@media (orientation:portrait){
  .hero-media::after{
    background:radial-gradient(ellipse 72% 62% at 50% 50%,rgba(6,11,31,.72) 0%,rgba(6,11,31,.46) 50%,rgba(6,11,31,.1) 82%),
               linear-gradient(180deg,rgba(6,11,31,.5) 0%,rgba(6,11,31,.12) 30%,rgba(6,11,31,.12) 70%,rgba(6,11,31,.55) 100%)}
}
.hero-media img,.hero-media video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;display:block}
.hero-media video{opacity:0;transition:opacity 1.6s ease}
.hero-media video.ready{opacity:1}
.hero-media::after{content:"";position:absolute;inset:0;
  background:radial-gradient(ellipse 58% 52% at 50% 46%,rgba(6,11,31,.62) 0%,rgba(6,11,31,.34) 48%,rgba(6,11,31,0) 78%),
             linear-gradient(180deg,rgba(6,11,31,.38) 0%,rgba(6,11,31,0) 28%)}
.hero .wrap{text-shadow:0 2px 24px rgba(6,11,31,.9),0 0 2px rgba(6,11,31,.8)}
.hero .gilt{text-shadow:none;filter:drop-shadow(0 2px 14px rgba(6,11,31,.95))}
.hero .cd-cell{background:rgba(6,11,31,.38);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}
.scrollcue{position:absolute;left:50%;bottom:1.6rem;transform:translateX(-50%);z-index:2;width:1px;height:2.6rem;
  background:linear-gradient(180deg,var(--gold),transparent);opacity:.75;overflow:hidden}
.scrollcue::after{content:"";position:absolute;left:0;top:-100%;width:1px;height:100%;background:linear-gradient(180deg,transparent,var(--gold-pale));animation:cue 2.4s ease-in-out infinite}
@keyframes cue{to{top:110%}}
@media (prefers-reduced-motion:reduce){.scrollcue::after{animation:none}}

/* drifting petals */
.petals{position:fixed;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.petal{position:absolute;left:var(--l);top:-14vh;width:var(--w);opacity:0;will-change:transform;
  animation:fall var(--d) linear var(--delay) infinite}
.petal img{display:block;width:100%;height:auto;animation:sway var(--s) ease-in-out infinite alternate;filter:drop-shadow(0 6px 10px rgba(0,0,0,.35))}
.petal.is-petal img{animation-name:sway-p}
@keyframes fall{0%{transform:translate3d(0,0,0) rotate(0deg);opacity:0}6%{opacity:var(--o)}88%{opacity:var(--o)}100%{transform:translate3d(var(--x),124vh,0) rotate(var(--r));opacity:0}}
@keyframes sway{from{transform:translateX(-16px) rotate(-14deg)}to{transform:translateX(16px) rotate(14deg)}}
@keyframes sway-p{from{transform:translateX(-14px) rotate(-30deg) scale(1,.62)}to{transform:translateX(14px) rotate(25deg) scale(1,.7)}}
@media (prefers-reduced-motion:reduce){.petals{display:none}}

/* section florals: clip only horizontally so blooms can bleed across section edges */
html,body{overflow-x:clip}
@supports not (overflow-x:clip){section,footer{overflow:hidden}}
.flo{position:absolute;z-index:0;pointer-events:none;user-select:none;transform:translate3d(0,var(--py,0px),0);will-change:transform}
.flo img{display:block;width:100%;height:auto;opacity:0;transform:translateY(46px) scale(.94);
  transition:opacity 1.4s ease,transform 1.5s cubic-bezier(.2,.7,.3,1);filter:drop-shadow(0 16px 30px rgba(0,0,0,.5))}
.flo.in img{opacity:var(--fo,1);transform:none}
.flo.flip img{transform:translateY(46px) scale(-.94,.94)}
.flo.flip.in img{transform:scaleX(-1)}
.flo.breathe.in img{animation:breathe 9s ease-in-out infinite}
.flo.flip.breathe.in img{animation:breathe-flip 9s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-10px) rotate(1.2deg)}}
@keyframes breathe-flip{0%,100%{transform:scaleX(-1) translateY(0) rotate(0deg)}50%{transform:scaleX(-1) translateY(-10px) rotate(-1.2deg)}}
@media (prefers-reduced-motion:reduce){.flo.breathe.in img,.flo.flip.breathe.in img{animation:none}}

/* gutter = space between the text column and the viewport edge */
.flo-corner-l{left:calc(50% - var(--measure)/2 - 330px);top:-1rem;width:420px}
.flo-corner-r{right:calc(50% - var(--measure)/2 - 330px);top:-1rem;width:420px}
.flo-vine-l{left:calc(50% - var(--measure)/2 - 290px);top:4rem;width:250px}
.flo-vine-r{right:calc(50% - var(--measure)/2 - 290px);bottom:3rem;width:250px}
.flo-rose{left:calc(50% - var(--measure)/2 - 250px);top:22%;width:190px}
.flo-orchid{right:calc(50% - var(--measure)/2 - 270px);top:10%;width:220px}
.flo-orchid.mid{top:44%}
.flo-orchid-2{left:calc(50% - var(--measure)/2 - 240px);bottom:14%;width:170px}
.flo-rose-2{right:calc(50% - var(--measure)/2 - 230px);bottom:8%;width:160px}
.flo-story-l{left:calc(50% - var(--measure)/2 - 230px);top:50%;width:170px}
.flo-story-r{right:calc(50% - var(--measure)/2 - 250px);bottom:6%;width:200px}
@media (max-width:1180px){
  .flo-corner-l{left:-9vw;top:-2vw;width:34vw}
  .flo-corner-r{right:-9vw;top:-2vw;width:34vw}
  .flo-vine-l{left:-6vw;top:3rem;width:22vw}
  .flo-vine-r{right:-6vw;bottom:2rem;width:22vw}
  .flo-rose{left:-5vw;width:17vw}
  .flo-orchid{right:-5vw;width:19vw}
  .flo-orchid-2{left:-4vw;width:15vw}
  .flo-rose-2{right:-4vw;width:14vw}
  .flo-story-l{left:-4vw;width:15vw}
  .flo-story-r{right:-5vw;width:17vw}
}
@media (max-width:760px){
  .flo{--fo:.62}
  .flo-corner-l{left:-24vw;top:-6vw;width:62vw}
  .flo-corner-r{right:-24vw;top:-6vw;width:62vw}
  .flo-vine-l{left:-14vw;top:2rem;width:36vw}
  .flo-vine-r{right:-14vw;bottom:1rem;width:36vw}
  .flo-rose{left:-13vw;top:auto;bottom:-3vw;width:30vw}
  .flo-orchid{right:-14vw;top:0;width:34vw}
  /* single-bloom accents collide with the text column on phones */
  .flo-rose,.flo-orchid-2,.flo-rose-2,.flo-story-l,.flo-story-r,#rsvp .flo-vine-r{display:none}
}


/* ---------- mobile legibility ---------- */
@media (orientation:portrait){
  .hero-media video,.hero-media img{transform:scale(1.28);transform-origin:50% 42%}
  .hero-media::after{
    background:radial-gradient(ellipse 78% 64% at 50% 50%,rgba(6,11,31,.9) 0%,rgba(6,11,31,.7) 42%,rgba(6,11,31,.25) 78%,rgba(6,11,31,.05) 100%),
               linear-gradient(180deg,rgba(6,11,31,.55) 0%,rgba(6,11,31,.15) 28%,rgba(6,11,31,.15) 72%,rgba(6,11,31,.6) 100%)}
  .hero .wrap{text-shadow:0 2px 10px rgba(6,11,31,1),0 0 28px rgba(6,11,31,1),0 0 2px rgba(6,11,31,1)}
}
@media (max-width:760px){
  .theme-sub{font-size:.9rem}
  .cd-lab{font-size:.68rem;letter-spacing:.14em}
  .detail h3,.venue-k,.hop b{font-size:.8rem}
  .maplink,.mapbtn,.mappin,.tag,.field > label,.legend,footer .yr{font-size:.82rem}
  .detail .place em,.program .where{font-size:.95rem}
  .opt span{font-size:.95rem}
  .btn{font-size:.9rem}
  .lang{font-size:.85rem}
}
@media (max-width:420px){
  .cd-lab{font-size:.64rem;letter-spacing:.1em}
  .cd-num{font-size:1.55rem}
}

/* ---------- story film ---------- */
.photos{display:block;margin-top:3rem}
.film{position:relative;width:min(100%,40rem);margin:0 auto;aspect-ratio:7/4;border:1px solid var(--line);
  background:rgba(6,11,31,.4);overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.45);transition:box-shadow .6s ease}
.film video{width:100%;height:100%;object-fit:cover;display:block}
.film.locked{box-shadow:0 0 0 1px rgba(227,190,106,.7),0 0 40px rgba(227,190,106,.18),0 24px 60px rgba(0,0,0,.55)}
.film-sound{position:absolute;right:.6rem;bottom:.6rem;z-index:2;border:1px solid var(--line);background:rgba(6,11,31,.62);color:var(--cream);
  font:500 .72rem/1 var(--sans);letter-spacing:.14em;padding:.55rem .75rem;cursor:pointer;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);transition:all .2s}
.film-sound:hover{border-color:var(--gold);color:var(--gold)}
.film-sound[aria-pressed="false"] .turn-off,.film-sound[aria-pressed="true"] .turn-on{display:none}
.film-tap{position:absolute;inset:0;z-index:2;display:flex;align-items:center;justify-content:center;border:0;cursor:pointer;
  background:rgba(6,11,31,.45);color:var(--gold);font-family:var(--script);font-weight:600;font-size:2rem}
.film-tap[hidden]{display:none}
.film-progress{position:absolute;left:0;bottom:0;z-index:2;height:2px;width:0;background:linear-gradient(90deg,var(--gold-deep),var(--gold-pale));transition:width .25s linear}
.film.done .film-progress{opacity:0}
html.film-lock{scroll-behavior:auto}
@media (max-width:760px){.photos{margin-top:2.4rem}.film-sound{font-size:.78rem}}

.program .n{min-width:6.4rem;white-space:nowrap}
@media (max-width:420px){.program .n{font-size:1.5rem;min-width:5.6rem}}

.program .what,.program .where,.detail .place em,.venue-k,.hop b{display:block!important}
/* bilingual option labels: highlight whichever language span is showing */
.opt input:checked ~ span{background:linear-gradient(135deg,var(--gold-pale),var(--gold) 50%,var(--gold-deep));color:#0B1533;border-color:transparent;font-weight:500}
.opt input:focus-visible ~ span{outline:2px solid var(--gold);outline-offset:3px}

/* language toggle must beat the original's display:block rules (program, venue, hop, place em) */
html:not([lang="en"]) [data-en]{display:none!important}
html[lang="en"] [data-es]{display:none!important}

/* ---------- countdown: twice the presence ---------- */
.countdown{gap:.9rem;margin-top:3.4rem}
.cd-cell{min-width:8.2rem;padding:1.5rem .6rem 1.25rem;border-width:1px}
.cd-num{font-size:4.1rem;letter-spacing:.02em}
.cd-lab{font-size:.82rem;letter-spacing:.24em;margin-top:.7rem}
@media (max-width:760px){
  .countdown{gap:.5rem;margin-top:2.8rem}
  .cd-cell{min-width:0;flex:1;padding:1.1rem .2rem .9rem}
  .cd-num{font-size:clamp(2.2rem,10.5vw,3.2rem)}
  .cd-lab{font-size:.74rem;letter-spacing:.16em}
}
@media (max-width:420px){
  .countdown{gap:.4rem}
  .cd-num{font-size:clamp(2rem,10vw,2.6rem)}
  .cd-lab{font-size:.7rem;letter-spacing:.12em}
}

/* footer bouquet */
footer{position:relative;padding-top:3rem}
.bouquet{display:block;width:min(88vw,560px);height:auto;margin:0 auto 1.6rem;pointer-events:none;user-select:none;
  filter:drop-shadow(0 18px 34px rgba(0,0,0,.55))}
.js .bouquet{opacity:0;transform:translateY(30px) scale(.92);transition:opacity 1.6s ease,transform 1.8s cubic-bezier(.2,.7,.3,1)}
.js .bouquet.in{opacity:1;transform:none}

/* scroll reveal */
.js .rv{opacity:0;transform:translateY(26px);transition:opacity .95s ease,transform .95s cubic-bezier(.2,.7,.3,1)}
.js .rv.in{opacity:1;transform:none}
.js .detail.rv{transform:translateX(-28px)}
.js .detail.rv.in{transform:none}
.js .program li.rv{transform:translateX(22px)}
.js .program li.rv.in{transform:none}
.js .ornament.rv{transform:scale(.88);transition-duration:1.4s}
.js .ornament.rv.in{transform:none}
@media (prefers-reduced-motion:reduce){.js .rv,.js .bouquet,.flo img{opacity:1!important;transform:none!important;transition:none!important}}

/* photos: gilded hover */
.photo{transition:transform .5s cubic-bezier(.2,.7,.3,1),box-shadow .5s ease,border-color .5s ease}
.photo:hover{transform:translateY(-6px) scale(1.025)!important;border-color:var(--gold);box-shadow:0 18px 40px rgba(0,0,0,.5),0 0 0 1px rgba(227,190,106,.35)}
.photo img{transition:transform 1.2s ease}
.photo:hover img{transform:scale(1.06)}

/* detail marker glow */
.detail::before{box-shadow:0 0 0 4px rgba(227,190,106,.18),0 0 14px rgba(227,190,106,.55)}
.cd-cell{transition:border-color .4s ease,box-shadow .4s ease}
.cd-cell:hover{border-color:var(--gold);box-shadow:0 0 22px rgba(227,190,106,.25)}
"""
out = out.replace('</style>', CSS + '</style>', 1)

# ---------- 4. HTML insertions ----------
PETALS = """
<div class="petals" id="petals" aria-hidden="true"></div>
"""
out = out.replace('<div class="frame" aria-hidden="true"></div>', '<div class="frame" aria-hidden="true"></div>' + PETALS, 1)

HERO_MEDIA = """<header class="hero">
  <div class="hero-media" aria-hidden="true">
    <picture>
      <source media="(orientation: portrait)" srcset="assets/img/hero-tall-poster.webp">
      <img src="assets/img/hero-wide-poster.webp" alt="" decoding="async" fetchpriority="high">
    </picture>
    <video id="hero-video" muted loop playsinline autoplay preload="auto" disablepictureinpicture></video>
  </div>
  <div class="scrollcue" aria-hidden="true"></div>
"""
out = out.replace('<header class="hero">\n', HERO_MEDIA, 1)
assert 'hero-media' in out

def flo(cls, img, speed, extra=''):
    return f'  <div class="flo {cls}{extra}" data-speed="{speed}" aria-hidden="true"><img src="assets/img/{img}" alt="" loading="lazy" decoding="async"></div>\n'

out = out.replace('<section id="historia">\n',
    '<section id="historia">\n' + flo('flo-corner-l', 'corner.webp', .12, ' breathe') + flo('flo-corner-r flip', 'corner.webp', .09, ' breathe')
    + flo('flo-story-l', 'orchid.webp', .18, ' breathe') + flo('flo-story-r', 'rose.webp', .15, ' breathe'), 1)
out = out.replace('<section id="detalles">\n',
    '<section id="detalles">\n' + flo('flo-vine-l', 'vine.webp', .08) + flo('flo-vine-r flip', 'vine.webp', .06)
    + flo('flo-orchid', 'orchid.webp', .16, ' breathe') + flo('flo-rose-2', 'rose.webp', .13, ' breathe'), 1)
out = out.replace('<section id="programa">\n',
    '<section id="programa">\n' + flo('flo-rose', 'rose.webp', .17, ' breathe') + flo('flo-orchid mid', 'orchid.webp', .12, ' breathe')
    + flo('flo-orchid-2', 'orchid.webp', .14, ' breathe'), 1)
out = out.replace('<section class="rsvp" id="rsvp">\n',
    '<section class="rsvp" id="rsvp">\n' + flo('flo-corner-l', 'corner.webp', .1, ' breathe') + flo('flo-corner-r flip', 'corner.webp', .13, ' breathe')
    + flo('flo-vine-r flip', 'vine.webp', .07), 1)
out = out.replace('<footer>\n', '<footer>\n  <img class="bouquet" src="assets/img/bouquet.webp" alt="" loading="lazy" decoding="async">\n', 1)
assert out.count('class="flo ') == 14, out.count('class="flo ')

# ---------- 5. JS ----------
JS = r"""
/* ---------- blue & gold edition: motion ---------- */
document.documentElement.classList.add('js');
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* hero video: pick orientation + size, fade in when ready */
  var v = document.getElementById('hero-video');
  var saveData = navigator.connection && navigator.connection.saveData;
  if(v && (reduce || saveData)){ v.remove(); v = null; }
  if(v){
    var portraitMQ = window.matchMedia('(orientation: portrait)');
    function pick(){
      var small = Math.max(window.innerWidth, window.innerHeight) < 1100 ||
                  (window.devicePixelRatio > 1.5 && window.innerWidth < 900);
      var src = 'assets/video/hero-' + (portraitMQ.matches ? 'tall' : 'wide') + (small ? '-720' : '') + '.mp4';
      if(v.getAttribute('src') !== src){
        v.classList.remove('ready');
        v.setAttribute('src', src);
        v.load();
        var p = v.play(); if(p && p.catch){ p.catch(function(){}); }
      }
    }
    v.addEventListener('playing', function(){ v.classList.add('ready'); });
    v.addEventListener('error', function(){ v.classList.remove('ready'); });
    pick();
    if(portraitMQ.addEventListener){ portraitMQ.addEventListener('change', pick); }
    else if(portraitMQ.addListener){ portraitMQ.addListener(pick); }
    document.addEventListener('visibilitychange', function(){ if(!document.hidden){ var p = v.play(); if(p && p.catch){ p.catch(function(){}); } } });
  }

  /* drifting petals */
  var layer = document.getElementById('petals');
  if(layer && !reduce){
    var kinds = ['leaf.webp','fern.webp','petal.webp','forget.webp','leaf.webp','fern.webp','forget.webp','petal.webp'];
    var mobile = window.innerWidth < 760;
    var count = mobile ? 7 : 14;
    var frag = document.createDocumentFragment();
    for(var i=0;i<count;i++){
      var kind = kinds[i % kinds.length];
      var d = document.createElement('div'); d.className = 'petal' + (kind === 'petal.webp' ? ' is-petal' : '');
      var img = document.createElement('img'); img.src = 'assets/img/' + kind; img.alt = ''; img.loading = 'lazy'; img.decoding = 'async';
      d.appendChild(img);
      var w = mobile ? 12 + Math.random()*12 : 16 + Math.random()*18;
      d.style.setProperty('--l', (Math.random()*100).toFixed(1) + 'vw');
      d.style.setProperty('--w', w.toFixed(0) + 'px');
      d.style.setProperty('--d', (22 + Math.random()*20).toFixed(1) + 's');
      d.style.setProperty('--delay', (-Math.random()*40).toFixed(1) + 's');
      d.style.setProperty('--s', (2.6 + Math.random()*2.4).toFixed(2) + 's');
      d.style.setProperty('--x', ((Math.random()-.5)*30).toFixed(1) + 'vw');
      d.style.setProperty('--r', ((Math.random()-.5)*720).toFixed(0) + 'deg');
      d.style.setProperty('--o', (0.28 + Math.random()*0.3).toFixed(2));
      frag.appendChild(d);
    }
    layer.appendChild(frag);
  }


  /* story film: plays when scrolled to, holds the page until it has played once, then loops */
  (function(){
    var v = document.getElementById('story-video'), film = document.getElementById('film');
    if(!v || !film) return;
    var tap = film.querySelector('.film-tap'), snd = film.querySelector('.film-sound'), bar = film.querySelector('.film-progress');
    var small = Math.max(window.innerWidth, window.innerHeight) < 1100;
    v.src = 'assets/video/story' + (small ? '-720' : '') + '.mp4';
    var done = false, locked = false, started = false, lockY = 0;
    var keys = {32:1,33:1,34:1,35:1,36:1,38:1,40:1};
    function prevent(e){ e.preventDefault(); }
    function keyBlock(e){ if(keys[e.keyCode]){ e.preventDefault(); } }
    function hold(){ if(Math.abs(window.scrollY - lockY) > 1){ window.scrollTo(0, lockY); } }
    function lock(){
      if(locked || done) return;
      locked = true;
      film.classList.add('locked'); document.documentElement.classList.add('film-lock');
      var r = film.getBoundingClientRect();   /* finish centring instantly, then hold there */
      lockY = Math.max(0, Math.round(window.scrollY + r.top + r.height/2 - window.innerHeight/2));
      window.scrollTo(0, lockY);
      window.addEventListener('wheel', prevent, {passive:false});
      document.addEventListener('touchmove', prevent, {passive:false});
      window.addEventListener('keydown', keyBlock);
      window.addEventListener('scroll', hold);
    }
    function unlock(){
      if(!locked) return;
      locked = false;
      film.classList.remove('locked'); document.documentElement.classList.remove('film-lock');
      window.removeEventListener('wheel', prevent); document.removeEventListener('touchmove', prevent);
      window.removeEventListener('keydown', keyBlock); window.removeEventListener('scroll', hold);
    }
    function centre(){
      var r = film.getBoundingClientRect();
      window.scrollTo({ top: window.scrollY + r.top + r.height/2 - window.innerHeight/2, behavior: 'smooth' });
    }
    function settle(fn){ /* wait until the smooth scroll has stopped moving, then lock there */
      var last = window.scrollY, ticks = 0, t0 = Date.now();
      (function poll(){
        var y = window.scrollY;
        ticks = (y === last) ? ticks + 1 : 0; last = y;
        if((ticks >= 3 && Date.now() - t0 > 450) || Date.now() - t0 > 2000){ fn(); } else { setTimeout(poll, 80); }
      })();
    }
    function begin(){
      var p = v.play();
      if(p && p.then){
        p.then(function(){ if(!reduce){ settle(lock); } })
         .catch(function(){ tap.hidden = false; });
      }else if(!reduce){ settle(lock); }
    }
    v.addEventListener('timeupdate', function(){ if(v.duration){ bar.style.width = (v.currentTime / v.duration * 100).toFixed(1) + '%'; } });
    v.addEventListener('ended', function(){
      done = true; film.classList.add('done'); unlock();
      v.loop = true; var p = v.play(); if(p && p.catch){ p.catch(function(){}); }
    });
    v.addEventListener('error', unlock);
    v.addEventListener('stalled', function(){ setTimeout(function(){ if(v.readyState < 3 && v.paused){ unlock(); } }, 4000); });
    tap.addEventListener('click', function(){ tap.hidden = true; v.muted = false; snd.setAttribute('aria-pressed', 'true'); centre(); begin(); });
    snd.addEventListener('click', function(){
      v.muted = !v.muted; snd.setAttribute('aria-pressed', String(!v.muted));
      if(v.paused){ var p = v.play(); if(p && p.catch){ p.catch(function(){}); } }
    });
    if('IntersectionObserver' in window){
      var fio = new IntersectionObserver(function(entries){
        entries.forEach(function(e){
          if(e.isIntersecting && !started){ started = true; fio.disconnect(); centre(); begin(); }
        });
      }, { threshold: 0.55 });
      fio.observe(film);
    }else{ started = true; v.controls = true; }
  })();

  /* scroll reveal */
  var sel = '.sec-title,.sec-script,.diamond,.story-copy,.photo,.ornament,.detail,.maps-h,.maps-sub,.venue,.hop,.program li,.faq h3,details,.tags,.deadline,.field,.btn,.formnote,footer p';
  var items = Array.prototype.slice.call(document.querySelectorAll(sel));
  items.forEach(function(el){
    el.classList.add('rv');
    var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
    el.style.transitionDelay = ((sib % 6) * 80) + 'ms';
  });
  var revealables = items.concat(Array.prototype.slice.call(document.querySelectorAll('.flo,.bouquet')));
  if('IntersectionObserver' in window && !reduce){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function(el){ io.observe(el); });
  }else{
    revealables.forEach(function(el){ el.classList.add('in'); });
  }

  /* parallax florals */
  var px = Array.prototype.slice.call(document.querySelectorAll('.flo[data-speed]'));
  if(px.length && !reduce){
    var ticking = false;
    function update(){
      ticking = false;
      var vh = window.innerHeight;
      px.forEach(function(el){
        var r = el.parentElement.getBoundingClientRect();
        if(r.bottom < -vh || r.top > vh*2) return;
        /* drift relative to the bloom's own resting position, so tall sections never fling it far */
        var centre = r.top + el.offsetTop + el.offsetHeight/2 - vh/2;
        var off = Math.max(-140, Math.min(140, -centre * parseFloat(el.getAttribute('data-speed'))));
        el.style.setProperty('--py', off.toFixed(1) + 'px');
      });
    }
    function onScroll(){ if(!ticking){ ticking = true; requestAnimationFrame(update); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }
})();
"""
marker = '</script>\n</body>'
assert marker in out
out = out.replace(marker, JS + marker, 1)

open('index.html', 'w', encoding='utf-8', newline='\n').write(out)
print('written index.html', len(out))
