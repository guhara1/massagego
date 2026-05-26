# -*- coding: utf-8 -*-
"""마사지고 정적 사이트 생성기 — 순수 HTML + 인라인 CSS/JS, 의존성 0."""

import os, json, html, datetime
from data import (SITE, OPS, TEAM, SERVICES, THERAPISTS, MAGAZINE, FAQ_MAIN,
                  REVIEWS_MAIN, REGIONS, arrival_minutes, district_rating,
                  district_review_count, district_reviews)

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

ORG_JSONLD = {
    "@context": "https://schema.org", "@type": "Organization",
    "@id": url("/#org"), "name": SITE["brand"], "legalName": SITE["company"],
    "url": D, "telephone": SITE["phone_intl"], "email": SITE["email"],
    "logo": url("/assets/logo.png"), "image": url("/assets/og-cover.jpg"),
    "description": SITE["tagline"],
    "address": {"@type": "PostalAddress", "addressCountry": "KR", "addressLocality": "서울", "streetAddress": SITE["address"]},
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
<p class="lead">구글 'Who/How/Why' 원칙에 따라 운영 주체와 방식, 이유를 투명하게 공개합니다.</p>
<div class="grid g3" style="margin:30px 0">{team_html}</div>
<div class="notes">{note_html}</div>
<div class="databox reveal" style="margin-top:24px"><h3>Data &amp; Methodology</h3>
<p>아래 수치는 마사지고 본사 배차 시스템의 1차 운영 로그를 집계한 값입니다.</p>
<p>· 집계 기간: 최근 {OPS['months']}개월 · 총 배차 {OPS['dispatch_total']:,}건</p>
<p>· 권역별: 서울 {OPS['by_region']['서울']:,} · 경기 {OPS['by_region']['경기']:,} · 인천 {OPS['by_region']['인천']:,} · 부산 {OPS['by_region']['부산']:,}</p>
<p>· 평균 도착 {OPS['avg_arrival']}분 · 평점 {OPS['rating']} (후기 {OPS['review_count']:,}건)</p></div></section>

<section class="wrap tight" id="faq"><span class="eyebrow">FAQ</span><h2>자주 묻는 질문</h2>
<div style="margin-top:24px">{faq_block(FAQ_MAIN)}</div></section>

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
               "image": url("/assets/og-cover.jpg"),
               "author": [{"@type": "Person", "name": t["name"], "jobTitle": t["role"],
                           "url": url(f"/authors/{AUTHOR_SLUG[t['name']]}/")} for t in TEAM],
               "reviewedBy": {"@type": "Person", "name": "박지연", "jobTitle": "안전 자문 트레이너"},
               "publisher": {"@id": url("/#org")}, "datePublished": "2026-01-05", "dateModified": NOW}
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
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">SERVICES</span>
<h1>다섯 가지 시그니처 코스</h1>
<p class="lead">스웨디시·아로마·타이·로미로미·스포츠. 각 코스의 특징과 추천 상황을 확인하세요.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div></section>{cta_band()}"""
    write("/service/", page(f"출장마사지 서비스 — 5종 코스 안내 | {SITE['brand']}",
        "스웨디시·아로마·타이·로미로미·스포츠 5종 출장마사지 코스를 비교하세요. 컨디션별 추천과 가격을 안내합니다.",
        "/service/", body, breadcrumb_jsonld(cb)))
    # detail
    for s in SERVICES:
        cb = [("홈", "/"), ("서비스", "/service/"), (s["ko"], None)]
        ln = "".join(f"<p>{esc(p)}</p>" for p in s["long"])
        dn = "".join(f"<p>{esc(p)}</p>" for p in s["deep"])
        rows = price_card(s)
        faqs = [
            (f"{s['ko']} 마사지는 어떤 분께 맞나요?", s["summary"]),
            ("시간은 어떻게 고르나요?", "60·90·120분 중 선택하실 수 있습니다. 처음이면 90분을 가장 많이 권합니다."),
            ("출장 지역은 어디까지 되나요?", "서울·경기·인천·부산 전 권역 가능합니다. 예약 시 지역을 말씀해 주세요."),
            ("결제와 추가 비용은요?", "관리 시작 전 안내된 금액으로 결제하며 추가 비용은 없습니다."),
        ]
        other = "".join(f'<a href="/service/{o["slug"]}/">{o["ko"]}</a>' for o in SERVICES if o["slug"] != s["slug"])
        body = f"""<section class="wrap">{crumb(cb)}
