# -*- coding: utf-8 -*-
"""마사지고 정적 사이트 생성기 — 순수 HTML + 인라인 CSS/JS, 의존성 0."""

import os, json, html, datetime
from data import (SITE, OPS, TEAM, SERVICES, THERAPISTS, MAGAZINE, FAQ_MAIN,
                  REVIEWS_MAIN, REGIONS, arrival_minutes, district_rating,
                  district_review_count, district_reviews)
from content import (SERVICE_SECTIONS, SERVICE_EXTRA, THERAPIST_SECTIONS,
                     THERAPIST_DEEP, THERAPIST_COMMON, THERAPIST_EXTRA, METRO_SECTIONS)

def prose_section(heading, paras, eyebrow=None):
    eb = f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    ps = "".join(f"<p>{esc(p)}</p>" for p in paras)
    return f'<section class="wrap tight">{eb}<h2>{esc(heading)}</h2><div class="prose" style="margin-top:16px;max-width:680px">{ps}</div></section>'

def notes_section(heading, sections, eyebrow=None, start=1):
    eb = f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    nh = "".join(note(i, h, p) for i, (h, p) in enumerate(sections, start))
    return f'<section class="wrap tight">{eb}<h2>{esc(heading)}</h2><div class="notes" style="margin-top:24px">{nh}</div></section>'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = SITE["domain"]
NOW = datetime.date.today().isoformat()

# 저자 슬러그
AUTHOR_SLUG = {"김세영": "kim-seyeong", "박지연": "park-jiyeon", "이도현": "lee-dohyeon"}
AUTHORS = {t["name"]: t for t in TEAM}

def esc(s): return html.escape(str(s), quote=True)
def url(path): return D + path

# ─────────────────────────────────────────────────────────────
# CSS (인라인) — 디자인 시스템
# ─────────────────────────────────────────────────────────────
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
--bg:#0b0b0e;--surface:#13131a;--surface-2:#1a1a23;--line:rgba(255,255,255,.08);
--text:#f3f3f5;--muted:#9a9aa3;--dim:#6c6c75;
--gold:#d6b274;--rose:#e9b8a7;--copper:#c98a6b;
--grad:linear-gradient(135deg,#f4d29c 0%,#e9b8a7 45%,#c98a6b 100%);
--grad-soft:linear-gradient(135deg,rgba(244,210,156,.14),rgba(201,138,107,.06));
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);line-height:1.65;letter-spacing:-.01em;
font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.serif,.note-num,.step .n{font-family:"Cormorant Garamond","Noto Serif KR",Georgia,serif;font-weight:300;font-style:italic}
.grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.wrap{max-width:1240px;margin:0 auto;padding:120px 24px}
section.tight{padding:84px 24px}
h1{font-weight:800;letter-spacing:-.038em;line-height:1.08;font-size:clamp(38px,6.5vw,72px)}
h2{font-weight:800;letter-spacing:-.03em;font-size:clamp(26px,4vw,44px);margin-bottom:14px}
h3{font-weight:800;font-size:20px}
p{color:#c8c8d0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11.5px;letter-spacing:.2em;
text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:18px}
.pulse{width:8px;height:8px;border-radius:50%;background:var(--rose);box-shadow:0 0 0 0 rgba(233,184,167,.7);animation:pulse 2s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 10px rgba(233,184,167,0)}100%{box-shadow:0 0 0 0 rgba(233,184,167,0)}}
.lead{font-size:clamp(15px,1.6vw,17px);color:var(--muted);max-width:560px;margin-top:18px}
.label{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--dim);font-weight:700}
/* header */
header{position:sticky;top:0;z-index:100;background:rgba(11,11,14,.82);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav{max-width:1240px;margin:0 auto;display:flex;align-items:center;gap:18px;padding:14px 24px}
.brand{font-weight:800;font-size:22px;letter-spacing:-.03em;display:flex;align-items:center;gap:8px}
.brand .dot{width:9px;height:9px;border-radius:50%;background:var(--grad)}
.menu{list-style:none;display:flex;align-items:center;gap:6px;margin-left:auto}
.menu>li{position:relative}
.menu>li>a{display:block;padding:10px 13px;font-size:14px;color:var(--muted);border-radius:10px;font-weight:600;transition:.2s}
.menu>li>a:hover{color:var(--text);background:rgba(255,255,255,.04)}
.submenu{list-style:none;position:absolute;top:100%;left:0;min-width:190px;background:var(--surface);
border:1px solid var(--line);border-radius:14px;padding:8px;opacity:0;visibility:hidden;transform:translateY(8px);
transition:.22s;box-shadow:0 20px 50px rgba(0,0,0,.45)}
.menu>li:hover .submenu,.menu>li.open .submenu{opacity:1;visibility:visible;transform:translateY(6px)}
.submenu a{display:block;padding:9px 12px;font-size:13.5px;color:var(--muted);border-radius:9px}
.submenu a:hover{color:var(--text);background:rgba(255,255,255,.05)}
.cta-pill{background:var(--grad)!important;color:#1a1208!important;font-weight:800!important;border-radius:999px;padding:10px 18px!important}
.toggle{display:none;margin-left:auto;background:none;border:1px solid var(--line);color:var(--text);
font-size:20px;width:44px;height:44px;border-radius:12px;cursor:pointer}
/* hero */
.hero{position:relative;overflow:hidden;border-bottom:1px solid var(--line)}
.hero::before{content:"";position:absolute;inset:0;z-index:0;
background:radial-gradient(800px 500px at 80% -10%,rgba(244,210,156,.14),transparent 60%),
radial-gradient(700px 500px at 0% 20%,rgba(201,138,107,.10),transparent 55%),
radial-gradient(600px 600px at 60% 110%,rgba(233,184,167,.08),transparent 60%)}
.hero-inner{position:relative;z-index:1;max-width:1240px;margin:0 auto;padding:96px 24px 104px;
display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.hero h1{margin:6px 0 0}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:14px 22px;border-radius:12px;font-weight:700;font-size:14.5px;transition:.25s;border:1px solid transparent}
.btn-primary{background:var(--grad);color:#1a1208;box-shadow:0 12px 30px rgba(201,138,107,.28)}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 18px 40px rgba(201,138,107,.4)}
.btn-ghost{border-color:var(--line);color:var(--text)}
.btn-ghost:hover{border-color:rgba(244,210,156,.4);transform:translateY(-2px)}
.trust{margin-top:28px;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:13px;color:var(--muted)}
.trust b{color:var(--gold)}
.hero-visual{position:relative;min-height:340px}
.glass{position:relative;z-index:2;background:rgba(20,20,28,.6);backdrop-filter:blur(20px);
border:1px solid rgba(244,210,156,.22);border-radius:22px;padding:26px;transform:rotate(2deg)}
.glass h3{font-size:18px;margin-bottom:16px}
.glass h3 small{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:6px}
.book-row{display:flex;justify-content:space-between;padding:11px 0;border-top:1px solid var(--line);font-size:13.5px}
.book-row span:first-child{color:var(--dim)}
.bk{display:block;text-align:center;margin-top:16px;background:var(--grad);color:#1a1208;font-weight:800;padding:12px;border-radius:12px}
.floating{position:absolute;z-index:3;background:var(--surface);border:1px solid var(--line);border-radius:14px;
padding:11px 15px;font-size:12px;color:var(--muted);box-shadow:0 14px 34px rgba(0,0,0,.4)}
.floating b{color:var(--text)}
.fl-1{top:-8px;left:-18px;transform:rotate(-4deg)}
.fl-2{bottom:-12px;right:-10px;transform:rotate(3deg)}
/* marquee */
.marquee{overflow:hidden;border-bottom:1px solid var(--line);background:var(--surface);white-space:nowrap}
.marquee-track{display:inline-flex;gap:34px;padding:14px 0;animation:scroll 38s linear infinite}
.marquee-track span{font-size:13px;letter-spacing:.06em;color:var(--muted)}
.marquee-track span::before{content:"·";margin-right:34px;color:var(--copper)}
@keyframes scroll{to{transform:translateX(-50%)}}
/* grids */
.grid{display:grid;gap:18px}
.g4{grid-template-columns:repeat(4,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
.card{background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);
border-radius:18px;padding:24px;transition:.3s}
.card:hover{transform:translateY(-4px);border-color:rgba(244,210,156,.28);box-shadow:0 18px 44px rgba(0,0,0,.3)}
.card .kicker{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:10px}
.card h3{margin-bottom:8px}
.card p{font-size:14px;color:var(--muted)}
.card .more{display:inline-block;margin-top:14px;font-size:13px;color:var(--gold);font-weight:700}
.card:hover .more{}
/* note cards */
.notes{display:flex;flex-direction:column;gap:16px}
.note-card{display:flex;gap:24px;padding:26px 28px;border-radius:18px;
background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);
transition:.3s;overflow:hidden;position:relative}
.note-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--grad);opacity:0;transition:.3s}
.note-card:hover::before{opacity:1}
.note-card:hover{transform:translateY(-2px);box-shadow:0 18px 44px rgba(0,0,0,.32);border-color:rgba(244,210,156,.28)}
.note-num{font-size:46px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1;flex-shrink:0}
.note-title{font-size:19px;margin-bottom:10px}
.note-text{max-width:660px}
.note-text p{margin:0 0 10px;color:#c8c8d0;font-size:14.5px;line-height:1.78}
/* price */
.price-card{position:relative;background:linear-gradient(135deg,var(--surface),var(--surface-2));
border:1px solid var(--line);border-radius:18px;padding:24px;overflow:hidden;transition:.3s}
.price-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--grad);opacity:.5}
.price-card:hover{transform:translateY(-3px);border-color:rgba(244,210,156,.3)}
.price-card.best{border-color:rgba(244,210,156,.4)}
.best-badge{position:absolute;top:14px;right:14px;background:var(--grad);color:#1a1208;font-size:10px;font-weight:800;letter-spacing:.1em;padding:4px 9px;border-radius:999px}
.price-card .kicker{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:8px}
.price-card p{font-size:13.5px;color:var(--muted);margin:6px 0 14px}
.time-rows>div{display:flex;justify-content:space-between;padding:9px 0;border-top:1px solid var(--line);font-size:14px}
.time-rows span:last-child{font-weight:700;color:var(--text)}
/* chips */
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.chip{display:flex;flex-direction:column;gap:2px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.chip .k{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);font-weight:700}
.chip .v{font-size:16px;font-weight:800}
.chip .v.grad{font-family:inherit}
/* faq */
details{background:var(--surface);border:1px solid var(--line);border-radius:14px;margin-bottom:10px;overflow:hidden}
summary{list-style:none;cursor:pointer;padding:18px 22px;font-weight:700;font-size:15px;display:flex;justify-content:space-between;align-items:center}
summary::-webkit-details-marker{display:none}
summary span{color:var(--gold);font-size:22px;transition:.2s}
details[open] summary span{transform:rotate(45deg)}
details>div{padding:0 22px 20px;color:var(--muted);font-size:14.5px;line-height:1.78}
/* reviews */
.review{background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);border-radius:18px;padding:22px}
.review .stars{color:var(--gold);font-size:14px;letter-spacing:2px}
.review p{font-size:14.5px;margin:12px 0;line-height:1.7}
.review .who{font-size:12.5px;color:var(--dim)}
.review .who b{color:var(--muted)}
/* steps */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.step{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:24px}
.step .n{font-size:40px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.step h3{font-size:17px;margin:8px 0}
.step p{font-size:13.5px;color:var(--muted)}
/* data box */
.databox{background:var(--grad-soft);border:1px solid rgba(244,210,156,.2);border-radius:18px;padding:26px 28px}
.databox h3{margin-bottom:10px}
.databox p{font-size:14px;color:var(--muted);margin-bottom:6px}
/* cta band */
.cta-band{text-align:center;background:var(--grad-soft);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.cta-band .wrap{padding:96px 24px}
/* breadcrumb */
.crumb{font-size:12.5px;color:var(--dim);margin-bottom:18px}
.crumb a{color:var(--muted)}
.crumb a:hover{color:var(--gold)}
/* byline (E-E-A-T) */
.byline{display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px;margin:18px 0 4px;padding:14px 16px;
border:1px solid var(--line);border-radius:12px;background:var(--surface);font-size:13px;color:var(--muted)}
.byline .av{width:30px;height:30px;border-radius:50%;background:var(--grad);flex-shrink:0}
.byline a{color:var(--gold);font-weight:700}
.byline .sep{color:var(--dim)}
.byline .upd{color:var(--dim);font-size:12px}
/* references (외부 인용) */
.refs{border:1px solid var(--line);border-radius:14px;padding:22px 24px;background:var(--surface)}
.refs h3{font-size:15px;margin-bottom:12px}
.refs ul{list-style:none}
.refs li{padding:7px 0;border-top:1px solid var(--line);font-size:13.5px;color:var(--muted)}
.refs li:first-child{border-top:none}
.refs a{color:var(--gold)}
.refs .ext::after{content:"↗";font-size:11px;margin-left:4px;color:var(--dim)}
/* toc */
.toc{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 22px;margin:24px 0}
.toc .label{margin-bottom:10px;display:block}
.toc a{display:block;padding:6px 0;font-size:14px;color:var(--muted)}
.toc a:hover{color:var(--gold)}
/* link list */
.linklist{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:22px}
.linklist a{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:13px 16px;font-size:14px;color:var(--muted);transition:.2s}
.linklist a:hover{color:var(--text);border-color:rgba(244,210,156,.3);transform:translateY(-2px)}
.prose p{margin:0 0 14px;font-size:15px;line-height:1.85;color:#c8c8d0}
.prose h2{margin-top:40px}
/* footer */
.site-footer{border-top:1px solid var(--line);background:#08080b}
.footer-wrap{max-width:1240px;margin:0 auto;padding:72px 24px 40px}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px}
.footer-grid h4{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-bottom:14px}
.footer-grid a,.footer-grid p{display:block;font-size:13.5px;color:var(--muted);margin-bottom:9px}
.footer-grid a:hover{color:var(--text)}
.footer-ops{margin:40px 0;padding:22px;border-radius:16px;background:var(--grad-soft);border:1px solid rgba(244,210,156,.18);
display:flex;flex-wrap:wrap;gap:10px 32px;align-items:center}
.footer-ops .k{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);font-weight:700}
.footer-ops .v{font-size:15px;font-weight:700}
.footer-ops a.phone{font-size:20px;font-weight:800;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.company-info{display:grid;grid-template-columns:repeat(3,1fr);gap:12px 24px;padding:24px 0;border-top:1px solid var(--line);font-size:12.5px;color:var(--dim)}
.company-info b{color:var(--muted);font-weight:600}
.footer-policies{display:flex;flex-wrap:wrap;gap:16px;padding:18px 0;border-top:1px solid var(--line)}
.footer-policies a{font-size:12.5px;color:var(--muted)}
.footer-policies a:hover{color:var(--gold)}
.footer-bottom{padding-top:18px;border-top:1px solid var(--line);font-size:12px;color:var(--dim);line-height:1.7}
/* reveal */
.reveal{opacity:0;transform:translateY(20px);transition:.8s}
.reveal.in{opacity:1;transform:none}
/* perf */
#region,#process,#reviews,#about,#faq,.cta-band,.site-footer{content-visibility:auto;contain-intrinsic-size:auto 700px}
.card,.reg,.step,.review,.note-card,.price-card{contain:layout style}
@media(hover:none){.glass,.floating{backdrop-filter:none!important}}
@media(prefers-reduced-motion:reduce){.marquee-track,.pulse{animation:none!important}.reveal{opacity:1!important;transform:none!important}}
/* responsive */
@media(max-width:1100px){
.toggle{display:block}
.menu{position:fixed;top:64px;right:0;bottom:0;width:min(86vw,320px);flex-direction:column;align-items:stretch;
background:var(--surface);border-left:1px solid var(--line);padding:18px;gap:2px;transform:translateX(100%);transition:.3s;overflow:auto}
.menu.open{transform:none}
.menu>li>a{padding:13px}
.submenu{position:static;opacity:1;visibility:visible;transform:none;box-shadow:none;border:none;background:transparent;padding:0 0 8px 12px;display:none}
.menu>li.open .submenu{display:block}
.hero-inner{grid-template-columns:1fr;gap:40px}
.hero-visual{min-height:300px}
.g4{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(2,1fr)}
.steps{grid-template-columns:repeat(2,1fr)}
.footer-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:680px){
.wrap{padding:80px 18px}
.g4,.g3,.g2,.steps,.company-info{grid-template-columns:1fr}
.note-card{flex-direction:column;gap:8px}
.footer-grid{grid-template-columns:1fr}
.hero-inner{padding:64px 18px 80px}
}
"""

JS = """
(function(){
function idle(fn){if('requestIdleCallback'in window){requestIdleCallback(fn,{timeout:1500})}else{setTimeout(fn,1)}}
// mobile toggle
var t=document.querySelector('.toggle'),m=document.getElementById('primary-menu');
if(t&&m){t.addEventListener('click',function(){var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o)})}
idle(function(){
// dropdown click (mobile) + ESC + outside
var items=document.querySelectorAll('.menu>li');
items.forEach(function(li){
var sub=li.querySelector('.submenu');if(!sub)return;
var a=li.querySelector('a');
a.addEventListener('click',function(e){if(window.innerWidth<=1100){e.preventDefault();li.classList.toggle('open')}});
});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){items.forEach(function(li){li.classList.remove('open')});if(m){m.classList.remove('open')}}});
document.addEventListener('click',function(e){if(!e.target.closest('.menu')&&!e.target.closest('.toggle')){items.forEach(function(li){li.classList.remove('open')})}});
// reveal
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'80px'});
document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
});
})();
"""

# ─────────────────────────────────────────────────────────────
# 공통 조각
# ─────────────────────────────────────────────────────────────
def header():
    svc = "".join(f'<li><a href="/service/{s["slug"]}/">{s["ko"]}</a></li>' for s in SERVICES)
    locs = "".join(f'<li><a href="/locations/{k}/">{v["ko"]}</a></li>' for k, v in REGIONS.items())
    ther = "".join(f'<li><a href="/therapists/{t["slug"]}/">{t["ko"]}</a></li>' for t in THERAPISTS)
    return f"""<header><nav class="nav" aria-label="주 메뉴">
