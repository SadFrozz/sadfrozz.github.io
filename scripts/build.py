"""Build the bilingual static portal using only Python's standard library."""
import html,json
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
PROJECTS=json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8'))
SNAPSHOT=json.loads((ROOT/'content/snapshot.json').read_text(encoding='utf-8'))
E=html.escape
BASE='https://sadfrozz.github.io'
T={
'ru':dict(home='Проекты',docs='Документация',all='Все проекты',reaper='Инструменты REAPER',audio='Обработка звука',network='Сетевые драйверы',code='Исходники',release='Релиз',norelease='Без релиза',pre='Предварительный релиз',read='Открыть руководство',requirements='Требования',contents='На этой странице',verified='Сверено 24.11.2026',foot='Открытые проекты SadFrozz. Документация, загрузки и исходники.',foot2='Без аналитики и внешних шрифтов.',search='Найти проект',empty='Подходящих проектов нет. Измените запрос или категорию.',downloads='Загрузки',other='Другие проекты',next='Продолжить',issues='Сообщить об ошибке',main='Исходники main',download='Скачать',support='Вопросы по проекту',skip='К содержимому'),
'en':dict(home='Projects',docs='Documentation',all='All projects',reaper='REAPER tools',audio='Audio processing',network='Network drivers',code='Source code',release='Release',norelease='No release',pre='Pre-release',read='Read the guide',requirements='Requirements',contents='On this page',verified='Reviewed 24 Nov 2026',foot='Open projects by SadFrozz. Guides, downloads and source code.',foot2='No analytics or external fonts.',search='Find a project',empty='No matching projects. Try another search or category.',downloads='Downloads',other='More projects',next='Explore',issues='Report an issue',main='Main source',download='Download',support='Project support',skip='Skip to content')}

def home(lang): return '/' if lang=='ru' else '/en/'
def name(p,lang): return p.get('title_en',p['title']) if lang=='en' else p['title']
def guide(p,lang): return f'/{lang}/projects/{p["slug"]}/'
def repo(p): return 'https://github.com/SadFrozz/'+p['repo']
def meta(p): return next(s for s in SNAPSHOT['projects'] if s['repo']==p['repo'])
def label(p,lang):
    r=meta(p)['release']; t=T[lang]
    return t['norelease'] if not r else r['tag']+(' · '+t['pre'] if r['prerelease'] else '')
def a(url,text,cls=''):return f'<a href="{E(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+f'>{E(text)}</a>'
def write(path,content):
    p=OUT/path.lstrip('/')
    if path.endswith('/'):p=p/'index.html'
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8',newline='\n')