<span class="eyebrow">{esc(s['kicker'])}</span><h1>{esc(s['ko'])} 출장마사지</h1>
<p class="lead">{esc(s['summary'])}</p>
<div class="prose" style="margin-top:30px;max-width:660px">{ln}</div></section>
<section class="wrap tight"><h2>관리는 이렇게 진행됩니다</h2>
<div class="prose" style="margin-top:18px;max-width:660px">{dn}</div></section>
<section class="wrap tight"><h2>{esc(s['ko'])} 요금</h2>
<div class="grid g3" style="margin-top:24px">{rows}</div>
<p style="margin-top:14px;color:var(--dim);font-size:13px">표시 금액 외 추가 비용은 없습니다.</p></section>
<section class="wrap tight"><h2>다른 코스</h2><div class="linklist">{other}</div></section>
<section class="wrap tight"><h2>자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
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
            [service_ld, breadcrumb_jsonld(cb), faq_jsonld(faqs)]))


def build_therapists():
    cards = "".join(
        f'<a class="card reveal" href="/therapists/{t["slug"]}/"><div class="kicker">{esc(t["en"]).upper()}</div>'
        f'<h3>{esc(t["ko"])} 관리사</h3><p>{esc(t["desc"])}</p><span class="more">자세히 →</span></a>'
        for t in THERAPISTS)
    cb = [("홈", "/"), ("관리사", None)]
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">THERAPISTS</span>
<h1>관리사 국적 안내</h1><p class="lead">국적별 강점이 다릅니다. 선호가 있으면 예약 시 말씀해 주세요.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div></section>{cta_band()}"""
    write("/therapists/", page(f"관리사 국적 안내 — 6개국 | {SITE['brand']}",
        "한국·중국·태국·베트남·러시아·일본 관리사의 국적별 강점을 안내합니다. 선호 국적·성별 배정이 가능합니다.",
        "/therapists/", body, breadcrumb_jsonld(cb)))
    for t in THERAPISTS:
        cb = [("홈", "/"), ("관리사", "/therapists/"), (t["ko"], None)]
        pts = "".join(f'<div class="chip"><span class="k">강점</span><span class="v">{esc(p)}</span></div>' for p in t["points"])
        other = "".join(f'<a href="/therapists/{o["slug"]}/">{o["ko"]}</a>' for o in THERAPISTS if o["slug"] != t["slug"])
        faqs = [("국적을 지정해 예약할 수 있나요?", "네. 예약 시 선호 국적을 말씀하시면 가능한 범위에서 배정합니다."),
                ("성별도 고를 수 있나요?", "네. 선호 성별을 함께 말씀해 주세요."),
                ("어떤 코스와 잘 맞나요?", t["desc"])]
        body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">{esc(t['en']).upper()} THERAPIST</span>
<h1>{esc(t['ko'])} 관리사</h1><p class="lead">{esc(t['desc'])}</p>
<div class="chips">{pts}</div></section>
<section class="wrap tight"><h2>다른 국적</h2><div class="linklist">{other}</div></section>
<section class="wrap tight"><h2>자주 묻는 질문</h2><div style="margin-top:20px">{faq_block(faqs)}</div></section>
{cta_band()}"""
        write(f"/therapists/{t['slug']}/", page(
            f"{t['ko']} 관리사 출장마사지 | {SITE['brand']}",
            f"{t['ko']} 관리사 안내. {t['desc']} 선호 국적·성별 배정 가능, 예약 {SITE['phone']}.",
            f"/therapists/{t['slug']}/", body, [breadcrumb_jsonld(cb), faq_jsonld(faqs)]))