<a class="brand" href="/" aria-label="마사지고 홈"><span class="dot"></span>{SITE['brand']}</a>
<button class="toggle" aria-expanded="false" aria-controls="primary-menu">☰</button>
<ul id="primary-menu" class="menu">
<li><a href="/service/" aria-haspopup="true">서비스</a><ul class="submenu">{svc}</ul></li>
<li><a href="/locations/" aria-haspopup="true">지역</a><ul class="submenu">{locs}</ul></li>
<li><a href="/therapists/" aria-haspopup="true">관리사</a><ul class="submenu">{ther}</ul></li>
<li><a href="/pricing/">요금</a></li>
<li><a href="/magazine/">매거진</a></li>
<li><a href="/reviews/">후기</a></li>
<li><a class="cta-pill" href="{SITE['phone_href']}">{SITE['phone']}</a></li>
</ul></nav></header>"""

def footer():
    svc = "".join(f'<a href="/service/{s["slug"]}/">{s["ko"]}</a>' for s in SERVICES)
    locs = "".join(f'<a href="/locations/{k}/">{v["ko"]} 출장마사지</a>' for k, v in REGIONS.items())
    return f"""<footer class="site-footer"><div class="footer-wrap">
<div class="footer-grid">
<div>
<div class="brand" style="margin-bottom:14px"><span class="dot"></span>{SITE['brand']}</div>
<p>{esc(SITE['tagline'])}</p>
<p style="margin-top:10px">건강관리를 위한 이완 서비스이며 의료 행위가 아닙니다.</p>
</div>
<div><h4>서비스</h4>{svc}</div>
<div><h4>지역</h4>{locs}</div>
<div><h4>안내</h4>
<a href="/about/">회사 소개</a><a href="/contact/">연락처</a>
<a href="/editorial-policy/">편집 정책</a><a href="/pricing/">요금</a>
<a href="/magazine/">매거진</a><a href="/reviews/">후기</a></div>
</div>
<div class="footer-ops">
<span class="k">고객센터</span><a class="phone" href="{SITE['phone_href']}">{SITE['phone']}</a>
<span class="k">운영시간</span><span class="v">{esc(SITE['hours'])}</span>
<span class="k">이메일</span><span class="v">{esc(SITE['email'])}</span>
</div>
<div class="company-info">
<span><b>회사명</b> {esc(SITE['company'])}</span>
<span><b>대표자</b> {esc(SITE['ceo'])}</span>
<span><b>사업자등록번호</b> {esc(SITE['biz_no'])}</span>
<span><b>주소</b> {esc(SITE['address'])}</span>
<span><b>통신판매업신고</b> {esc(SITE['mail_order_no'])}</span>
<span><b>개인정보보호책임자</b> {esc(SITE['privacy_officer'])}</span>
</div>
<div class="footer-policies">
<a href="/policy/privacy/">개인정보처리방침</a>
<a href="/policy/terms/">이용약관</a>
<a href="/policy/youth/">청소년보호정책</a>
<a href="/about/">회사 소개</a>
<a href="/editorial-policy/">편집 정책</a>
<a href="/contact/">연락처</a>
</div>
<div class="footer-bottom">
19세 이상 이용 가능 · 본 서비스는 건강관리를 위한 이완 서비스이며 의료 행위가 아닙니다.<br>
© {datetime.date.today().year} {esc(SITE['company'])}. All rights reserved.
</div>
</div></footer>"""

def page(title, desc, path, body, jsonld=None, og_image=None):
    canonical = url(path)
    ogimg = og_image or url("/assets/og-cover.jpg")
    blocks = ""
    if jsonld:
        if isinstance(jsonld, dict): jsonld = [jsonld]
        for obj in jsonld:
            blocks += f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'
    return f"""<!doctype html><html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b0b0e">
<meta name="format-detection" content="telephone=no">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="googlebot" content="index,follow">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(SITE['author'])}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ko-KR" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['brand'])}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{ogimg}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<style>{CSS}</style>
{blocks}
</head><body>
{header()}
<main>{body}</main>
{footer()}
<script>{JS}</script>
</body></html>"""

def write(path, content):
    fp = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

# 컴포넌트 헬퍼
def note(n, title, paras):
    ps = "".join(f"<p>{esc(p)}</p>" for p in paras)
    return f'<div class="note-card reveal"><div class="note-num">{n:02d}</div><div><h3 class="note-title">{esc(title)}</h3><div class="note-text">{ps}</div></div></div>'

def price_card(s):
    rows = "".join(f"<div><span>{t}</span><span>{p}</span></div>" for t, p in s["prices"])
    badge = '<span class="best-badge">BEST</span>' if s.get("best") else ""
    return f'<div class="price-card{" best" if s.get("best") else ""} reveal">{badge}<div class="kicker">{esc(s["kicker"])}</div><h3>{esc(s["ko"])}</h3><p>{esc(s["summary"])}</p><div class="time-rows">{rows}</div></div>'

def faq_block(items):
    out = '<div>'
    for q, a in items:
        out += f'<details><summary>{esc(q)}<span>+</span></summary><div>{esc(a)}</div></details>'
    return out + '</div>'

def crumb(parts):
    # parts: list of (label, href or None)
    out = []
    for label, href in parts:
        if href: out.append(f'<a href="{href}">{esc(label)}</a>')
        else: out.append(esc(label))
    return '<div class="crumb">' + ' › '.join(out) + '</div>'

def breadcrumb_jsonld(parts):
    items = []
    for i, (label, href) in enumerate(parts, 1):
        el = {"@type": "ListItem", "position": i, "name": label}
        if href: el["item"] = url(href)
        items.append(el)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def faq_jsonld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def cta_band():
    return f"""<section class="cta-band" id="cta"><div class="wrap reveal">
<span class="eyebrow"><span class="pulse"></span>RESERVE TONIGHT</span>
<h2>지금, 당신의 공간으로 부르세요</h2>
<p class="lead" style="margin:14px auto 0">전화 한 통이면 가까운 매니저가 출발합니다. {esc(SITE['hours'])}.</p>
<div class="actions" style="justify-content:center"><a class="btn btn-primary" href="{SITE['phone_href']}">{SITE['phone']} 예약하기 →</a></div>
</div></section>"""

def byline(author="김세영", reviewer="박지연", updated=None):
    a = AUTHORS[author]; r = AUTHORS[reviewer]
    upd = updated or NOW
    return (f'<div class="byline"><span class="av" aria-hidden="true"></span>'
            f'<span>글 <a href="/authors/{AUTHOR_SLUG[author]}/">{esc(author)}</a> · {esc(a["role"])}</span>'
            f'<span class="sep">·</span>'
            f'<span>감수 <a href="/authors/{AUTHOR_SLUG[reviewer]}/">{esc(reviewer)}</a> · {esc(r["role"])}</span>'
            f'<span class="sep">·</span><span class="upd">최종 업데이트 {upd}</span></div>')

# 외부 신뢰 신호 — 실재하는 공공기관/공식 도메인 루트만 인용(딥링크 미사용)
REFERENCES = [
    ("통신판매사업자 정보 공개 확인", "공정거래위원회", "https://www.ftc.go.kr"),
    ("관련 법령 원문 (공중위생관리법 등)", "국가법령정보센터", "https://www.law.go.kr"),
    ("스포츠마사지·생활체육 자격 안내", "국민체육진흥공단(KSPO)", "https://www.kspo.or.kr"),
    ("소비자 분쟁·피해구제 안내", "한국소비자원", "https://www.kca.go.kr"),
]
def references_block(extra_internal=None):
    items = "".join(
        f'<li><a class="ext" href="{u}" target="_blank" rel="nofollow noopener">{esc(t)}</a> — {esc(org)}</li>'
        for t, org, u in REFERENCES)
    internal_block = ""
    if extra_internal:
        lis = "".join(f'<li><a href="{href}">{esc(label)}</a></li>' for label, href in extra_internal)
        internal_block = f'<h3 style="margin-top:16px">관련 안내</h3><ul>{lis}</ul>'
    return (f'<section class="wrap tight"><span class="eyebrow">REFERENCES · 참고 자료</span>'
            f'<h2>출처 및 참고 자료</h2>'
            f'<p class="lead">아래는 본 안내의 근거가 되는 공공기관·법령 정보입니다. 운영 수치는 마사지고 본사 1차 배차 로그에 근거합니다.</p>'
            f'<div class="refs" style="margin-top:18px"><h3>외부 공식 자료</h3><ul>{items}</ul>{internal_block}</div></section>')

def webpage_jsonld(path, title, desc, author="김세영", reviewer="박지연",
                   published="2026-01-05", typ="WebPage", about=None):
    obj = {
        "@context": "https://schema.org", "@type": typ,
        "name": title, "description": desc, "url": url(path), "inLanguage": "ko-KR",
        "isPartOf": {"@id": url("/#website")},
        "datePublished": published, "dateModified": NOW,
        "primaryImageOfPage": {"@type": "ImageObject", "url": url("/assets/og-cover.jpg"),
                               "width": 1200, "height": 630},
        "author": {"@type": "Person", "name": author, "jobTitle": AUTHORS[author]["role"],
                   "url": url(f"/authors/{AUTHOR_SLUG[author]}/")},
        "reviewedBy": {"@type": "Person", "name": reviewer, "jobTitle": AUTHORS[reviewer]["role"],
                       "url": url(f"/authors/{AUTHOR_SLUG[reviewer]}/")},
        "publisher": {"@id": url("/#org")},
        "citation": [{"@type": "CreativeWork", "name": f"{org} — {t}", "url": u} for t, org, u in REFERENCES],
    }
    if about: obj["about"] = about
    return obj

ORG_JSONLD = {
    "@context": "https://schema.org", "@type": "Organization",
    "@id": url("/#org"), "name": SITE["brand"], "legalName": SITE["company"],
    "url": D, "telephone": SITE["phone_intl"], "email": SITE["email"],
    "logo": url("/assets/logo.png"), "image": url("/assets/og-cover.jpg"),
    "description": SITE["tagline"], "taxID": SITE["biz_no"],
    "founder": {"@type": "Person", "name": SITE["ceo"]},
    "address": {"@type": "PostalAddress", "addressCountry": "KR", "addressRegion": "경기도",
                "addressLocality": "파주시", "streetAddress": "청석로 268"},
    "contactPoint": {"@type": "ContactPoint", "telephone": SITE["phone_intl"], "contactType": "reservations",
                     "availableLanguage": ["ko", "en", "zh", "ja"]},
}

# ─────────────────────────────────────────────────────────────
# 페이지 빌더
# ─────────────────────────────────────────────────────────────
def build_home():
    svc_cards = "".join(
        f'<a class="card reveal" href="/service/{s["slug"]}/"><div class="kicker">{esc(s["kicker"])}</div>'
        f'<h3>{esc(s["ko"])}</h3><p>{esc(s["summary"])}</p><span class="more">자세히 →</span></a>'
        for s in SERVICES)
    reg_cards = "".join(
        f'<a class="card reveal" href="/locations/{k}/"><div class="kicker">{esc(v["en"]).upper()}</div>'
        f'<h3>{esc(v["ko"])} 출장마사지</h3><p>{esc(v["intro"])}</p><span class="more">{len(v["districts"])}개 지역 →</span></a>'
        for k, v in REGIONS.items())
    steps = [("상담·예약", "전화로 지역·코스·시간을 말씀하세요. 디스패처가 가까운 매니저를 배정합니다."),
             ("출발 안내", "매니저 출발 시 안내드리고, 도착 전 한 번 더 연락드립니다."),
             ("관리 진행", "압의 세기는 언제든 조절 가능합니다. 편안하게 받으세요."),
             ("마무리", "관리 시작 전 안내된 금액으로 결제합니다. 추가 비용은 없습니다.")]
    step_html = "".join(f'<div class="step reveal"><div class="n">{i:02d}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
                        for i, (t, d) in enumerate(steps, 1))
    rev_html = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*r["stars"]}</div><p>{esc(r["text"])}</p>'
        f'<div class="who"><b>{esc(r["name"])}</b> · {esc(r["area"])} · {esc(r["course"])}</div></div>'
        for r in REVIEWS_MAIN)
    team_html = "".join(
        f'<div class="card reveal"><div class="kicker">{esc(t["role"])}</div>'
        f'<h3><a href="/authors/{AUTHOR_SLUG[t["name"]]}/">{esc(t["name"])}</a></h3><p>{esc(t["bio"])}</p></div>'
        for t in TEAM)
    notes = [
        ("운영 주체 (Who)", ["마사지고는 본사 디스패처가 직접 매니저를 배정하는 출장마사지 운영팀입니다.",
                          f"서울·경기·인천·부산 4개 광역권, 총 {sum(len(v['districts']) for v in REGIONS.values())}개 행정구를 담당합니다.",
                          "운영팀장과 안전 자문 트레이너의 실명·책임 영역을 공개합니다."]),
        ("운영 방식 (How)", ["전화 접수 → 가까운 매니저 배정 → 출발·도착 안내 → 관리 → 사전 안내 금액 결제 순으로 진행합니다.",
                          "압의 세기는 시술 중 언제든 조절하며, 불편하면 즉시 중단할 수 있습니다."]),
        ("운영 이유 (Why)", ["이동·대기 없이 익숙한 공간에서 받는 휴식의 가치를 믿습니다.",
                          "방문업소 대비 동선 부담이 없어 늦은 시간에도 부담이 적습니다."]),
        ("안전 가이드", ["모든 매니저는 본사 등록 절차와 자문 트레이너 기본 교육을 이수합니다.",
                     "박지연 자문 트레이너(KSPO 스포츠마사지·재활케어 8년)가 강압 회피 가이드를 감수합니다."]),
        ("편집 정책", ["후기는 실제 이용 고객의 작성분만 게시하며 운영 로그와 대조해 검증합니다.",
                    "콘텐츠는 운영팀이 작성하고 자문 트레이너가 감수합니다. 자세한 기준은 편집 정책 페이지에 공개합니다."]),
    ]
    note_html = "".join(note(i, t, p) for i, (t, p) in enumerate(notes, 1))

    body = f"""