def shell(lang,title,description,path,alternate,body,kind=''):
    t=T[lang]; altlang='en' if lang=='ru' else 'ru'
    logo='<span>SadFrozz</span>'
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · SadFrozz</title><meta name="description" content="{E(description,quote=True)}">
<meta name="color-scheme" content="light dark">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; object-src 'none'; form-action 'none'">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css">
<link rel="canonical" href="{BASE}{path}"><link rel="alternate" hreflang="{lang}" href="{BASE}{path}"><link rel="alternate" hreflang="{altlang}" href="{BASE}{alternate}">
<meta property="og:title" content="{E(title,quote=True)} · SadFrozz"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{path}">
<script src="/assets/theme.js"></script><script src="/assets/site.js" defer></script></head>
<body class="{kind}"><a class="skip" href="#main">{t['skip']}</a>
<header class="site-header"><div class="header-inner"><a href="{home(lang)}" class="brand" aria-label="SadFrozz">{logo}</a>
<nav aria-label="{'Навигация' if lang=='ru' else 'Navigation'}">{a(home(lang)+'#projects',t['home'])}{a('https://github.com/SadFrozz','GitHub ↗')}</nav>
<div class="header-options"><div class="language" aria-label="Language / Язык">{a(path if lang=='ru' else alternate,'RU','active' if lang=='ru' else '')}{a(path if lang=='en' else alternate,'EN','active' if lang=='en' else '')}</div>
<button class="theme-toggle" type="button" aria-label="{'Тёмная тема' if lang=='ru' else 'Dark theme'}" aria-pressed="false" hidden><span aria-hidden="true">◐</span></button></div></div></header>
{body}
<footer class="site-footer"><div><a href="{home(lang)}" class="footer-name">SadFrozz</a><p>{t['foot']}</p></div><div class="footer-meta"><span>{t['foot2']}</span>{a('https://github.com/SadFrozz/sadfrozz.github.io','GitHub Pages ↗')}</div></footer></body></html>'''

def project_screenshot(p, lang, thumbnail=False):
    russian = lang == 'ru'
    if p['slug'] == 'web-prompter':
        asset, width, height = 'text-monitor.png', 1903, 1130
        alt = 'Текстовый монитор с таймкодом, ролями и подсветкой текущей реплики' if russian else 'Text monitor with timecodes, speaker roles and a highlighted cue'
        caption = 'Текстовый монитор на примере проекта озвучки.' if russian else 'The text monitor showing a sample voice-over session.'
    else:
        asset, width, height = 'mcu-display.png', 1702, 427
        alt = 'MCU Display Web с названиями каналов, уровнями и таймкодом' if russian else 'MCU Display Web with channel names, levels and timecode'
        caption = 'MCU Display Web: названия каналов, уровни и таймкод.' if russian else 'MCU Display Web showing channel names, levels and timecode.'
    url = '/assets/' + asset
    img = f'<img src="{url}" width="{width}" height="{height}" alt="{alt}" loading="lazy">'
    if thumbnail:
        return f'<div class="visual screenshot-thumb {p["slug"]}">{img}</div>'
    return f'<figure class="project-screenshot"><a href="{url}">{img}</a><figcaption>{caption}</figcaption></figure>'

ILLUSTRATIONS = {
    'dlab-series': ('dlab-series-cover.jpg', 800, {
        'ru': ('Обложка на основе интерфейсов dLab 286, 376 и 676', 'Иллюстрация по мотивам интерфейсов 286, 376 и 676. В релиз v1.0 входят 286 и 376.'),
        'en': ('Cover artwork based on dLab 286, 376 and 676', 'Artwork inspired by the 286, 376 and 676 interfaces. Release v1.0 includes 286 and 376.'),
    }),
    'webview': ('reaper-webview-cover.jpg', 444, {
        'ru': ('Браузер внутри рабочей станции с аудиодорожками', 'Иллюстрация REAPER WebView.'),
        'en': ('A browser embedded in a workstation with audio tracks', 'REAPER WebView illustration.'),
    }),
    'ath10k-airport': ('ath10k-wifi-cover.jpg', 800, {
        'ru': ('Ноутбук с открытым меню Wi-Fi', 'Иллюстрация подключения к Wi-Fi на ноутбуке.'),
        'en': ('Laptop with the Wi-Fi menu open', 'Illustration of a laptop connecting to Wi-Fi.'),
    }),
}


def project_illustration(project, lang, thumbnail=False):
    filename, height, copy = ILLUSTRATIONS[project['slug']]
    alt, caption = copy[lang]
    url = '/assets/' + filename
    img = f'<img src="{url}" alt="{E(alt, quote=True)}" width="1200" height="{height}" loading="lazy">'
    if thumbnail:
        return f'<div class="visual illustration-thumb">{img}</div>'
    return f'<figure class="project-screenshot"><a href="{url}">{img}</a><figcaption>{E(caption)}</figcaption></figure>'

def visual(p, lang):
    if p['slug']=='media-import':
        bars=''.join(f'<i class="h{v}"></i>' for v in [16,30,56,38,78,95,65,48,85,60,40,70,100,80,45,24,50,70,56,90,65,30,50,80,95,40,65,32,55,75,35,22,45,60,80,90,55,70,45,25])
        return f'<div class="visual media-visual" aria-hidden="true"><div class="visual-label">MEDIA / SIGNAL IN</div><div class="wave">{bars}</div><div class="codec-row"><span>DOLBY</span><span>DTS</span><span>MKV / MP4</span><span>SUBTITLES</span></div></div>'
    if p['slug'] in ILLUSTRATIONS:
        return project_illustration(p, lang, thumbnail=True)
    return project_screenshot(p, lang, thumbnail=True)

def card(p,lang):
    t=T[lang]; m=meta(p); status='experimental' if not m['release'] or m['release']['prerelease'] else ''
    return f'''<article class="project-card" data-category="{p['category']}" data-search="{E(name(p,lang)+' '+p['repo']+' '+p['summary'][lang]+' '+' '.join(p['platforms']),quote=True)}">