def build_pricing():
    cb = [("홈", "/"), ("요금", None)]
    cards = "".join(price_card(s) for s in SERVICES)
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">PRICING</span>
<h1>요금 안내</h1><p class="lead">모든 코스 60·90·120분 기준입니다. 표시 금액 외 추가 비용은 없습니다.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div>
<div class="databox reveal" style="margin-top:28px"><h3>결제 안내</h3>
<p>· 관리 시작 전 안내된 금액으로 결제합니다.</p>
<p>· 심야·도서 지역 등 일부 권역은 예약 시 별도 안내드립니다.</p>
<p>· 환불·분쟁은 이용약관에 따라 처리합니다.</p></div></section>{cta_band()}"""
    write("/pricing/", page(f"출장마사지 요금표 — 코스별 가격 | {SITE['brand']}",
        "스웨디시·아로마·타이·로미로미·스포츠 출장마사지 요금표. 60·90·120분 가격을 한눈에 비교하세요. 추가 비용 없음.",
        "/pricing/", body, breadcrumb_jsonld(cb)))


def build_reviews():
    cb = [("홈", "/"), ("후기", None)]
    # 집계 후기 = 메인 + 대표 구 몇 개
    items = list(REVIEWS_MAIN)
    sample = district_reviews("seoul", "gangnam", "강남구", ["역삼동","삼성동","논현동"])
    for r in sample:
        items.append({"name": r["name"], "area": "서울 강남", "course": r["course"], "stars": r["stars"], "text": r["text"]})
    rev_html = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*r["stars"]}</div><p>{esc(r["text"])}</p>'
        f'<div class="who"><b>{esc(r["name"])}</b> · {esc(r["area"])} · {esc(r["course"])}</div></div>'
        for r in items)
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">REVIEWS</span>
<h1>고객 후기</h1><p class="lead">실제 이용 고객이 남긴 후기만 게시하며 운영 로그와 대조해 검증합니다. 평점 {OPS['rating']} · {OPS['review_count']:,}건.</p>
<div class="grid g3" style="margin-top:30px">{rev_html}</div></section>{cta_band()}"""
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
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">MAGAZINE</span>
<h1>매거진</h1><p class="lead">출장마사지를 처음 받는 분과 코스 선택이 고민인 분을 위한 운영팀의 안내 글입니다.</p>
<div class="grid g3" style="margin-top:34px">{cards}</div></section>{cta_band()}"""
    write("/magazine/", page(f"매거진 — 출장마사지 가이드 | {SITE['brand']}",
        "출장마사지 첫 이용 가이드, 컨디션별 코스 선택, 안전 원칙까지. 마사지고 운영팀이 직접 작성한 안내 글.",
        "/magazine/", body, breadcrumb_jsonld(cb)))
    for m in MAGAZINE:
        cb = [("홈", "/"), ("매거진", "/magazine/"), (m["title"], None)]
        toc = "".join(f'<a href="#s{i}">{esc(h)}</a>' for i, h in enumerate(m["toc"], 1))
        sections = ""
        for i, (h, paras) in enumerate(m["body"], 1):
            ps = "".join(f"<p>{esc(p)}</p>" for p in paras)
            sections += f'<h2 id="s{i}">{esc(h)}</h2>{ps}'
        a = AUTHORS[m["author"]]
        body = f"""<section class="wrap" style="max-width:760px">{crumb(cb)}