<section class="hero"><div class="hero-inner">
<div class="hero-copy reveal">
<span class="eyebrow"><span class="pulse"></span>출장마사지 · 연중무휴</span>
<h1>당신의 공간에<br>도착하는 <span class="grad">최상의</span><br><span class="serif">휴식 한 시간.</span></h1>
<p class="lead">전화 한 통이면 가까운 매니저가 출발합니다. 서울 기준 평균 {OPS['avg_arrival']}분, 사전 안내 금액 외 추가 비용은 없습니다.</p>
<div class="actions"><a class="btn btn-primary" href="{SITE['phone_href']}">{SITE['phone']} 예약 →</a><a class="btn btn-ghost" href="/service/">코스 둘러보기</a></div>
<div class="trust">★★★★★ <b>{OPS['rating']}</b> · 후기 {OPS['review_count']:,}건 · {esc(SITE['hours'])} · 평균 도착 <b>{OPS['avg_arrival']}분</b></div>
</div>
<div class="hero-visual">
<div class="floating fl-1">LIVE BOOKING · 5분 전 예약</div>
<div class="glass"><h3><small>시그니처 코스</small>아로마 딥 릴렉스 90분</h3>
<div class="book-row"><span>관리사</span><span>한국 · 여성</span></div>
<div class="book-row"><span>예상 도착</span><span>약 {OPS['avg_arrival']}분</span></div>
<div class="book-row"><span>금액</span><span>120,000원</span></div>
<a class="bk" href="{SITE['phone_href']}">전화 예약 →</a></div>
<div class="floating fl-2">CUSTOMER RATING · ★{OPS['rating']}</div>
</div></div></section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">
{"".join(f"<span>{v['ko']} {len(v['districts'])}개 지역</span>" for v in REGIONS.values())*2}
{"".join(f"<span>{s['ko']}</span>" for s in SERVICES)*2}
</div></div>

<section class="wrap" id="services"><span class="eyebrow">SIGNATURE SERVICES</span><h2>다섯 가지 시그니처 코스</h2>
<p class="lead">오늘의 컨디션에 맞춰 고르세요. 무엇을 고를지 모르겠다면 상담 중 함께 정해 드립니다.</p>
<div class="grid g4" style="margin-top:34px">{svc_cards}</div></section>

<section class="wrap tight" id="region"><span class="eyebrow">SERVICE AREA</span><h2>전 권역 출장 가능</h2>
<div class="grid g4" style="margin-top:30px">{reg_cards}</div></section>

<section class="wrap tight" id="process"><span class="eyebrow">HOW IT WORKS</span><h2>예약부터 마무리까지 네 단계</h2>
<div class="steps" style="margin-top:30px">{step_html}</div></section>

<section class="wrap tight" id="reviews"><span class="eyebrow">CLIENT VOICES</span><h2>고객의 목소리</h2>
<div class="grid g3" style="margin-top:30px">{rev_html}</div>
<div style="margin-top:24px"><a class="btn btn-ghost" href="/reviews/">후기 더 보기 →</a></div></section>

<section class="wrap tight" id="about"><span class="eyebrow">WHO · HOW · WHY</span><h2>누가, 어떻게, 왜 운영하는가</h2>
<p class="lead">'누가, 어떻게, 왜 만들었는가' 원칙에 따라 운영 주체와 방식, 이유를 투명하게 공개합니다.</p>
{byline(author="김세영", reviewer="박지연")}
<div class="grid g3" style="margin:30px 0">{team_html}</div>
<div class="notes">{note_html}</div>
<div class="databox reveal" style="margin-top:24px"><h3>Data &amp; Methodology</h3>
<p>아래 수치는 마사지고 본사 배차 시스템의 1차 운영 로그를 집계한 값입니다.</p>
<p>· 집계 기간: 최근 {OPS['months']}개월 · 총 배차 {OPS['dispatch_total']:,}건</p>
<p>· 권역별: 서울 {OPS['by_region']['서울']:,} · 경기 {OPS['by_region']['경기']:,} · 인천 {OPS['by_region']['인천']:,} · 부산 {OPS['by_region']['부산']:,}</p>
<p>· 평균 도착 {OPS['avg_arrival']}분 · 평점 {OPS['rating']} (후기 {OPS['review_count']:,}건)</p></div></section>

<section class="wrap tight" id="faq"><span class="eyebrow">FAQ</span><h2>자주 묻는 질문</h2>
<div style="margin-top:24px">{faq_block(FAQ_MAIN)}</div></section>

{references_block(extra_internal=[("회사 소개","/about/"),("편집 정책","/editorial-policy/"),("개인정보처리방침","/policy/privacy/"),("이용약관","/policy/terms/")])}
{cta_band()}"""

    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": url("/#website"),
               "url": D, "name": SITE["brand"], "inLanguage": "ko-KR",
               "potentialAction": {"@type": "SearchAction", "target": url("/?q={search_term_string}"),
                                   "query-input": "required name=search_term_string"}}
    local = {"@context": "https://schema.org", "@type": "HealthAndBeautyBusiness", "@id": url("/#local"),
             "name": SITE["brand"], "image": url("/assets/og-cover.jpg"), "url": D,
             "telephone": SITE["phone_intl"], "priceRange": "₩₩",
             "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                "opens": "11:00", "closes": "05:00"}],
             "areaServed": [v["ko"] for v in REGIONS.values()],
             "aggregateRating": {"@type": "AggregateRating", "ratingValue": OPS["rating"],
                                 "reviewCount": OPS["review_count"], "bestRating": 5},
             "contactPoint": {"@type": "ContactPoint", "telephone": SITE["phone_intl"],
                              "contactType": "reservations", "availableLanguage": ["ko","en","zh","ja"]}}
    article = {"@context": "https://schema.org", "@type": "Article",
               "headline": "마사지고 출장마사지 운영 안내", "inLanguage": "ko-KR",
               "image": {"@type": "ImageObject", "url": url("/assets/og-cover.jpg"), "width": 1200, "height": 630},
               "mainEntityOfPage": D,
               "author": [{"@type": "Person", "name": t["name"], "jobTitle": t["role"],
                           "url": url(f"/authors/{AUTHOR_SLUG[t['name']]}/")} for t in TEAM],
               "reviewedBy": {"@type": "Person", "name": "박지연", "jobTitle": "안전 자문 트레이너",
                              "url": url("/authors/park-jiyeon/")},
               "publisher": {"@id": url("/#org")}, "datePublished": "2026-01-05", "dateModified": NOW,
               "citation": [{"@type": "CreativeWork", "name": f"{org} — {t}", "url": u} for t, org, u in REFERENCES]}
    write("/", page(
        f"{SITE['brand']} — 출장마사지 예약 {SITE['phone']} · 서울·경기·인천·부산 전 권역",
        f"마사지고 출장마사지. 전화 한 통이면 가까운 매니저가 출발합니다. 서울 기준 평균 {OPS['avg_arrival']}분 도착, 스웨디시·아로마·타이·로미로미·스포츠 5종. 예약 {SITE['phone']}, {SITE['hours']}.",
        "/", body, [ORG_JSONLD, website, local, article, faq_jsonld(FAQ_MAIN)]))


def build_services():
    # hub
    cards = "".join(
        f'<a class="card reveal" href="/service/{s["slug"]}/"><div class="kicker">{esc(s["kicker"])}</div>'
        f'<h3>{esc(s["ko"])} 마사지</h3><p>{esc(s["summary"])}</p><span class="more">자세히 →</span></a>'
        for s in SERVICES)
    cb = [("홈", "/"), ("서비스", None)]
    choose = [
        ("풀어 주는 코스 — 스웨디시·아로마", [
            "오일을 사용해 전신을 부드럽게 풀어 주는 코스입니다.",
            "스웨디시는 순환과 근육 이완에, 아로마는 향을 통한 정서적 이완과 수면에 무게를 둡니다.",
            "마사지가 처음이거나 자기 전 받고 싶은 분께 권합니다.",
        ]),
        ("늘려 주는 코스 — 타이", [
            "오일 없이 지압과 스트레칭으로 가동 범위를 넓히는 건식 코스입니다.",
            "오래 앉아 굳은 몸을 시원하게 펴고 싶거나, 끈적임 없이 받고 싶은 분께 잘 맞습니다.",
        ]),
        ("감싸 주는 코스 — 로미로미", [
            "팔뚝 전체로 파도처럼 흐르는 하와이 전통 코스입니다.",
            "특정 통증보다 전반적인 피로와 긴장을 깊게 풀고 싶은 분께 권합니다.",
        ]),
        ("눌러 주는 코스 — 스포츠", [
            "강한 압으로 특정 부위의 뭉침을 집중 관리하는 회복형 코스입니다.",
            "운동 후 근육 피로나 또렷한 어깨·허리 통증이 있는 분께 권합니다.",
        ]),
    ]
    ch_html = notes_section("어떤 코스를 고를까", choose, eyebrow="HOW TO CHOOSE")
    faqs = [
        ("처음인데 뭘 골라야 하나요?", "스웨디시 90분이 가장 무난합니다. 예약 시 컨디션을 말씀하시면 함께 골라 드립니다."),
        ("코스를 도착 후 바꿀 수 있나요?", "가능한 범위에서 조정해 드립니다. 다만 준비물이 다른 경우가 있어 예약 시 정해 두면 좋습니다."),
        ("모든 코스가 전 지역 출장 되나요?", "네. 서울·경기·인천·부산 전 권역에서 5종 모두 가능합니다."),
    ]
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">SERVICES</span>
<h1>다섯 가지 시그니처 코스</h1>
<p class="lead">스웨디시·아로마·타이·로미로미·스포츠. 같은 마사지처럼 보여도 풀어 주는 방식과 잘 맞는 컨디션이 모두 다릅니다. 각 코스의 특징과 추천 상황을 확인하고 오늘 내 몸에 맞는 코스를 골라 보세요.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div></section>
{ch_html}
<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>코스 선택 자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
{cta_band()}"""
    write("/service/", page(f"출장마사지 서비스 — 5종 코스 비교·선택 가이드 | {SITE['brand']}",
        "스웨디시·아로마·타이·로미로미·스포츠 5종 출장마사지 코스를 비교하세요. 컨디션별 추천과 선택 가이드, 가격을 한눈에 안내합니다.",
        "/service/", body, [breadcrumb_jsonld(cb), faq_jsonld(faqs)]))
    # detail
    for s in SERVICES:
        cb = [("홈", "/"), ("서비스", "/service/"), (s["ko"], None)]
        ln = "".join(f"<p>{esc(p)}</p>" for p in s["long"])
        rows = "".join(price_card(x) for x in SERVICES if x["slug"] == s["slug"])
        faqs = [
            (f"{s['ko']} 마사지는 어떤 분께 맞나요?", f"{s['summary']} 더 자세한 추천 상황은 위 안내를 참고해 주세요."),
            (f"{s['ko']}는 시간을 어떻게 고르나요?", "60·90·120분 중 선택하실 수 있습니다. 처음이면 전신을 균형 있게 받는 90분을 가장 많이 권하고, 핵심만 받고 싶으면 60분, 여유 있게 받고 싶으면 120분이 좋습니다."),
            ("출장 지역은 어디까지 되나요?", "서울·경기·인천·부산 전 권역 가능합니다. 예약 시 현재 위치를 말씀해 주시면 가까운 매니저를 배정하고 예상 도착 시간을 안내드립니다."),
            ("관리사 국적·성별을 고를 수 있나요?", "네. 예약 시 선호를 말씀하시면 가능한 범위에서 맞춰 배정합니다. 시간대·권역에 따라 어려울 때는 가까운 대안을 함께 안내드립니다."),
            (f"{s['ko']}를 받을 때 무엇을 준비하나요?", "한 사람이 누울 공간이면 충분합니다. 오일 코스는 수건을 한두 장 준비하면 좋고, 샤워를 미리 해 두면 한결 쾌적합니다."),
            ("관리 시간은 실제로 얼마나 걸리나요?", "선택한 코스 시간에 더해 준비와 마무리로 10분 안팎이 더 소요됩니다. 시간을 넉넉히 잡아 두시면 여유롭게 받을 수 있습니다."),
            ("결제와 추가 비용은요?", "관리 시작 전 안내된 금액으로 결제하며 표시 금액 외 추가 비용은 없습니다. 심야·도서 지역 등 일부 권역은 예약 시 미리 안내드립니다."),
            ("질환이 있어도 받을 수 있나요?", "건강관리를 위한 이완 서비스이며 의료 행위가 아닙니다. 디스크·관절 질환, 수술 이력, 임신 등이 있으면 예약 시 알려 주시고, 통증·질환은 전문의 상담을 함께 받으시길 권합니다."),
        ]
        other = "".join(f'<a href="/service/{o["slug"]}/">{o["ko"]}</a>' for o in SERVICES if o["slug"] != s["slug"])
        secs = SERVICE_SECTIONS.get(s["slug"], [])
        extra = SERVICE_EXTRA.get(s["slug"], [])
        deep_sec = [("관리 디테일", s["deep"])]
        secs = secs + deep_sec
        sec_html = notes_section(f"{s['ko']}, 자세히 알아보기", secs, eyebrow="GUIDE")
        extra_html = notes_section(f"{s['ko']} 출장 이용 안내", extra, eyebrow="MORE", start=len(secs) + 1)
        body = f"""<section class="wrap">{crumb(cb)}
<span class="eyebrow">{esc(s['kicker'])}</span><h1>{esc(s['ko'])} 출장마사지</h1>
<p class="lead">{esc(s['summary'])}</p>
{byline(author="김세영", reviewer="박지연")}
<div class="prose" style="margin-top:24px;max-width:680px">{ln}</div></section>
{sec_html}
{extra_html}
<section class="wrap tight"><span class="eyebrow">PRICING</span><h2>{esc(s['ko'])} 요금</h2>
<div class="grid g3" style="margin-top:24px">{rows}</div>
<p style="margin-top:14px;color:var(--dim);font-size:13px">표시 금액 외 추가 비용은 없습니다. 심야·도서 지역 등 일부 권역은 예약 시 안내드립니다.</p></section>
<section class="wrap tight"><h2>다른 코스도 살펴보세요</h2>
<p class="lead">컨디션에 따라 잘 맞는 코스가 다릅니다. 아래에서 비교해 보세요.</p>
<div class="linklist">{other}</div></section>
<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>{esc(s['ko'])} 자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
{references_block(extra_internal=[("전체 요금표","/pricing/"),("관리사 안내","/therapists/"),("편집 정책","/editorial-policy/"),("이용약관","/policy/terms/")])}
{cta_band()}"""
        service_ld = {"@context": "https://schema.org", "@type": "Service",
                      "name": f"{s['ko']} 출장마사지", "serviceType": s["en"] + " massage",
                      "provider": {"@id": url("/#org")}, "areaServed": [v["ko"] for v in REGIONS.values()],
                      "description": s["summary"],
                      "offers": [{"@type": "Offer", "name": f"{s['ko']} {t}", "price": p.replace(",","").replace("원",""),
                                  "priceCurrency": "KRW"} for t, p in s["prices"]]}
        write(f"/service/{s['slug']}/", page(
            f"{s['ko']} 출장마사지 — 가격·추천·예약 | {SITE['brand']}",
            f"{s['ko']} 출장마사지 안내. {s['summary']} 60·90·120분 가격과 추천 상황을 확인하고 {SITE['phone']}로 예약하세요.",
            f"/service/{s['slug']}/", body,
            [service_ld, webpage_jsonld(f"/service/{s['slug']}/", f"{s['ko']} 출장마사지", s['summary']),
             breadcrumb_jsonld(cb), faq_jsonld(faqs)]))


