"""Copy src/Interactive Resume.dc.html into the page template embedded in index.html.

Edit the source file, then run from the repo root:

    python tools/sync.py            # rebuild index.html
    python tools/sync.py --check    # only report whether index.html is up to date

index.html keeps its own <head> part of the template (fonts and the runtime are
inlined there); everything from the <helmet> style block onward comes from src.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / 'index.html'
SRC = ROOT / 'src' / 'Interactive Resume.dc.html'
ANCHOR = '  <style>\n    html, body {'


def enc(s):
    return json.dumps(s, ensure_ascii=False).replace('</', '<\\u002F')


def bundle_tail(src):
    tail = src[src.index(ANCHOR):]
    # the bundler stores camelCase attributes (onClick) as sc-camel-on-click, since HTML lowercases names
    cut = tail.index('<script type="text/x-dc"')
    markup, script = tail[:cut], tail[cut:]
    markup = re.sub(
        r'(\s)([a-z]+(?:[A-Z][a-z]*)+)(="\{\{)',
        lambda m: m.group(1) + 'sc-camel-' + re.sub(r'([A-Z])', lambda c: '-' + c.group(1).lower(), m.group(2)) + m.group(3),
        markup,
    )
    script = script.replace('data-dc-script data-props', 'data-dc-script="" data-props', 1)
    return markup + script


def main():
    html = HTML.read_text(encoding='utf-8')
    src = SRC.read_text(encoding='utf-8')
    m = re.search(r'(<script type="__bundler/template">\s*)(.*?)(\s*</script>)', html, re.S)
    raw = m.group(2)
    template = json.loads(raw)
    assert enc(template) == raw, 'template encoding does not round-trip; refusing to rewrite index.html'
    assert template.count(ANCHOR) == 1 and src.count(ANCHOR) == 1, 'helmet <style> anchor not found exactly once'

    new_template = template[:template.index(ANCHOR)] + bundle_tail(src)
    if '--check' in sys.argv:
        print('index.html is up to date' if new_template == template else 'index.html is out of date')
        sys.exit(0 if new_template == template else 1)

    HTML.write_text(html[:m.start(2)] + enc(new_template) + html[m.end(2):], encoding='utf-8', newline='')
    print('index.html updated')


if __name__ == '__main__':
    main()