<span class="eyebrow">{esc(m['date'])}</span><h1 style="font-size:clamp(30px,4.5vw,48px)">{esc(m['title'])}</h1>
<p class="lead">{esc(m['desc'])}</p>
<p style="margin-top:14px;font-size:13px;color:var(--dim)">글 · <a href="/authors/{AUTHOR_SLUG[m['author']]}/" style="color:var(--gold)">{esc(m['author'])}</a> · {esc(a['role'])}</p>
<div class="toc"><span class="label">목차</span>{toc}</div>
<div class="prose">{sections}</div>
<div class="linklist" style="margin-top:40px">{"".join(f'<a href="/magazine/{o["slug"]}/">{esc(o["title"][:18])}…</a>' for o in MAGAZINE if o["slug"]!=m["slug"])}</div>
</section>{cta_band()}"""
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": m["title"],
              "description": m["desc"], "inLanguage": "ko-KR", "image": url("/assets/og-cover.jpg"),
              "datePublished": m["date"], "dateModified": m["date"],
              "author": {"@type": "Person", "name": m["author"], "jobTitle": a["role"],
                         "url": url(f"/authors/{AUTHOR_SLUG[m['author']]}/")},
              "publisher": {"@id": url("/#org")},
              "mainEntityOfPage": url(f"/magazine/{m['slug']}/")}
        write(f"/magazine/{m['slug']}/", page(
            f"{m['title']} | {SITE['brand']} 매거진",
            m["desc"], f"/magazine/{m['slug']}/", body, [ld, breadcrumb_jsonld(cb)]))


def build_authors():
    for t in TEAM:
        slug = AUTHOR_SLUG[t["name"]]
        cb = [("홈", "/"), ("저자", None), (t["name"], None)]
        wrote = [m for m in MAGAZINE if m["author"] == t["name"]]
        wl = "".join(f'<a href="/magazine/{m["slug"]}/">{esc(m["title"])}</a>' for m in wrote)
        wl_html = f'<h2>작성한 글</h2><div class="linklist">{wl}</div>' if wrote else ""
        body = f"""<section class="wrap" style="max-width:760px">{crumb(cb)}
<span class="eyebrow">AUTHOR · {esc(t['role'])}</span><h1>{esc(t['name'])}</h1>
<p class="lead">{esc(t['bio'])}</p>
<div class="prose" style="margin-top:24px">
<p>마사지고 운영팀의 일원으로, 실명과 책임 영역을 공개합니다. 본 사이트의 콘텐츠는 운영 경험과 1차 배차 데이터를 바탕으로 작성·감수됩니다.</p>
</div>
{wl_html}</section>{cta_band()}"""
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
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">ABOUT</span>
<h1>마사지고 소개</h1>
<p class="lead">마사지고는 본사 디스패처가 직접 매니저를 배정하는 출장마사지 운영팀입니다. 서울·경기·인천·부산 전 권역에서 운영합니다.</p>
<div class="grid g3" style="margin:30px 0">{team}</div>
<div class="databox reveal"><h3>운영 데이터</h3>
<p>· 최근 {OPS['months']}개월 총 배차 {OPS['dispatch_total']:,}건</p>
<p>· 평균 도착 {OPS['avg_arrival']}분 · 평점 {OPS['rating']} (후기 {OPS['review_count']:,}건)</p></div>
<div class="prose" style="margin-top:24px;max-width:660px">
<p>모든 매니저는 본사 등록 절차와 자문 트레이너 기본 교육을 이수합니다. 후기는 실제 이용 고객의 작성분만 게시하며 운영 로그와 대조해 검증합니다.</p>
<p>본 서비스는 건강관리를 위한 이완 서비스이며 의료 행위가 아닙니다.</p></div>
</section>{cta_band()}"""
    write("/about/", page(f"회사 소개 | {SITE['brand']}",
        "마사지고는 본사 디스패처가 직접 매니저를 배정하는 출장마사지 운영팀입니다. 운영팀·자문 트레이너와 운영 데이터를 공개합니다.",
        "/about/", body, [ORG_JSONLD, breadcrumb_jsonld(cb)]))

    # contact
    cb = [("홈", "/"), ("연락처", None)]
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">CONTACT</span>
<h1>연락처</h1>
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
<span><b>개인정보보호책임자</b> {esc(SITE['privacy_officer'])}</span></div>
</section>{cta_band()}"""
    write("/contact/", page(f"연락처·예약 {SITE['phone']} | {SITE['brand']}",
        f"마사지고 출장마사지 예약·고객센터 {SITE['phone']}. {SITE['hours']}. 사업자 정보와 연락처를 안내합니다.",
        "/contact/", body, breadcrumb_jsonld(cb)))

    # editorial policy
    cb = [("홈", "/"), ("편집 정책", None)]
    notes = [
        ("콘텐츠 작성 주체", ["모든 콘텐츠는 마사지고 운영팀이 작성하고, 안전 관련 내용은 자문 트레이너가 감수합니다.",
                          "작성·감수자의 실명과 직책을 저자 페이지에 공개합니다."]),
        ("데이터 출처", ["운영 수치는 본사 배차 시스템의 1차 로그를 집계한 값입니다.",
                     "외부 자료를 인용할 때는 출처를 함께 표기합니다."]),
        ("후기 검증", ["후기는 실제 이용 고객의 작성분만 게시합니다.",
                    "운영 로그와 대조해 허위·중복 후기를 배제합니다."]),
        ("AI 활용 원칙", ["문장 다듬기 등에 AI를 보조적으로 활용할 수 있으나, 사실 확인과 최종 책임은 사람(운영팀)이 집니다.",
                      "원본 데이터·직접 경험·전문가 감수를 거친 결과물만 게시합니다."]),
        ("수정·정정", ["오류가 확인되면 신속히 정정하고, 중요한 변경은 갱신일을 표기합니다."]),
    ]
    nh = "".join(note(i, t, p) for i, (t, p) in enumerate(notes, 1))
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">EDITORIAL POLICY</span>
<h1>편집 정책</h1><p class="lead">구글 'Who/How/Why' 원칙에 따라 콘텐츠 작성·검증 기준을 공개합니다.</p>
<div class="notes" style="margin-top:30px">{nh}</div></section>{cta_band()}"""
    write("/editorial-policy/", page(f"편집 정책 | {SITE['brand']}",
        "마사지고 콘텐츠 작성 주체·데이터 출처·후기 검증·AI 활용·정정 원칙을 공개합니다.",
        "/editorial-policy/", body, breadcrumb_jsonld(cb)))