def build_therapists():
    cards = "".join(
        f'<a class="card reveal" href="/therapists/{t["slug"]}/"><div class="kicker">{esc(t["en"]).upper()}</div>'
        f'<h3>{esc(t["ko"])} 관리사</h3><p>{esc(t["desc"])}</p><span class="more">자세히 →</span></a>'
        for t in THERAPISTS)
    cb = [("홈", "/"), ("관리사", None)]
    guide = [
        ("소통을 가장 중시한다면", [
            "압 조절과 부위 요청을 우리말로 세밀하게 전하고 싶다면 한국인 관리사를 권합니다.",
            "마사지가 처음이라 진행 과정을 묻고 확인하며 받고 싶은 분께도 잘 맞습니다.",
        ]),
        ("강한 압을 원한다면", [
            "묵직하고 깊은 지압을 선호한다면 중국인 관리사가 강점을 보입니다.",
            "만성적인 어깨·등 뭉침을 시원하게 풀고 싶은 분께 권합니다.",
        ]),
        ("스트레칭·이완을 원한다면", [
            "오일 없이 시원하게 늘리고 싶다면 타이, 부드럽고 섬세한 오일 이완을 원하면 베트남 관리사가 잘 맞습니다.",
            "전신을 고르게 풀고 싶다면 러시아, 차분한 분위기를 원하면 일본 관리사를 권합니다.",
        ]),
    ]
    g_html = notes_section("어떤 관리사를 고를까", guide, eyebrow="HOW TO CHOOSE")
    faqs = [
        ("국적·성별을 지정할 수 있나요?", "네. 예약 시 선호를 말씀하시면 가능한 범위에서 맞춰 배정합니다."),
        ("원하는 조건이 어려울 때는요?", "시간대·권역에 따라 대기 매니저가 달라, 어려울 때는 가까운 대안을 함께 안내드립니다."),
        ("국적과 무관하게 지켜지는 것은요?", "모든 매니저는 본사 등록 절차와 자문 트레이너 기본 교육을 이수하며, 압은 언제든 조절·중단할 수 있습니다."),
    ]
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">THERAPISTS</span>
<h1>관리사 국적 안내</h1><p class="lead">국적에 따라 손길의 스타일과 잘 맞는 코스가 다릅니다. 한국·중국·태국·베트남·러시아·일본 관리사의 강점을 비교하고, 선호가 있으면 예약 시 말씀해 주세요.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div></section>
{g_html}
<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>관리사 배정 자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
{cta_band()}"""
    write("/therapists/", page(f"관리사 국적 안내 — 6개국 강점 비교 | {SITE['brand']}",
        "한국·중국·태국·베트남·러시아·일본 관리사의 국적별 강점과 잘 맞는 코스를 비교합니다. 선호 국적·성별 배정이 가능합니다.",
        "/therapists/", body, [breadcrumb_jsonld(cb), faq_jsonld(faqs)]))
    for t in THERAPISTS:
        cb = [("홈", "/"), ("관리사", "/therapists/"), (t["ko"], None)]
        pts = "".join(f'<div class="chip"><span class="k">강점</span><span class="v">{esc(p)}</span></div>' for p in t["points"])
        other = "".join(f'<a href="/therapists/{o["slug"]}/">{o["ko"]}</a>' for o in THERAPISTS if o["slug"] != t["slug"])
        faqs = [(f"{t['ko']} 관리사를 지정해 예약할 수 있나요?", "네. 예약 시 선호 국적을 말씀하시면 가능한 범위에서 배정합니다. 시간대·권역에 따라 어려울 때는 가까운 대안을 안내드립니다."),
                ("성별도 함께 고를 수 있나요?", "네. 선호 성별을 함께 말씀해 주세요. 국적과 성별을 모두 지정하면 대기 매니저 상황에 따라 시간이 더 걸릴 수 있습니다."),
                (f"{t['ko']} 관리사는 어떤 코스와 잘 맞나요?", t["desc"] + " 위 안내에서 추천 코스를 확인하실 수 있습니다."),
                ("소통이 어렵지 않을까요?", "압 조절·부위 요청 같은 핵심 의사는 간단한 표현으로 충분히 전달됩니다. 소통의 편안함이 가장 중요하면 한국인 관리사를 요청해 주세요."),
                ("국적과 무관하게 지켜지는 것은요?", "모든 매니저는 본사 등록 절차와 자문 트레이너 기본 교육을 이수합니다. 압은 언제든 조절·중단할 수 있고, 약속된 관리 외의 행위는 정중히 거절될 수 있습니다.")]
        secs = THERAPIST_SECTIONS.get(t["slug"], [])
        deep = THERAPIST_DEEP.get(t["slug"], [])
        sec_html = notes_section(f"{t['ko']} 관리사, 자세히", secs, eyebrow="PROFILE")
        deep_html = notes_section(f"{t['ko']} 관리사 이용 가이드", deep, eyebrow="GUIDE", start=len(secs) + 1)
        common_html = notes_section("배정·소통·안전 안내", THERAPIST_COMMON + THERAPIST_EXTRA, eyebrow="POLICY", start=len(secs) + len(deep) + 1)
        body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">{esc(t['en']).upper()} THERAPIST</span>
<h1>{esc(t['ko'])} 관리사</h1><p class="lead">{esc(t['desc'])}</p>
{byline(author="박지연", reviewer="이도현")}
<div class="chips">{pts}</div></section>
{sec_html}
{deep_html}
{common_html}
<section class="wrap tight"><h2>다른 국적 관리사</h2><div class="linklist">{other}</div></section>
<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
{references_block(extra_internal=[("서비스 코스 안내","/service/"),("회사 소개","/about/"),("편집 정책","/editorial-policy/"),("이용약관","/policy/terms/")])}
{cta_band()}"""
        write(f"/therapists/{t['slug']}/", page(
            f"{t['ko']} 관리사 출장마사지 | {SITE['brand']}",
            f"{t['ko']} 관리사 안내. {t['desc']} 국적별 강점·추천 코스·선호 배정 안내, 예약 {SITE['phone']}.",
            f"/therapists/{t['slug']}/", body,
            [webpage_jsonld(f"/therapists/{t['slug']}/", f"{t['ko']} 관리사 출장마사지", t['desc'],
                            author="박지연", reviewer="이도현"),
             breadcrumb_jsonld(cb), faq_jsonld(faqs)]))


