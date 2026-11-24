"""Validate generated pages, local links, language pairs and sensitive patterns."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.lang=None;self.h1=0;self.alternates={};self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag in ('script','img') and a.get('src'):self.links.append(a['src'])
        if tag=='link' and a.get('href'):
            self.links.append(a['href'])
            if a.get('rel')=='alternate':self.alternates[a.get('hreflang')]=a['href']

pages={p:Page(p.read_text(encoding='utf-8')) for p in OUT.rglob('*.html')}
errors=[];external=set()
for p,page in pages.items():
    if page.lang not in ('ru','en'):errors.append(f'{p}: language')
    if page.h1!=1:errors.append(f'{p}: h1 count {page.h1}')
    if len(set(page.ids))!=len(page.ids):errors.append(f'{p}: duplicate IDs')
    for link in page.links:
        u=urlsplit(link)
        if u.netloc and u.netloc!='sadfrozz.github.io':
            if u.scheme!='https':errors.append(f'{p}: non-HTTPS external URL')
            external.add(link);continue
        if u.path.startswith('/'):target=OUT/unquote(u.path.lstrip('/'))
        else:target=p.parent/unquote(u.path)
        if not u.path:target=p
        elif u.path.endswith('/') or target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{p}: missing {link}')
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{p}: missing anchor {link}')
    if p.name!='404.html':
        if set(page.alternates)!={'ru','en'}:errors.append(f'{p}: missing language pairs')
        for lang,url in page.alternates.items():
            target=OUT/urlsplit(url).path.lstrip('/')/'index.html'
            if target not in pages or pages[target].lang!=lang:errors.append(f'{p}: wrong language target {url}')
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts:continue
    if p.suffix == '.png' and p.parent == OUT/'assets':continue
    text=p.read_text(encoding='utf-8')
    # Match concrete secrets/paths, not documentation discussing them.
    patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',r'[A-Za-z]:[\\/]Users[\\/]',r'(?i)(?:password|api_key)\s*[=:]\s*[\"\x27][^\"\x27]{5,}[\"\x27]']
    if p.name=='check.py':continue
    for pattern in patterns:
        if re.search(pattern,text):errors.append(f'{p}: sensitive-data pattern')
assert len(pages)==17, f'Expected 17 HTML pages, found {len(pages)}'
assert (OUT/'.nojekyll').is_file()
assert len(json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8')))==6
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages, local links/anchors, RU/EN targets, content scan; {len(external)} distinct external links')