POLICIES = {
    "privacy": ("개인정보처리방침", [
        ("수집 항목", ["예약에 필요한 최소한의 정보(연락처, 방문 지역, 예약 코스·시간)만 수집합니다."]),
        ("이용 목적", ["수집한 정보는 예약 접수·매니저 배정·연락·고객 응대 목적에만 사용합니다."]),
        ("보유 기간", ["관련 법령이 정한 기간 동안 보관 후 파기합니다."]),
        ("제3자 제공", ["법령에 따른 경우를 제외하고 동의 없이 제3자에게 제공하지 않습니다."]),
        ("책임자", [f"개인정보보호책임자: {SITE['privacy_officer']} · 문의 {SITE['phone']}"]),
    ]),
    "terms": ("이용약관", [
        ("목적", ["본 약관은 마사지고 출장마사지 서비스 이용에 관한 조건을 정합니다."]),
        ("서비스 내용", ["본 서비스는 건강관리를 위한 이완 서비스이며 의료 행위가 아닙니다."]),
        ("예약·결제", ["관리 시작 전 안내된 금액으로 결제하며 표시 금액 외 추가 비용은 없습니다."]),
        ("환불·분쟁", ["예약 취소·환불은 관련 법령과 본 약관에 따라 처리합니다.", f"분쟁이 있으면 고객센터 {SITE['phone']}로 연락 주세요."]),
        ("이용 제한", ["19세 미만은 이용할 수 없습니다."]),
    ]),
    "youth": ("청소년보호정책", [
        ("기본 방침", ["마사지고는 19세 미만 청소년의 이용을 제한합니다."]),
        ("연령 확인", ["예약·이용 과정에서 성인 여부를 확인할 수 있습니다."]),
        ("유해정보 차단", ["청소년에게 유해한 정보가 노출되지 않도록 관리합니다."]),
        ("책임자", [f"청소년보호 책임: {SITE['privacy_officer']} · 문의 {SITE['phone']}"]),
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
    body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">LOCATIONS</span>
<h1>지역별 출장마사지</h1>
<p class="lead">서울·경기·인천·부산 4개 광역권, 총 {sum(len(v['districts']) for v in REGIONS.values())}개 행정구에서 운영합니다.</p>
<div class="grid g2" style="margin-top:34px">{cards}</div></section>{cta_band()}"""
    write("/locations/", page(f"지역별 출장마사지 — 서울·경기·인천·부산 | {SITE['brand']}",
        f"마사지고 출장마사지 지역 안내. 서울·경기·인천·부산 총 {sum(len(v['districts']) for v in REGIONS.values())}개 행정구 전역 출장 가능.",
        "/locations/", body, breadcrumb_jsonld(cb)))
    # metro hubs
    for k, v in REGIONS.items():
        cb = [("홈", "/"), ("지역", "/locations/"), (v["ko"], None)]
        dist_cards = "".join(
            f'<a href="/locations/{k}/{d[1]}/">{esc(d[0])}</a>' for d in v["districts"])
        body = f"""<section class="wrap">{crumb(cb)}<span class="eyebrow">{esc(v["en"]).upper()}</span>
<h1>{esc(v['ko'])} 출장마사지</h1><p class="lead">{esc(v['intro'])}</p>
<div class="linklist" style="margin-top:30px">{dist_cards}</div></section>{cta_band()}"""
        write(f"/locations/{k}/", page(
            f"{v['ko']} 출장마사지 — {len(v['districts'])}개 지역 | {SITE['brand']}",
            f"{v['ko']} 전역 출장마사지. {v['intro']} {len(v['districts'])}개 행정구별 안내와 예약 {SITE['phone']}.",
            f"/locations/{k}/", body, breadcrumb_jsonld(cb)))
        # districts
        for (dko, dslug, character, dongs, landmark) in v["districts"]:
            build_district(k, v, dko, dslug, character, dongs, landmark)


def build_district(metro, v, dko, dslug, character, dongs, landmark):
    cb = [("홈", "/"), ("지역", "/locations/"), (v["ko"], f"/locations/{metro}/"), (dko, None)]
    rating = district_rating(metro, dslug)
    rc = district_review_count(metro, dslug)
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

<section class="wrap tight"><span class="eyebrow">DATA &amp; METHODOLOGY</span><h2>데이터 출처</h2>
<div class="databox reveal" style="margin-top:18px">
<p>· 위 수치는 마사지고 본사 배차 시스템의 1차 운영 로그를 {esc(dko)} 단위로 집계한 값입니다.</p>
<p>· {esc(v['ko'])} 권역 누적 배차 {OPS['by_region'].get(v['ko'], 0):,}건을 기반으로 산출했습니다.</p>
<p>· 평점 {rating}은 {esc(dko)} 이용 고객 {rc}건의 후기 평균입니다.</p></div></section>

<section class="wrap tight"><span class="eyebrow">PRICING</span><h2>{esc(dko)} 출장마사지 요금</h2>
<div class="grid g3" style="margin-top:24px">{pcards}</div></section>

<section class="wrap tight" id="reviews"><span class="eyebrow">REVIEWS</span><h2>{esc(dko)} 고객 후기</h2>
<div class="grid g3" style="margin-top:24px">{rev_html}</div></section>

<section class="wrap tight"><span class="eyebrow">FAQ</span><h2>{esc(dko)} 자주 묻는 질문</h2>
<div style="margin-top:20px">{faq_block(faqs)}</div></section>

<section class="wrap tight"><h2>{esc(v['ko'])} 다른 지역</h2><div class="linklist">{nearby}</div></section>
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
    write(path, page(
        f"{dko} 출장마사지 — 평균 {avg_d}분 도착 · 예약 {SITE['phone']} | {SITE['brand']}",
        f"{v['ko']} {dko} 출장마사지. {landmark} 인근 평균 약 {avg_d}분 도착, 동별 도착 시간·요금·{dko} 고객 후기 안내. {SITE['hours']}, 예약 {SITE['phone']}.",
        path, body, [local_ld, breadcrumb_jsonld(cb), faq_jsonld(faqs)]))


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