<div class="card-top"><span class="eyebrow">{t[p['category']]}</span><span class="status {status}">{E(label(p,lang))}</span></div>
{visual(p,lang)}<div class="card-copy"><h3>{a(guide(p,lang),name(p,lang))}</h3><p>{E(p['summary'][lang])}</p><div class="tags">{''.join(f'<span>{E(s)}</span>' for s in p['platforms'])}</div></div>
<div class="card-links">{a(guide(p,lang),t['read']+' ↗')}{a(repo(p),'GitHub','quiet')}</div></article>'''

def portal(lang):
    t=T[lang]
    if lang == 'ru':
        title = 'Проекты и документация'
        intro = 'Мои проекты для REAPER, плагины обработки звука и Wi-Fi-драйвер для macOS. Здесь собраны инструкции по установке, ссылки на релизы и исходный код.'
        quick_title = 'Документация'
        catalogue = 'Проекты'
    else:
        title = 'Projects and documentation'
        intro = 'My REAPER tools, audio plugins and a Wi-Fi driver for macOS. Find setup guides, releases and source code here.'
        quick_title = 'Documentation'
        catalogue = 'Projects'
    quick_links = ''.join(f'<li>{a(guide(p, lang), name(p, lang))}</li>' for p in PROJECTS)
    filterbuttons=''.join(f'<button type="button" data-filter="{cat}" aria-pressed="{str(cat=="all").lower()}">{t[cat]}</button>' for cat in ['all','reaper','audio','network'])
    body=f'''<main id="main">
<section class="project-intro wrap" aria-labelledby="portal-title">
  <div class="intro-copy"><h1 id="portal-title">SadFrozz</h1><p>{E(intro)}</p></div>
  <nav class="quick-docs" aria-labelledby="quick-docs-title"><h2 id="quick-docs-title">{quick_title}</h2><ul>{quick_links}</ul></nav>
</section>
<section id="projects" class="catalogue wrap"><div class="section-heading"><h2>{catalogue}</h2></div>
<div class="catalogue-controls" hidden><div class="filters" aria-label="{'Категории' if lang=='ru' else 'Categories'}">{filterbuttons}</div><label class="search"><span aria-hidden="true">⌕</span><span class="sr-only">{t['search']}</span><input type="search" placeholder="{t['search']}" aria-label="{t['search']}" maxlength="150"></label></div>
<p class="filter-result sr-only" role="status" aria-live="polite"></p><div class="projects-grid">{''.join(card(p,lang) for p in PROJECTS)}</div><p class="no-results" hidden>{t['empty']}</p></section>
</main>'''
    path=home(lang);alternate=home('en' if lang=='ru' else 'ru')
    write(path,shell(lang,title,intro,path,alternate,body,'portal'))

def documentation(p,lang):
    t=T[lang];m=meta(p);r=m['release'];path=guide(p,lang);alt=guide(p,'en' if lang=='ru' else 'ru')
    preview = ''
    if p['slug'] in ILLUSTRATIONS:
        preview = project_illustration(p, lang)
    elif p['slug'] in ('web-prompter', 'mcudisp-web'):
        preview = project_screenshot(p, lang)
    links=''.join(a('#'+s['id'],s['title']) for s in p['sections'][lang])+a('#downloads',t['downloads'])
    sections=''
    for s in p['sections'][lang]:
        tag='ol' if s['id']=='install' else 'ul'
        sections+=f'<section id="{s["id"]}" class="doc-section"><h2>{E(s["title"])}</h2><{tag}>'+''.join('<li>'+E(x)+'</li>' for x in s['items'])+f'</{tag}>'
        if s['code']:sections+='<div class="code-block"><pre><code>'+E(s['code'])+'</code></pre></div>'
        if s['id']=='usage' and p['slug']=='web-prompter':sections+='<p class="related">'+a(f'/{lang}/projects/media-import/','Media Import ↗')+' · '+a(f'/{lang}/projects/webview/','REAPER WebView ↗')+'</p>'
        sections+='</section>'
    assets=''
    if r:
        for asset in r['assets']:
            if asset['name'].lower().startswith('sha'):btn='SHA-256'
            elif 'win' in asset['name'].lower():btn='Windows'
            elif 'mac' in asset['name'].lower():btn='macOS'
            else:btn=asset['name']
            assets+=f'<li>{a(asset["url"],btn+" ↗","button download")}<span>{E(asset["name"])}</span></li>'
        release_link=a(repo(p)+'/releases/tag/'+quote(r['tag']),r['tag']+' · '+r['date'][:10]+' ↗')
        if not assets:assets='<li>'+a(repo(p)+'/tree/'+r['commit'],('Исходники '+r['tag'] if lang=='ru' else r['tag']+' source')+' ↗','button download')+'</li>'
    else:
        release_link=t['norelease'];assets='<li>'+a(repo(p)+'/tree/'+m['commit'],t['main']+' ↗','button download')+'</li>'
    sections+=f'<section id="downloads" class="doc-section"><h2>{t["downloads"]}</h2><p>{release_link}</p><ul class="download-list">{assets}</ul></section>'
    other=''.join(a(guide(q,lang),name(q,lang)+' ↗') for q in PROJECTS if q['slug']!=p['slug'])
    body=f'''<main id="main" class="wrap docs-wrap"><div class="breadcrumbs">{a(home(lang),t['home'])}<span>/</span><span>{E(name(p,lang))}</span></div>
