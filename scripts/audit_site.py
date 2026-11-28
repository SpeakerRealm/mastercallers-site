"""Check local navigation targets and interactive controls in the static site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'training').glob('*.html'))

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.buttons = []
        self.menus = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.add(data['id'])
        if tag in ('a', 'img', 'link', 'script'):
            key = 'href' if tag in ('a', 'link') else 'src'
            if key in data:
                self.links.append((tag, data[key], data))
        if tag == 'button':
            self.buttons.append(data)
        if tag == 'details' and 'mobile-menu' in data.get('class', '').split():
            self.menus += 1

pages = {}
for path in PAGES:
    parser = Page()
    parser.feed(path.read_text(encoding='utf-8'))
    pages[path] = parser

errors = []
for path, page in pages.items():
    if page.menus != 1:
        errors.append(f'{path.relative_to(ROOT)}: expected one mobile menu')
    for tag, raw, attrs in page.links:
        link = urlsplit(raw)
        if tag == 'a' and raw == '#':
            errors.append(f'{path.relative_to(ROOT)}: empty link')
        if tag == 'a' and attrs.get('target') == '_blank' and 'noopener' not in attrs.get('rel', '').split():
            errors.append(f'{path.relative_to(ROOT)}: new-tab link missing noopener: {raw}')
        if link.scheme or link.netloc or raw.startswith('mailto:'):
            continue
        target = (path.parent / unquote(link.path)).resolve() if link.path else path
        if not target.is_file():
            errors.append(f'{path.relative_to(ROOT)}: missing {raw}')
        elif link.fragment and target.suffix == '.html':
            target_page = pages.get(target)
            if target_page and unquote(link.fragment) not in target_page.ids:
                errors.append(f'{path.relative_to(ROOT)}: missing anchor {raw}')
    for button in page.buttons:
        if button.get('type') not in ('button', 'submit'):
            errors.append(f'{path.relative_to(ROOT)}: button without explicit type')

print(f'Checked {len(pages)} pages, {sum(len(p.links) for p in pages.values())} resource and navigation links, and {sum(len(p.buttons) for p in pages.values())} buttons.')
for error in errors:
    print('ERROR:', error)
raise SystemExit(bool(errors))