def build_pricing():
    cb = [("홈", "/"), ("요금", None)]
    cards = "".join(price_card(s) for s in SERVICES)
    notes = [
        ("요금은 코스와 시간으로 정해집니다", [
            "모든 코스는 60·90·120분 세 가지 시간으로 운영하며, 시간이 길수록 전신을 빠짐없이, 여유 있게 받을 수 있습니다.",
            "오일을 쓰는 아로마·로미로미는 준비 과정이 더 들어가 건식 코스보다 다소 높게 책정됩니다.",
            "어떤 코스든 표시된 금액이 전부이며, 시작 전 안내한 금액 외에 추가로 청구하는 항목은 없습니다.",
        ]),
        ("시간은 이렇게 고르세요", [
            "60분은 핵심 부위 위주로 짧게 받고 싶을 때, 90분은 전신을 균형 있게 받고 싶을 때 적당합니다.",
            "120분은 두피·손·발 마무리까지 충분히 받고 싶은 분께 권합니다.",
            "처음이라면 90분을 가장 많이 선택합니다.",
        ]),
        ("결제와 추가 비용", [
            "결제는 관리 시작 전, 안내된 금액으로 진행합니다.",
            "심야 시간대나 강화·옹진 등 도서 지역은 이동 여건에 따라 예약 시 별도로 안내드립니다.",
            "예약 전 금액을 명확히 확인하실 수 있어, 받고 나서 예상과 달라지는 일이 없습니다.",
        ]),
        ("예약 변경·취소·환불", [
            "예약 변경이나 취소는 가능한 한 빨리 고객센터로 연락 주시면 도와드립니다.",
            "이미 매니저가 출발한 뒤의 취소는 이동에 따른 안내가 있을 수 있습니다.",
            "환불·분쟁은 관련 법령과 이용약관에 따라 처리합니다.",
        ]),
        ("코스별 가격이 다른 이유", [
            "스웨디시·타이는 같은 시간대 가장 합리적인 가격으로, 처음 받기에 부담이 적습니다.",
            "아로마는 에센셜 오일 블렌딩이 더해지고, 로미로미는 충분한 오일과 긴 흐름이 필요해 조금 높게 책정됩니다.",
            "스포츠는 부위 집중 관리에 손이 많이 들어가는 회복형 코스입니다.",
        ]),
        ("이렇게 받으면 더 합리적입니다", [
            "처음이라면 90분이 시간 대비 만족도가 가장 좋습니다. 60분은 핵심만, 120분은 여유 있게 받는 선택입니다.",
            "집중해서 풀고 싶은 부위가 있다면 미리 말씀해 그 부위에 시간을 배분받는 편이 같은 금액에서 효율적입니다.",
            "어떤 코스가 맞을지 모르겠다면 예약 시 컨디션을 말씀해 주세요. 불필요하게 비싼 코스를 권하지 않습니다.",
        ]),
        ("출장비·심야 안내", [
            "기본 권역은 별도의 출장비가 없습니다. 표시된 코스 금액에 이동 비용이 포함된 개념으로 보시면 됩니다.",
            "강화·옹진·기장·가평 등 거리가 먼 외곽·도서 지역만, 이동 여건에 따라 예약 시 미리 안내드립니다.",
            "심야 시간대는 권역에 따라 도착이 더 걸릴 수 있으며, 금액 변동이 있는 경우 예약 시 분명히 알려 드립니다.",
        ]),
        ("정직한 가격 약속", [
            "받고 난 뒤 금액이 달라지거나, 안내하지 않은 항목을 더 청구하는 일은 없습니다.",
            "할인을 미끼로 한 과장 광고나 현장 추가 권유를 하지 않습니다.",
            "예약 전화에서 최종 금액을 분명히 확인하실 수 있으니, 궁금한 점은 무엇이든 물어보세요.",
        ]),
        ("시간대·지역에 따른 차이", [
            "기본 권역에서는 시간대와 무관하게 표시 금액으로 받으실 수 있습니다.",
            "다만 심야 시간대나 거리가 먼 외곽·도서 지역은 이동 여건에 따라 도착이 더 걸리거나 별도 안내가 있을 수 있습니다.",
            "이런 경우에도 변동 사항은 예약 전화에서 미리 분명히 알려 드립니다.",
        ]),
        ("어떤 코스가 좋을지 모르겠다면", [
            "예약 시 오늘의 컨디션과 불편한 부위를 말씀해 주시면 그에 맞는 코스와 시간을 함께 골라 드립니다.",
            "처음이라면 스웨디시 90분, 수면이 고민이면 아로마, 또렷한 통증은 스포츠를 권합니다.",
            "각 코스의 자세한 추천 상황은 서비스 페이지에서 확인하실 수 있습니다.",
            "불필요하게 비싼 코스를 권하지 않으며, 처음에는 부담 없는 코스로 시작해 보시기를 권합니다.",
            "한 번 받아 본 뒤 다음 예약 때 시간을 늘리거나 코스를 바꾸는 분이 많으니, 처음부터 길게 잡지 않으셔도 됩니다.",
        ]),
    ]
    n_html = notes_section("요금 안내, 자세히", notes, eyebrow="DETAILS")
    faqs = [
        ("표시된 금액 외에 더 내는 게 있나요?", "없습니다. 시작 전 안내한 금액이 전부입니다. 심야·도서 지역은 예약 시 미리 안내드립니다."),
        ("출장비가 따로 있나요?", "기본 권역은 출장비가 별도로 없습니다. 거리가 먼 일부 외곽·도서 지역만 예약 시 안내드립니다."),
        ("현금만 되나요?", "예약 시 가능한 결제 방법을 안내드립니다."),
        ("코스를 도중에 바꾸면 금액은요?", "변경된 코스·시간 기준으로 안내드리며, 시작 전에 정해 두는 것을 권합니다."),
    ]
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">PRICING</span>
<h1>요금 안내</h1><p class="lead">모든 코스 60·90·120분 기준입니다. 표시 금액 외 추가 비용은 없으며, 예약 전에 정확한 금액을 확인하실 수 있습니다.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div></section>
{n_html}
<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>요금 자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
{cta_band()}"""
    write("/pricing/", page(f"출장마사지 요금표 — 코스별 가격·결제 안내 | {SITE['brand']}",
        "스웨디시·아로마·타이·로미로미·스포츠 출장마사지 요금표. 60·90·120분 가격, 시간 선택·결제·환불 안내까지 한눈에. 추가 비용 없음.",
        "/pricing/", body, [breadcrumb_jsonld(cb), faq_jsonld(faqs)]))


def build_reviews():
    cb = [("홈", "/"), ("후기", None)]
    # 집계 후기 = 메인 + 여러 권역 대표 구 (실제 행정구 후기에서 발췌)
    items = list(REVIEWS_MAIN)
    _samples = [
        ("seoul", "gangnam", "강남구", ["역삼동", "삼성동", "논현동"], "서울 강남"),
        ("seoul", "mapo", "마포구", ["서교동", "합정동", "상암동"], "서울 마포"),
        ("gyeonggi", "seongnam", "성남시", ["정자동", "서현동", "판교동"], "경기 성남"),
        ("gyeonggi", "suwon", "수원시", ["영통동", "인계동", "권선동"], "경기 수원"),
        ("incheon", "yeonsu", "연수구", ["송도동", "연수동", "동춘동"], "인천 연수"),
        ("busan", "haeundae", "해운대구", ["우동", "중동", "좌동"], "부산 해운대"),
    ]
    for metro, slug, ko, dongs, area in _samples:
        for r in district_reviews(metro, slug, ko, dongs)[:3]:
            items.append({"name": r["name"], "area": area, "course": r["course"], "stars": r["stars"], "text": r["text"]})
    rev_html = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*r["stars"]}</div><p>{esc(r["text"])}</p>'
        f'<div class="who"><b>{esc(r["name"])}</b> · {esc(r["area"])} · {esc(r["course"])}</div></div>'
        for r in items)
    notes = [
        ("후기는 이렇게 검증합니다", [
            "후기는 실제로 관리를 받은 고객의 작성분만 게시합니다.",
            "본사 배차 로그와 대조해, 이용 기록이 확인되지 않는 후기나 중복·허위로 의심되는 글은 게시에서 제외합니다.",
            "지나치게 홍보성으로 보이거나 사실과 다른 내용은 싣지 않는 것이 원칙입니다.",
        ]),
        ("평점은 어떻게 집계하나요", [
            f"현재 전체 평점은 {OPS['rating']}이며, 누적 후기 {OPS['review_count']:,}건의 평균입니다.",
            "행정구 페이지의 평점은 해당 지역 이용 고객의 후기만 따로 모아 산출합니다.",
            "낮은 평가도 함께 반영해, 평점을 인위적으로 부풀리지 않습니다.",
        ]),
        ("권역별로 후기가 다른 이유", [
            "지역마다 인기 코스와 이용 상황이 달라, 후기에 담기는 내용도 자연스럽게 달라집니다.",
            "도심권은 퇴근 후 빠른 도착에 대한 후기가, 주거권은 주말·야간 이용 후기가 많습니다.",
            "각 행정구 페이지에서 그 지역의 실제 후기를 확인하실 수 있습니다.",
        ]),
        ("후기에서 자주 언급되는 점", [
            "가장 많이 언급되는 것은 '생각보다 빠른 도착'과 '시간 약속을 지킨다'는 점입니다.",
            "'압을 계속 확인해 줘서 편했다'는 후기도 많아, 강도 소통이 만족도에 큰 영향을 준다는 것을 보여 줍니다.",
            "출장임에도 '준비가 꼼꼼하고 깔끔했다'는 평이 이어집니다.",
        ]),
        ("후기를 남기고 싶다면", [
            "관리를 받으신 뒤 고객센터를 통해 후기를 전해 주시면 검토 후 게시합니다.",
            "좋았던 점뿐 아니라 아쉬웠던 점도 환영합니다. 운영 개선의 가장 중요한 자료가 됩니다.",
            "개인을 특정할 수 있는 정보는 가린 채로 게시해, 작성자의 사생활을 보호합니다.",
        ]),
    ]
    n_html = notes_section("후기를 신뢰할 수 있는 이유", notes, eyebrow="METHODOLOGY")
    region_stats = "".join(
        f'<div class="chip"><span class="k">{esc(rk)}</span><span class="v">{rv:,}건 배차</span></div>'
        for rk, rv in OPS["by_region"].items())
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">REVIEWS</span>
<h1>고객 후기</h1><p class="lead">실제 이용 고객이 남긴 후기만 게시하며 본사 운영 로그와 대조해 검증합니다. 평점 {OPS['rating']} · 누적 {OPS['review_count']:,}건.</p>
<div class="chips">{region_stats}</div>
<div class="grid g3" style="margin-top:30px">{rev_html}</div></section>
{n_html}
{cta_band()}"""
    ld = {"@context": "https://schema.org", "@type": "ItemList",
          "itemListElement": [{"@type": "ListItem", "position": i,
            "item": {"@type": "Review", "author": {"@type": "Person", "name": r["name"]},
                     "reviewBody": r["text"],
                     "reviewRating": {"@type": "Rating", "ratingValue": r["stars"], "bestRating": 5}}}
            for i, r in enumerate(items, 1)]}
    agg = {"@context": "https://schema.org", "@type": "AggregateRating",
           "itemReviewed": {"@type": "Organization", "name": SITE["brand"]},
           "ratingValue": OPS["rating"], "reviewCount": OPS["review_count"], "bestRating": 5}
    write("/reviews/", page(f"고객 후기 — 평점 {OPS['rating']} | {SITE['brand']}",
        f"마사지고 출장마사지 실제 고객 후기. 평점 {OPS['rating']}, 총 {OPS['review_count']:,}건. 검증된 후기만 게시합니다.",
        "/reviews/", body, [ld, agg, breadcrumb_jsonld(cb)]))


def build_magazine():
    cb = [("홈", "/"), ("매거진", None)]
    cards = "".join(
        f'<a class="card reveal" href="/magazine/{m["slug"]}/"><div class="kicker">{esc(m["date"])} · {esc(m["author"])}</div>'
        f'<h3>{esc(m["title"])}</h3><p>{esc(m["desc"])}</p><span class="more">읽기 →</span></a>'
        for m in MAGAZINE)
    m_notes = [
        ("매거진은 이런 글을 담습니다", [
            "마사지고 매거진은 출장마사지를 처음 받는 분, 코스 선택이 고민인 분, 안전이 궁금한 분을 위한 안내 글을 싣습니다.",
            "광고성 과장 대신, 실제 운영하며 가장 많이 받은 질문과 1차 데이터를 바탕으로 작성합니다.",
            "어디서나 볼 수 있는 일반론보다, 직접 운영해야 알 수 있는 내용을 우선합니다.",
        ]),
        ("누가 쓰나요", [
            "글은 운영팀이 작성하고, 안전·건강 관련 내용은 자문 트레이너가 감수합니다.",
            "각 글에는 작성자의 실명과 직책을 밝혀, 누가 어떤 책임으로 쓴 글인지 확인하실 수 있습니다.",
            "자세한 작성·검증 기준은 편집 정책 페이지에 공개합니다.",
        ]),
    ]
    n_html = notes_section("매거진 소개", m_notes, eyebrow="ABOUT")
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">MAGAZINE</span>
<h1>매거진</h1><p class="lead">출장마사지를 처음 받는 분과 코스 선택이 고민인 분을 위한, 마사지고 운영팀의 안내 글입니다.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div></section>
{n_html}
{cta_band()}"""
    write("/magazine/", page(f"매거진 — 출장마사지 가이드 | {SITE['brand']}",
        "출장마사지 첫 이용 가이드, 컨디션별 코스 선택, 안전 원칙까지. 마사지고 운영팀이 직접 작성하고 자문 트레이너가 감수한 안내 글.",
        "/magazine/", body, breadcrumb_jsonld(cb)))
    for m in MAGAZINE:
        cb = [("홈", "/"), ("매거진", "/magazine/"), (m["title"], None)]
        toc = "".join(f'<a href="#s{i}">{esc(h)}</a>' for i, h in enumerate(m["toc"], 1))
        sections = ""
        for i, (h, paras) in enumerate(m["body"], 1):
            ps = "".join(f"<p>{esc(p)}</p>" for p in paras)
            sections += f'<h2 id="s{i}">{esc(h)}</h2>{ps}'
        a = AUTHORS[m["author"]]
        mag_reviewer = "박지연" if m["author"] != "박지연" else "이도현"
        body = f"""<section class="wrap" style="max-width:760px">{crumb(cb)}
<span class="eyebrow">{esc(m['date'])} 발행 · 최종 업데이트 {NOW}</span><h1 style="font-size:clamp(30px,4.5vw,48px)">{esc(m['title'])}</h1>
<p class="lead">{esc(m['desc'])}</p>
{byline(author=m['author'], reviewer=mag_reviewer, updated=NOW)}
<div class="prose" style="margin-top:18px"><p style="font-size:16px">{esc(m.get('lead',''))}</p></div>
<div class="toc"><span class="label">목차</span>{toc}</div>
<div class="prose">{sections}</div>
<div class="linklist" style="margin-top:40px">{"".join(f'<a href="/magazine/{o["slug"]}/">{esc(o["title"][:18])}…</a>' for o in MAGAZINE if o["slug"]!=m["slug"])}</div>
</section>
{references_block(extra_internal=[("회사 소개","/about/"),("편집 정책","/editorial-policy/"),("서비스 코스","/service/"),("요금 안내","/pricing/")])}
{cta_band()}"""
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": m["title"],
              "description": m["desc"], "inLanguage": "ko-KR",
              "image": {"@type": "ImageObject", "url": url("/assets/og-cover.jpg"), "width": 1200, "height": 630},
              "datePublished": m["date"], "dateModified": NOW,
              "author": {"@type": "Person", "name": m["author"], "jobTitle": a["role"],
                         "url": url(f"/authors/{AUTHOR_SLUG[m['author']]}/")},
              "reviewedBy": {"@type": "Person", "name": mag_reviewer, "jobTitle": AUTHORS[mag_reviewer]["role"],
                             "url": url(f"/authors/{AUTHOR_SLUG[mag_reviewer]}/")},
              "publisher": {"@id": url("/#org")},
              "mainEntityOfPage": url(f"/magazine/{m['slug']}/"),
              "citation": [{"@type": "CreativeWork", "name": f"{org} — {t}", "url": u} for t, org, u in REFERENCES]}
        write(f"/magazine/{m['slug']}/", page(
            f"{m['title']} | {SITE['brand']} 매거진",
            m["desc"], f"/magazine/{m['slug']}/", body, [ld, breadcrumb_jsonld(cb)]))


def build_authors():
    for t in TEAM:
        slug = AUTHOR_SLUG[t["name"]]
        cb = [("홈", "/"), ("저자", None), (t["name"], None)]
        wrote = [m for m in MAGAZINE if m["author"] == t["name"]]
        wl = "".join(f'<a href="/magazine/{m["slug"]}/">{esc(m["title"])}</a>' for m in wrote)
        wl_html = f'<section class="wrap tight"><h2>{esc(t["name"])}이(가) 작성한 글</h2><div class="linklist">{wl}</div></section>' if wrote else ""
        role_notes = {
            "서울·경기권 운영팀장": [
                ("담당 영역", [
                    "서울과 경기 권역의 매니저 배치와 배차 동선 설계, 도착 시간 관리를 총괄합니다.",
                    "혼잡 시간대 인접 권역 운용과 신도시권 매니저 배치 전략을 책임집니다.",
                ]),
                ("이런 글을 씁니다", [
                    "예약 절차, 도착 시간, 권역별 운영 특징처럼 실제 배차 데이터에서 나온 내용을 주로 다룹니다.",
                    "현장에서 가장 많이 받은 질문을 토대로 글의 주제를 정합니다.",
                ]),
            ],
            "안전 자문 트레이너": [
                ("전문 배경", [
                    "KSPO 스포츠마사지 트레이너로, 재활케어 분야에서 8년간 경력을 쌓았습니다.",
                    "강압을 피하고 안전하게 관리하는 가이드라인을 만들고 감수합니다.",
                ]),
                ("이런 글을 씁니다", [
                    "코스 선택, 안전하게 받는 법, 컨디션별 추천처럼 몸과 직접 관련된 내용을 다룹니다.",
                    "건강관리 서비스의 범위와 한계를 분명히 밝혀, 과장 없이 안내하는 것을 원칙으로 합니다.",
                ]),
            ],
            "인천·부산권 운영팀장": [
                ("담당 영역", [
                    "인천과 부산 권역의 디스패치 운영, 권역별 매니저 배치와 후기 검증을 담당합니다.",
                    "해안·도서 지역을 포함한 넓은 권역의 도착 시간 관리를 책임집니다.",
                ]),
                ("이런 글을 씁니다", [
                    "지역 운영, 후기 검증, 신뢰 원칙처럼 운영 신뢰와 관련된 내용을 주로 다룹니다.",
                    "고객이 직접 확인할 수 있는 안전장치를 투명하게 설명합니다.",
                ]),
            ],
        }
        rn = role_notes.get(t["role"], [])
        rn_html = notes_section(f"{t['name']} 소개", rn, eyebrow="PROFILE") if rn else ""
        body = f"""<section class="wrap" style="max-width:760px">{crumb(cb)}