<div class="docs-layout"><aside class="toc"><p class="eyebrow">{t['contents']}</p><nav aria-label="{t['contents']}">{links}</nav></aside>
<article class="doc-article"><div class="doc-header"><p class="eyebrow accent">{t[p['category']]} / {t['docs']}</p><h1>{E(name(p,lang))}</h1><p class="doc-lead">{E(p['summary'][lang])}</p><div class="tags">{''.join('<span>'+E(s)+'</span>' for s in p['platforms'])}</div>
<div class="doc-actions">{a('#downloads',t['downloads']+' ↓','button primary')}{a(repo(p),t['code']+' ↗','button outline')}</div><div class="release-note"><span class="status">{E(label(p,lang))}</span><span>{t['verified']}</span></div></div>
{preview}{sections}<div class="support-box"><h3>{t['support']}</h3><p>{'Ошибки и предложения обсуждаются в Issues исходного проекта.' if lang=='ru' else 'Discuss bugs and suggestions in the original project’s Issues.'}</p>{a(repo(p)+'/issues',t['issues']+' ↗','text-link')}</div></article></div>
<section class="more-projects"><h2>{t['other']}</h2><div>{other}</div></section></main>'''
    write(path,shell(lang,name(p,lang),p['summary'][lang],path,alt,body,'documentation'))

for lang in ['ru','en']:
    portal(lang)
    for p in PROJECTS:documentation(p,lang)
write('/404.html',shell('ru','Страница не найдена','Page not found','/404.html','/en/', '<main id="main" class="wrap not-found"><p class="eyebrow accent">404 / NO SIGNAL</p><h1>Страница не найдена.<br>Page not found.</h1><p>Выберите язык и вернитесь к проектам.</p><div class="hero-actions">'+a('/','Проекты / RU','button primary')+a('/en/','Projects / EN','button outline')+'</div></main>'))
write('/.nojekyll','')
paths=[('/' if x.relative_to(OUT).as_posix()=='index.html' else '/'+x.relative_to(OUT).as_posix().replace('index.html','')) for x in OUT.rglob('*.html') if x.name!='404.html']
write('/sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc><lastmod>2026-11-24</lastmod></url>' for p in sorted(paths))+'</urlset>\n')
write('/robots.txt','User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
print(f'Built {len(list(OUT.rglob("*.html")))} HTML pages')