<span class="eyebrow">AUTHOR · {esc(t['role'])}</span><h1>{esc(t['name'])}</h1>
<p class="lead">{esc(t['bio'])}</p>
<div class="prose" style="margin-top:24px">
<p>마사지고 운영팀의 일원으로 실명과 책임 영역을 공개합니다. 사이트의 콘텐츠는 운영 경험과 본사 1차 배차 데이터를 바탕으로 작성·감수되며, 누가 어떤 책임으로 만든 글인지 명확히 하는 것이 신뢰의 출발이라고 믿습니다.</p>
</div></section>
{rn_html}
{wl_html}{cta_band()}"""
        ld = {"@context": "https://schema.org", "@type": "Person", "name": t["name"],
              "jobTitle": t["role"], "description": t["bio"], "url": url(f"/authors/{slug}/"),
              "worksFor": {"@id": url("/#org")}}
        write(f"/authors/{slug}/", page(
            f"{t['name']} — {t['role']} | {SITE['brand']}",
            f"{t['name']} · {t['role']}. {t['bio']}",
            f"/authors/{slug}/", body, [ld, breadcrumb_jsonld(cb)]))


def build_static_pages():
    # about
    cb = [("홈", "/"), ("회사 소개", None)]
    team = "".join(f'<div class="card reveal"><div class="kicker">{esc(t["role"])}</div>'
                   f'<h3><a href="/authors/{AUTHOR_SLUG[t["name"]]}/">{esc(t["name"])}</a></h3><p>{esc(t["bio"])}</p></div>' for t in TEAM)
    notes = [
        ("우리가 하는 일 (Who)", [
            "마사지고는 고객의 공간으로 찾아가는 출장마사지를 운영하는 팀입니다.",
            "외부 업체에 연결만 해 주는 중개가 아니라, 본사 디스패처가 직접 매니저를 배정하고 도착까지 책임집니다.",
            "운영을 책임지는 팀장과 안전을 감수하는 자문 트레이너의 실명과 역할을 공개합니다.",
        ]),
        ("어떻게 운영하나 (How)", [
            "전화 접수 → 가까운 매니저 배정 → 출발·도착 안내 → 관리 → 사전 안내 금액 결제. 이 흐름을 모든 예약에서 동일하게 지킵니다.",
            "배차는 본사가 직접 하므로, 누가 어느 지역으로 방문하는지 본사가 항상 파악합니다.",
            "혼잡 시간대에는 인접 권역 매니저를 함께 운용해 대기 시간을 줄입니다.",
        ]),
        ("왜 이렇게 하나 (Why)", [
            "이동과 대기 없이, 익숙한 내 공간에서 받는 휴식의 가치를 믿습니다.",
            "낯선 사람이 공간에 온다는 점에서 신뢰가 가장 중요하다고 보고, 배정과 금액을 투명하게 공개합니다.",
            "한 번의 좋은 관리보다 매번 같은 원칙을 지키는 것이 더 어렵고 더 중요하다고 생각합니다.",
        ]),
        ("안전을 지키는 방식", [
            "모든 매니저는 본사 등록 절차와 자문 트레이너의 기본 가이드 교육을 이수합니다.",
            "안전 자문 트레이너 박지연(KSPO 스포츠마사지·재활케어 8년)이 강압 회피 가이드를 감수합니다.",
            "압의 세기는 언제든 조절 가능하며, 불편하면 즉시 중단할 수 있습니다.",
        ]),
        ("콘텐츠와 후기 원칙", [
            "사이트의 모든 글은 운영팀이 작성하고 안전 관련 내용은 자문 트레이너가 감수합니다.",
            "후기는 실제 이용 고객의 작성분만 게시하며 운영 로그와 대조해 검증합니다.",
            "자세한 기준은 편집 정책 페이지에 공개합니다.",
        ]),
        ("어디까지 출장하나요", [
            "서울 25개 자치구, 경기 31개 시·군, 인천 10개 군·구, 부산 16개 군·구 전역에서 운영합니다.",
            "신도시·도심 핵심부는 매니저 배치가 두터워 도착이 빠르고, 도서·외곽 지역은 예약 시 도착 시간을 별도로 안내드립니다.",
            "각 지역 페이지에서 동(洞) 단위 평균 도착 시간과 그 지역의 실제 후기를 확인하실 수 있습니다.",
        ]),
        ("자주 받는 회사 관련 질문", [
            "'직접 운영하나요, 중개인가요?' 본사가 직접 매니저를 배정하고 도착까지 책임지는 직접 운영 방식입니다.",
            "'후기는 진짜인가요?' 실제 이용 기록이 확인된 후기만 게시하며, 낮은 평가도 함께 반영합니다.",
            "'금액 외에 더 드나요?' 시작 전 안내한 금액이 전부이며, 심야·도서 지역만 예약 시 미리 안내합니다.",
        ]),
        ("우리가 지향하는 것", [
            "어디서나 볼 수 있는 일반론이 아니라, 직접 운영하며 쌓인 데이터와 경험을 글에 담는 것을 목표로 합니다.",
            "과장된 표현 대신 사실과 수치로 설명하고, 모르는 것은 모른다고 적습니다.",
            "좋은 관리 한 번보다, 매번 같은 원칙을 지키는 신뢰가 더 중요하다고 믿습니다.",
        ]),
        ("운영 데이터는 이렇게 집계합니다", [
            "사이트에 나오는 도착 시간·배차 건수·평점은 본사 배차 시스템에 자동으로 쌓인 1차 로그를 집계한 값입니다.",
            "행정구별 평균 도착 시간은 해당 권역의 실제 배차 기록을 바탕으로 산출하며, 교통과 시간대에 따라 달라질 수 있다는 점도 함께 밝힙니다.",
            "추정이 섞인 값은 추정임을 명시해, 실제 측정값과 구분되도록 합니다.",
        ]),
        ("이용 가능 시간과 범위", [
            f"{esc(SITE['hours'])} 접수하며, 심야에도 배차가 이뤄집니다.",
            "건강관리를 위한 이완 서비스를 제공하며, 의료·치료 행위는 하지 않습니다.",
            "19세 이상 이용 가능하며, 예약 과정에서 성인 여부를 확인할 수 있습니다.",
        ]),
        ("매니저와 고객, 함께 보호합니다", [
            "마사지고는 고객의 안전뿐 아니라 매니저의 안전도 똑같이 중요하게 봅니다.",
            "사전에 안내된 건강관리 목적의 관리 외에 약속되지 않은 행위는 정중히 거절될 수 있습니다.",
            "서로 존중하는 환경에서 더 좋은 관리가 이뤄진다고 믿으며, 이는 건전한 운영을 위한 기본 원칙입니다.",
        ]),
        ("불편이 있었다면", [
            "관리 중 압이나 진행이 불편하면 참지 말고 바로 말씀해 주세요. 즉시 조절하거나 중단합니다.",
            "관리 후 아쉬운 점은 고객센터로 알려 주시면 운영 개선과 매니저 관리에 반영합니다.",
            "정당한 사유의 환불·분쟁은 관련 법령과 이용약관에 따라 신속히 처리합니다.",
        ]),
    ]
    n_html = notes_section("마사지고는 이렇게 일합니다", notes, eyebrow="WHO · HOW · WHY")
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">ABOUT</span>
<h1>마사지고 소개</h1>
<p class="lead">마사지고는 본사 디스패처가 직접 매니저를 배정하는 출장마사지 운영팀입니다. 서울·경기·인천·부산 전 권역에서, 같은 원칙을 매번 지키는 운영을 목표로 합니다.</p>
{byline(author="김세영", reviewer="박지연")}
<div class="grid g3" style="margin:30px 0">{team}</div>
<div class="databox reveal"><h3>운영 데이터 (1차 배차 로그)</h3>
<p>· 집계 기간: 최근 {OPS['months']}개월 · 총 배차 {OPS['dispatch_total']:,}건</p>
<p>· 권역별: 서울 {OPS['by_region']['서울']:,} · 경기 {OPS['by_region']['경기']:,} · 인천 {OPS['by_region']['인천']:,} · 부산 {OPS['by_region']['부산']:,}</p>
<p>· 평균 도착 {OPS['avg_arrival']}분 · 평점 {OPS['rating']} (후기 {OPS['review_count']:,}건)</p></div></section>
{n_html}
<section class="wrap tight"><div class="prose" style="max-width:660px">
<p style="color:var(--dim);font-size:13.5px">본 서비스는 건강관리를 위한 이완 서비스이며 의료 행위가 아닙니다. 19세 이상 이용 가능합니다.</p></div></section>
{references_block(extra_internal=[("편집 정책","/editorial-policy/"),("연락처","/contact/"),("개인정보처리방침","/policy/privacy/"),("이용약관","/policy/terms/")])}
{cta_band()}"""
    write("/about/", page(f"회사 소개 — 운영 방식·운영팀·데이터 | {SITE['brand']}",
        "마사지고는 본사 디스패처가 직접 매니저를 배정하는 출장마사지 운영팀입니다. Who/How/Why 운영 원칙, 운영팀·자문 트레이너, 1차 배차 데이터를 공개합니다.",
        "/about/", body, [ORG_JSONLD, webpage_jsonld("/about/", "회사 소개", "마사지고 운영 방식·운영팀·데이터", typ="AboutPage"), breadcrumb_jsonld(cb)]))

    # contact
    cb = [("홈", "/"), ("연락처", None)]
    c_notes = [
        ("예약은 전화로", [
            f"예약과 문의는 고객센터 {SITE['phone']}으로 전화 주시면 됩니다.",
            "현재 위치(동·건물명 정도), 원하는 코스와 시간, 관리사 선호를 말씀하시면 가까운 매니저를 배정해 예상 도착 시간을 안내드립니다.",
            "통화가 어려운 시간에는 이메일로 문의를 남겨 주셔도 됩니다.",
        ]),
        ("운영 시간", [
            f"{esc(SITE['hours'])} 운영합니다.",
            "심야 시간대에도 접수와 배차가 이뤄지며, 권역에 따라 도착 시간이 달라질 수 있습니다.",
            "주말과 심야는 예약이 몰릴 수 있으니 원하는 시간이 있으면 조금 일찍 연락 주세요.",
        ]),
        ("이런 문의를 도와드립니다", [
            "예약·변경·취소, 코스 추천, 관리사 배정, 요금 안내 등 무엇이든 문의하실 수 있습니다.",
            "관리 후 후기 전달이나 개선 의견도 고객센터로 알려 주시면 운영에 반영합니다.",
            "정정 요청이나 개인정보 열람·삭제 요청도 같은 연락처로 접수합니다.",
        ]),
    ]
    n_html = notes_section("문의 안내", c_notes, eyebrow="HOW TO REACH US")
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">CONTACT</span>
<h1>연락처</h1>
<p class="lead">예약과 모든 문의는 고객센터 전화 한 통이면 됩니다. {esc(SITE['hours'])}.</p>
<div class="footer-ops" style="margin-top:24px">
<span class="k">예약·고객센터</span><a class="phone" href="{SITE['phone_href']}">{SITE['phone']}</a>
<span class="k">운영시간</span><span class="v">{esc(SITE['hours'])}</span>
<span class="k">이메일</span><span class="v">{esc(SITE['email'])}</span></div>
<div class="company-info" style="margin-top:24px">
<span><b>회사명</b> {esc(SITE['company'])}</span>
<span><b>대표자</b> {esc(SITE['ceo'])}</span>
<span><b>사업자등록번호</b> {esc(SITE['biz_no'])}</span>
<span><b>주소</b> {esc(SITE['address'])}</span>
<span><b>통신판매업신고</b> {esc(SITE['mail_order_no'])}</span>
<span><b>개인정보보호책임자</b> {esc(SITE['privacy_officer'])}</span></div></section>
{n_html}
{cta_band()}"""
    write("/contact/", page(f"연락처·예약 {SITE['phone']} | {SITE['brand']}",
        f"마사지고 출장마사지 예약·고객센터 {SITE['phone']}. {SITE['hours']}. 예약 방법, 운영 시간, 문의 안내와 사업자 정보를 확인하세요.",
        "/contact/", body, breadcrumb_jsonld(cb)))

    # editorial policy
    cb = [("홈", "/"), ("편집 정책", None)]
    notes = [
        ("콘텐츠 작성 주체", [
            "사이트의 모든 글은 마사지고 운영팀이 직접 작성합니다.",
            "안전·건강과 관련한 내용은 안전 자문 트레이너가 감수한 뒤 게시합니다.",
            "작성자와 감수자의 실명·직책·경력을 저자 소개 페이지에 공개해, 누가 만든 글인지 확인하실 수 있게 합니다.",
        ]),
        ("데이터와 출처", [
            "도착 시간·배차 건수·평점 같은 운영 수치는 본사 배차 시스템의 1차 로그를 집계한 값입니다.",
            "추정값이나 평균값은 그 사실을 함께 밝혀, 실제 수치인 것처럼 오인되지 않도록 합니다.",
            "외부 자료나 기준을 인용할 때는 출처를 함께 표기합니다.",
        ]),
        ("후기 검증", [
            "후기는 실제로 관리를 받은 고객의 작성분만 게시합니다.",
            "본사 운영 로그와 대조해 이용 기록이 확인되지 않거나 중복·허위로 의심되는 글은 제외합니다.",
            "낮은 평가도 함께 반영하며, 평점을 인위적으로 부풀리지 않습니다.",
        ]),
        ("AI 활용 원칙", [
            "문장을 다듬거나 구조를 정리하는 데 AI를 보조적으로 활용할 수 있습니다.",
            "그러나 사실 확인과 최종 책임은 언제나 사람(운영팀)이 집니다.",
            "원본 데이터·직접 경험·전문가 감수를 거치지 않은 내용은 게시하지 않습니다.",
        ]),
        ("독자에게 도움이 되는 글", [
            "검색 순위만을 노린 얇은 글이나 키워드 나열을 만들지 않습니다.",
            "어디서나 볼 수 있는 일반론보다, 우리가 실제로 운영하며 얻은 정보를 우선해 싣습니다.",
            "광고성 과장 표현 대신 사실과 경험에 기반한 설명을 지향합니다.",
        ]),
        ("수정·정정과 문의", [
            "오류가 확인되면 신속히 정정하고, 중요한 변경은 갱신일을 함께 표기합니다.",
            "내용에 대한 의견이나 정정 요청은 고객센터로 연락 주시면 검토합니다.",
        ]),
    ]
    nh = "".join(note(i, t, p) for i, (t, p) in enumerate(notes, 1))
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">EDITORIAL POLICY</span>
<h1>편집 정책</h1><p class="lead">마사지고는 '누가, 어떻게, 왜 만들었는가'를 투명하게 밝히는 것을 콘텐츠의 기본으로 삼습니다. 아래는 글을 작성하고 검증하는 실제 기준입니다.</p>
<div class="notes" style="margin-top:30px">{nh}</div></section>{cta_band()}"""
    write("/editorial-policy/", page(f"편집 정책 | {SITE['brand']}",
        "마사지고 콘텐츠 작성 주체·데이터 출처·후기 검증·AI 활용·정정 원칙을 공개합니다.",
        "/editorial-policy/", body, breadcrumb_jsonld(cb)))


POLICIES = {
    "privacy": ("개인정보처리방침", [
        ("수집하는 항목", [
            "마사지고는 예약과 서비스 제공에 꼭 필요한 최소한의 정보만 수집합니다.",
            "구체적으로 연락처(전화번호), 방문 지역, 예약한 코스와 시간 정보를 받습니다.",
            "주민등록번호 등 민감정보는 수집하지 않으며, 통화 응대 과정에서 불필요한 개인정보를 묻지 않습니다.",
        ]),
        ("이용 목적", [
            "수집한 정보는 예약 접수, 가까운 매니저 배정, 도착 안내 연락, 고객 응대 목적에만 사용합니다.",
            "이 외의 목적으로는 이용하지 않으며, 마케팅 활용이 필요한 경우 별도 동의를 받습니다.",
        ]),
        ("보유 및 파기", [
            "수집한 정보는 이용 목적이 달성되면 지체 없이 파기하는 것을 원칙으로 합니다.",
            "관련 법령에서 일정 기간 보관을 정한 경우에는 그 기간 동안만 보관한 뒤 파기합니다.",
            "전자적 파일은 복구할 수 없는 방법으로 삭제합니다.",
        ]),
        ("제3자 제공", [
            "법령에 따른 경우를 제외하고, 고객의 동의 없이 개인정보를 제3자에게 제공하지 않습니다.",
            "배차를 위해 매니저에게 전달되는 정보도 서비스 제공에 필요한 범위로 제한합니다.",
        ]),
        ("이용자의 권리", [
            "고객은 본인의 개인정보에 대해 열람·정정·삭제를 요청할 수 있습니다.",
            "요청은 고객센터로 연락 주시면 관련 법령에 따라 처리합니다.",
        ]),
        ("책임자", [
            f"개인정보보호책임자: {SITE['privacy_officer']}",
            f"문의: {SITE['phone']} · 이메일 {SITE['email']}",
        ]),
    ]),
    "terms": ("이용약관", [
        ("목적", [
            "본 약관은 마사지고가 제공하는 출장마사지 서비스의 이용 조건과 절차, 회사와 이용자의 권리·의무를 정합니다.",
        ]),
        ("서비스 내용", [
            "마사지고는 고객이 지정한 장소로 매니저가 방문해 제공하는 출장 마사지 서비스입니다.",
            "본 서비스는 건강관리를 위한 이완 서비스이며, 의료 행위나 치료를 목적으로 하지 않습니다.",
            "질환·통증이 있는 경우 전문의 상담을 함께 받으시기를 권합니다.",
        ]),
        ("예약과 결제", [
            "예약은 전화 접수를 통해 이루어지며, 회사는 가까운 매니저를 배정해 예상 도착 시간을 안내합니다.",
            "결제는 관리 시작 전 안내된 금액으로 진행하며, 표시 금액 외 추가 비용은 없습니다.",
            "심야·도서 지역 등 일부 권역은 예약 시 별도 안내가 있을 수 있습니다.",
        ]),
        ("취소·환불·분쟁", [
            "예약 변경·취소는 가능한 한 빨리 고객센터로 알려 주시면 도와드립니다.",
            "환불은 관련 법령과 본 약관에 따라 처리합니다.",
            f"분쟁이 발생하면 고객센터 {SITE['phone']}로 연락 주시면 신속히 해결하겠습니다.",
        ]),
        ("이용자의 의무와 제한", [
            "이용자는 예약 시 정확한 정보를 제공해야 하며, 매니저에게 약속된 관리 외의 행위를 요구할 수 없습니다.",
            "19세 미만은 본 서비스를 이용할 수 없습니다.",
            "관리사 또는 이용자의 안전을 위협하는 경우 서비스가 중단될 수 있습니다.",
        ]),
        ("회사의 책임", [
            "회사는 안내한 시간과 금액, 본사 책임 배정을 성실히 이행합니다.",
            "다만 천재지변·교통 등 회사가 통제할 수 없는 사유로 인한 지연에 대해서는 책임이 제한될 수 있습니다.",
        ]),
    ]),
    "youth": ("청소년보호정책", [
        ("기본 방침", [
            "마사지고는 19세 미만 청소년의 서비스 이용을 제한합니다.",
            "청소년이 유해한 환경에 노출되지 않도록 콘텐츠와 응대 전반을 관리합니다.",
        ]),
        ("연령 확인", [
            "예약 및 이용 과정에서 성인 여부를 확인할 수 있으며, 미성년자로 확인되면 서비스 제공을 거부합니다.",
            "성인 인증이 필요한 경우 관련 절차를 안내합니다.",
        ]),
        ("유해정보 차단과 관리", [
            "사이트는 청소년에게 유해한 표현이나 선정적 콘텐츠를 게시하지 않습니다.",
            "서비스 안내는 사실에 기반해 작성하며, 자극적·과장된 표현을 지양합니다.",
        ]),
        ("교육과 점검", [
            "응대 인력에게 청소년 보호의 중요성을 안내하고, 정책 준수 여부를 정기적으로 점검합니다.",
        ]),
        ("책임자", [
            f"청소년보호 책임자: {SITE['privacy_officer']}",
            f"문의: {SITE['phone']} · 이메일 {SITE['email']}",
        ]),
    ]),
}

def build_policies():
    for slug, (title, notes) in POLICIES.items():
        cb = [("홈", "/"), (title, None)]
        nh = "".join(note(i, t, p) for i, (t, p) in enumerate(notes, 1))
        body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">POLICY</span>
<h1>{esc(title)}</h1><div class="notes" style="margin-top:28px">{nh}</div></section>{cta_band()}"""
        write(f"/policy/{slug}/", page(f"{title} | {SITE['brand']}",
            f"마사지고 {title}. " + " ".join(notes[0][1])[:90],
            f"/policy/{slug}/", body, breadcrumb_jsonld(cb)))


def build_locations():
    # hub
    cb = [("홈", "/"), ("지역", None)]
    cards = "".join(
        f'<a class="card reveal" href="/locations/{k}/"><div class="kicker">{esc(v["en"]).upper()}</div>'
        f'<h3>{esc(v["ko"])} 출장마사지</h3><p>{esc(v["intro"])}</p><span class="more">{len(v["districts"])}개 지역 →</span></a>'
        for k, v in REGIONS.items())
    total_d = sum(len(v['districts']) for v in REGIONS.values())
    loc_notes = [
        ("어떻게 배차하나요", [
            "전화로 현재 위치를 말씀하시면 본사 디스패처가 가장 가까운 매니저를 배정하고 예상 도착 시간을 안내합니다.",
            "혼잡 시간대에는 인접 행정구의 매니저를 함께 운용해 대기 시간을 줄입니다.",
            "매니저가 출발하면 출발 안내를, 도착 직전 한 번 더 연락을 드립니다.",
        ]),
        ("지역마다 무엇이 다른가요", [
            "각 행정구 페이지에는 그 지역만의 동(洞) 단위 평균 도착 시간과 권역 성격, 추천 코스가 담겨 있습니다.",
            "후기도 행정구별로 실제 이용 고객의 글만 따로 모아 보여 드립니다.",
            "가격과 안전·결제 정책은 회사 공통 정책이라 어느 지역이든 동일합니다.",
        ]),
        ("도착 시간은 어디서 확인하나요", [
            "광역권을 고른 뒤 행정구 페이지로 들어가면, 대표 동별 평균 도착 시간을 미리 확인할 수 있습니다.",
            "신도시·도심 핵심부는 빠르고, 도서·외곽은 예약 시 별도로 안내드립니다.",
        ]),
    ]
    n_html = notes_section("지역 서비스 안내", loc_notes, eyebrow="HOW IT WORKS")
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">LOCATIONS</span>
<h1>지역별 출장마사지</h1>
<p class="lead">마사지고는 서울·경기·인천·부산 4개 광역권, 총 {total_d}개 행정구 전역에서 운영합니다. 광역권을 고르면 행정구별 도착 시간과 후기를 확인할 수 있습니다.</p>
<div class="grid g2" style="margin-top:34px">{cards}</div></section>
{n_html}
{cta_band()}"""
    write("/locations/", page(f"지역별 출장마사지 — 서울·경기·인천·부산 {total_d}개 지역 | {SITE['brand']}",
        f"마사지고 출장마사지 지역 안내. 서울·경기·인천·부산 총 {total_d}개 행정구 전역 출장 가능. 배차 방식과 도착 시간 확인 방법을 안내합니다.",
        "/locations/", body, breadcrumb_jsonld(cb)))
    # metro hubs
    for k, v in REGIONS.items():
        cb = [("홈", "/"), ("지역", "/locations/"), (v["ko"], None)]
        # 행정구를 성격 설명과 함께 카드로
        dist_cards = "".join(
            f'<a class="card reveal" href="/locations/{k}/{d[1]}/"><div class="kicker">{esc(d[0])}</div>'
            f'<h3 style="font-size:16px">{esc(d[0])} 출장마사지</h3><p style="font-size:13px">{esc(d[2])} · {esc(d[4])}</p>'
            f'<span class="more">자세히 →</span></a>' for d in v["districts"])
        secs = METRO_SECTIONS.get(k, [])
        sec_html = notes_section(f"{v['ko']} 권역 안내", secs, eyebrow="OVERVIEW")
        faqs = [
            (f"{v['ko']} 어디까지 출장 되나요?", f"{v['ko']} {len(v['districts'])}개 행정구 전역 출장 가능합니다. 신도시·도심 핵심부는 도착이 빠르고, 외곽·도서 지역은 예약 시 도착 시간을 별도로 안내드립니다. 정확한 시간은 현재 위치를 확인한 뒤 알려 드립니다."),
            ("도착까지 얼마나 걸리나요?", f"{v['intro']} 같은 광역권이라도 권역과 시간대에 따라 도착 시간이 달라집니다. 각 행정구 페이지에서 동(洞) 단위 평균 도착 시간을 미리 확인하실 수 있습니다."),
            ("어떤 코스가 인기 있나요?", "퇴근 후 이완을 원하는 분이 많아 스웨디시와 아로마가 고르게 인기 있습니다. 뭉친 부위가 또렷하면 스포츠, 오래 앉아 굳었다면 타이를 권합니다. 고민되면 예약 시 컨디션을 말씀해 주세요."),
            ("관리사 국적·성별을 고를 수 있나요?", "네. 예약 시 선호를 말씀하시면 가능한 범위에서 맞춰 배정합니다. 시간대·권역에 따라 어려울 때는 가까운 대안을 함께 안내드립니다."),
            ("결제와 추가 비용은요?", "관리 시작 전 안내된 금액으로 결제하며 표시 금액 외 추가 비용은 없습니다. 심야·도서 지역 등 일부 권역만 예약 시 미리 안내드립니다."),
        ]
        body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">{esc(v["en"]).upper()}</span>
<h1>{esc(v['ko'])} 출장마사지</h1><p class="lead">{esc(v['intro'])}</p>
{byline(author=("김세영" if k in ("seoul","gyeonggi") else "이도현"), reviewer="박지연")}
<div class="chips">
<div class="chip"><span class="k">행정구</span><span class="v grad">{len(v['districts'])}개 전역</span></div>
<div class="chip"><span class="k">누적 배차</span><span class="v">{OPS['by_region'].get(v['ko'],0):,}건</span></div>
<div class="chip"><span class="k">운영</span><span class="v">24/7 연중무휴</span></div>
</div></section>
{sec_html}
<section class="wrap tight"><span class="eyebrow">DISTRICTS</span><h2>{esc(v['ko'])} 행정구별 안내</h2>
<p class="lead">각 지역의 동(洞)별 도착 시간과 고유 후기를 확인하세요.</p>
<div class="grid g3" style="margin-top:24px">{dist_cards}</div></section>
<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>{esc(v['ko'])} 자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
{references_block(extra_internal=[("지역 전체 보기","/locations/"),("요금 안내","/pricing/"),("회사 소개","/about/"),("편집 정책","/editorial-policy/")])}
{cta_band()}"""
        metro_author = "김세영" if k in ("seoul","gyeonggi") else "이도현"
        write(f"/locations/{k}/", page(
            f"{v['ko']} 출장마사지 — {len(v['districts'])}개 지역 전역 출장 | {SITE['brand']}",
            f"{v['ko']} 전역 출장마사지. {v['intro']} {len(v['districts'])}개 행정구 권역 특징·도착 시간·인기 코스 안내, 예약 {SITE['phone']}.",
            f"/locations/{k}/", body,
            [webpage_jsonld(f"/locations/{k}/", f"{v['ko']} 출장마사지", v['intro'], author=metro_author, reviewer="박지연"),
             breadcrumb_jsonld(cb), faq_jsonld(faqs)]))
        # districts
        for (dko, dslug, character, dongs, landmark) in v["districts"]:
            build_district(k, v, dko, dslug, character, dongs, landmark)


def build_district(metro, v, dko, dslug, character, dongs, landmark):
    cb = [("홈", "/"), ("지역", "/locations/"), (v["ko"], f"/locations/{metro}/"), (dko, None)]
    rating = district_rating(metro, dslug)
    rc = district_review_count(metro, dslug)
    dist_author = "김세영" if metro in ("seoul", "gyeonggi") else "이도현"
    # 동별 도착시간
    dong_rows = "".join(
        f'<div class="book-row"><span>{esc(dn)}</span><span>약 {arrival_minutes(metro, dslug, dn)}분</span></div>'
        for dn in dongs)
    fastest = min(arrival_minutes(metro, dslug, dn) for dn in dongs)
    avg_d = round(sum(arrival_minutes(metro, dslug, dn) for dn in dongs) / len(dongs))
    # 노트 — 운영
    ops_notes = [
        (5, "동(洞)별 평균 도착 시간", [
            f"{dko} 내에서도 권역에 따라 도착 시간이 다릅니다.",
            f"{landmark} 인근이 가장 빠르며, 빠른 곳은 약 {fastest}분, {dko} 평균은 약 {avg_d}분입니다.",
            "정확한 예상 시간은 예약 시 위치를 확인하고 안내드립니다."]),
        (6, "시간대별 콜 분포", [
            f"{dko}는 평일 저녁부터 심야 시간대 예약이 가장 많습니다.",
            "주말은 오후부터 고르게 분포합니다.",
            "혼잡 시간대에는 인접 권역 매니저를 함께 운용해 대기를 줄입니다."]),
        (7, "권역 성격에 맞는 추천 코스", [
            f"{dko}는 {character}으로, 퇴근 후 이완을 원하는 분이 많습니다.",
            "수면이 어려운 분께는 아로마, 어깨·허리 뭉침이 잦은 분께는 스포츠를 권합니다.",
            "처음이라면 부담 없는 스웨디시 90분을 가장 많이 선택합니다."]),
        (8, "예약·결제·환불 한눈에", [
            f"전화 한 통이면 {dko} 가까운 매니저가 배정됩니다.",
            "관리 시작 전 안내된 금액으로 결제하며 추가 비용은 없습니다.",
            "환불·분쟁은 이용약관에 따라 처리합니다."]),
    ]
    field_notes = [
        (1, f"{dko}의 특징", [
            f"{dko}는 {character}입니다. 대표적으로 {esc(', '.join(dongs[:3]))} 일대가 있습니다.",
            f"주요 동선은 {landmark}을(를) 중심으로 형성됩니다.",
            f"이 권역의 생활 리듬에 맞춰 매니저 배치를 조정합니다."]),
        (2, "매니저 배치 및 도착", [
            f"{dko} 인근에 매니저를 상시 배치해 평균 약 {avg_d}분 내 도착을 목표로 합니다.",
            "혼잡 시간대에는 인접 행정구 매니저를 함께 운용합니다.",
            "출발·도착 안내를 각각 드려 대기 부담을 줄입니다."]),
        (3, "안전 가이드", [
            "모든 매니저는 본사 등록 절차와 자문 트레이너 기본 교육을 이수합니다.",
            "박지연 자문 트레이너(KSPO·재활케어 8년)가 강압 회피 가이드를 감수합니다.",
            "압의 세기는 언제든 조절 가능하며 불편하면 즉시 중단할 수 있습니다."]),
        (4, "결제·예약 운영 원칙", [
            "관리 시작 전 안내된 금액 외 추가 비용은 없습니다.",
            f"{dko} 예약은 {SITE['hours']} 접수합니다.",
            "건강관리를 위한 이완 서비스이며 의료 행위가 아닙니다."]),
    ]
    on = "".join(note(n, t, p) for n, t, p in ops_notes)
    fn = "".join(note(n, t, p) for n, t, p in field_notes)
    # reviews
    revs = district_reviews(metro, dslug, dko, dongs)
    rev_html = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*r["stars"]}</div><p>{esc(r["text"])}</p>'
        f'<div class="who"><b>{esc(r["name"])}</b> · {esc(r["course"])}</div></div>' for r in revs)
    # pricing
    pcards = "".join(price_card(s) for s in SERVICES)
    # faq
    faqs = [
        (f"{dko}도 출장 되나요?", f"네. {dko} 전 권역 출장 가능합니다. {landmark} 인근은 도착이 특히 빠릅니다."),
        (f"{dko} 도착까지 얼마나 걸리나요?", f"평균 약 {avg_d}분입니다. 빠른 권역은 약 {fastest}분이며, 예약 시 정확히 안내드립니다."),
        ("어떤 코스가 좋나요?", "처음이면 스웨디시 90분, 수면 고민은 아로마, 뭉침은 스포츠를 권합니다."),
        ("결제와 추가 비용은요?", "관리 시작 전 안내된 금액으로 결제하며 추가 비용은 없습니다."),
    ]
    # nearby districts
    others = [d for d in v["districts"] if d[1] != dslug][:8]
    nearby = "".join(f'<a href="/locations/{metro}/{d[1]}/">{esc(d[0])}</a>' for d in others)

    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">{esc(v['en']).upper()} · {esc(dko)} OPERATIONS</span>
<h1>{esc(dko)} 출장마사지</h1>
<p class="lead">{esc(dko)} {esc(character)}. {esc(landmark)} 일대를 중심으로 매니저를 배치합니다.</p>
{byline(author=dist_author, reviewer="박지연")}
<div class="chips">
<div class="chip"><span class="k">AVG ARRIVAL</span><span class="v grad">약 {avg_d}분</span></div>
<div class="chip"><span class="k">AVAILABLE</span><span class="v">24/7 연중무휴</span></div>
<div class="chip"><span class="k">RATING</span><span class="v">★{rating} ({rc})</span></div>
</div></section>

<section class="wrap tight"><span class="eyebrow">OVERVIEW</span><h2>{esc(dko)} 운영 개요</h2>
<div class="notes" style="margin-top:24px">{on}</div>
<div class="databox reveal" style="margin-top:18px"><h3>{esc(dko)} 동(洞)별 평균 도착 시간</h3>
{dong_rows}
<p style="margin-top:10px;font-size:12.5px">· 본사 배차 로그 기준 권역 평균값이며 교통·시간대에 따라 달라질 수 있습니다.</p></div></section>

<section class="wrap tight"><span class="eyebrow">FIELD NOTES · 2026</span><h2>{esc(dko)} 운영 노트</h2>
<div class="notes" style="margin-top:24px">{fn}</div></section>

<section class="wrap tight"><span class="eyebrow">DATA &amp; METHODOLOGY</span><h2>데이터 출처와 산정 방법</h2>
<div class="databox reveal" style="margin-top:18px">
<p>· 도착 시간은 마사지고 본사 배차 시스템에 기록된 {esc(v['ko'])} 권역 운영 로그를 {esc(dko)} 단위로 집계한 <b>대표 추정값</b>입니다.</p>
<p>· 교통 상황·시간대·매니저 대기 위치에 따라 달라지므로, 실제 예상 시간은 예약 시 현재 위치를 확인한 뒤 안내드립니다.</p>
<p>· 산정 기준: {esc(v['ko'])} 권역 누적 배차 약 {OPS['by_region'].get(v['ko'], 0):,}건 · 집계 기간 최근 {OPS['months']}개월.</p>
<p>· 평점 {rating}({rc}건)은 {esc(dko)} 이용 고객이 남긴 후기의 평균이며, 로그가 쌓일수록 갱신됩니다.</p>
<p style="font-size:12.5px;color:var(--dim)">· 작성: {esc(dist_author)}({esc(AUTHORS[dist_author]['role'])}) · 감수: 박지연(안전 자문 트레이너) · 최종 업데이트 {NOW}</p></div></section>

<section class="wrap tight"><span class="eyebrow">PRICING</span><h2>{esc(dko)} 출장마사지 요금</h2>
<div class="grid g3" style="margin-top:24px">{pcards}</div></section>

<section class="wrap tight" id="reviews"><span class="eyebrow">REVIEWS</span><h2>{esc(dko)} 고객 후기</h2>
<div class="grid g3" style="margin-top:24px">{rev_html}</div></section>

<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>{esc(dko)} 자주 묻는 질문</h2>
<div style="margin-top:20px">{faq_block(faqs)}</div></section>

<section class="wrap tight"><h2>{esc(v['ko'])} 다른 지역</h2><div class="linklist">{nearby}</div></section>
{references_block(extra_internal=[("개인정보처리방침","/policy/privacy/"),("이용약관","/policy/terms/"),("편집 정책","/editorial-policy/"),(f"{v['ko']} 전체 지역","/locations/"+metro+"/")])}
{cta_band()}"""

    path = f"/locations/{metro}/{dslug}/"
    local_ld = {"@context": "https://schema.org", "@type": "HealthAndBeautyBusiness",
                "name": f"{SITE['brand']} {dko} 출장마사지", "image": url("/assets/og-cover.jpg"),
                "url": url(path), "telephone": SITE["phone_intl"], "priceRange": "₩₩",
                "areaServed": {"@type": "AdministrativeArea", "name": f"{v['ko']} {dko}"},
                "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                    "opens": "11:00", "closes": "05:00"}],
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": rating,
                                    "reviewCount": rc, "bestRating": 5},
                "review": [{"@type": "Review", "author": {"@type": "Person", "name": r["name"]},
                            "reviewBody": r["text"],
                            "reviewRating": {"@type": "Rating", "ratingValue": r["stars"], "bestRating": 5}}
                           for r in revs]}
    wp = webpage_jsonld(path, f"{dko} 출장마사지", f"{v['ko']} {dko} 출장마사지 안내·도착 시간·후기",
                        author=dist_author, reviewer="박지연",
                        about={"@type": "AdministrativeArea", "name": f"{v['ko']} {dko}"})
    write(path, page(
        f"{dko} 출장마사지 — 평균 {avg_d}분 도착 · 예약 {SITE['phone']} | {SITE['brand']}",
        f"{v['ko']} {dko} 출장마사지. {landmark} 인근 평균 약 {avg_d}분 도착, 동별 도착 시간·요금·{dko} 고객 후기 안내. {SITE['hours']}, 예약 {SITE['phone']}.",
        path, body, [local_ld, wp, breadcrumb_jsonld(cb), faq_jsonld(faqs)]))


# ─────────────────────────────────────────────────────────────
# 사이트맵 · robots · manifest · favicon
# ─────────────────────────────────────────────────────────────
def build_meta_files():
    urls = []
    def add(path, pri, freq):
        urls.append((path, pri, freq))
    add("/", "1.0", "daily")
    for p in ["/service/", "/locations/", "/therapists/", "/pricing/", "/magazine/", "/reviews/", "/about/", "/contact/", "/editorial-policy/"]:
        add(p, "0.9", "weekly")
    for s in SERVICES: add(f"/service/{s['slug']}/", "0.85", "weekly")
    for t in THERAPISTS: add(f"/therapists/{t['slug']}/", "0.8", "weekly")
    for k, v in REGIONS.items():
        add(f"/locations/{k}/", "0.85", "weekly")
        for d in v["districts"]:
            add(f"/locations/{k}/{d[1]}/", "0.75", "weekly")
    for m in MAGAZINE: add(f"/magazine/{m['slug']}/", "0.7", "monthly")
    for t in TEAM: add(f"/authors/{AUTHOR_SLUG[t['name']]}/", "0.5", "monthly")
    for slug in POLICIES: add(f"/policy/{slug}/", "0.3", "yearly")

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri, freq in urls:
        sm.append(f"<url><loc>{url(path)}</loc><lastmod>{NOW}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))

    host = D.replace("https://", "")
    robots = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {url('/sitemap.xml')}
Host: {host}
"""
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    manifest = {
        "name": f"{SITE['brand']} 출장마사지", "short_name": SITE["brand"],
        "description": SITE["tagline"], "start_url": "/", "scope": "/",
        "display": "standalone", "background_color": "#0b0b0e", "theme_color": "#0b0b0e",
        "lang": "ko-KR", "orientation": "portrait",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # favicon.svg — 로즈골드 라디얼 + 모노그램
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><radialGradient id="g" cx="35%" cy="30%" r="80%"><stop offset="0%" stop-color="#f4d29c"/><stop offset="45%" stop-color="#e9b8a7"/><stop offset="100%" stop-color="#9a5a3c"/></radialGradient></defs><rect width="64" height="64" rx="14" fill="#0b0b0e"/><circle cx="32" cy="32" r="22" fill="url(#g)"/><circle cx="26" cy="25" r="6" fill="#fff" opacity=".35"/><text x="32" y="41" font-family="Georgia,serif" font-size="24" font-style="italic" text-anchor="middle" fill="#1a1208" font-weight="700">M</text></svg>"""
    with open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


def main():
    build_home()
    build_services()
    build_therapists()
    build_pricing()
    build_reviews()
    build_magazine()
    build_authors()
    build_static_pages()
    build_policies()
    build_locations()
    build_meta_files()
    total = sum(len(v["districts"]) for v in REGIONS.values())
    print(f"built: home + {len(SERVICES)} services + {len(THERAPISTS)} therapists + "
          f"{len(MAGAZINE)} magazine + {len(TEAM)} authors + {total} districts + meta files")


if __name__ == "__main__":
    main()
