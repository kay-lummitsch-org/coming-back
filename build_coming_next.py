"""Coming next: the two-books announcement as a post, and one compact homepage block
instead of two separate book sections. Runs after build_books_update. Idempotent."""
import re
from pathlib import Path
from build_apis_sexy import build_post

ROOT = Path(__file__).parent
OUT = ROOT / 'public'
EN = '/writing/coming-next/'
DE = '/de/artikel/als-naechstes/'
IMAGE = 'coming-next-two-covers.jpg'
PUBLISHED = '2026-11-23'
BOOKLET = '/booklets/the-digital-journeymen/'

COPY = {
    'en': dict(
        description='Two books instead of one. PEOPLE FIRST — WTF! comes first. The Agents Edition follows.',
        alt='The two new covers side by side: PEOPLE FIRST — WTF! with five workers carrying an orange pyramid, and THE DIGITAL JOURNEYMEN – Agents Edition with a human hand passing a yellow baton to a wireframe robot hand.',
        caption='The two new covers',
        eyebrow='POST',
        back='All posts &amp; articles',
        date=f'Published on this site: <time datetime="{PUBLISHED}">23 November 2026</time>',
        meta='Post',
        read='Read the post →',
    ),
    'de': dict(
        description='Zwei Bücher statt einem. Zuerst erscheint PEOPLE FIRST — WTF! Danach folgt die Agents Edition.',
        alt='Die beiden neuen Cover nebeneinander: PEOPLE FIRST — WTF! mit fünf Arbeitenden, die eine orange Pyramide tragen, und THE DIGITAL JOURNEYMEN – Agents Edition mit einer Menschenhand, die einer Drahtgitter-Roboterhand einen gelben Staffelstab übergibt.',
        caption='Die beiden neuen Cover',
        eyebrow='POST',
        back='Alle Posts &amp; Artikel',
        date=f'Auf dieser Website seit: <time datetime="{PUBLISHED}">23. November 2026</time>',
        meta='Post',
        read='Auf Deutsch lesen →',
    ),
}

PF_IMG = '<img src="/assets/people-first-cover-portrait.webp" alt="{}" loading="lazy" width="800" height="1236">'
AE_IMG = '<img src="/assets/agents-edition-cover.webp" alt="{}" loading="lazy" width="800" height="1236">'

BLOCK = {
    'en': dict(
        file=OUT / 'index.html',
        link=('on this website.', f'on <a href="{BOOKLET}">this website</a>.'),
        html=('<section class="booklet-next home-next" id="booklet"><p class="eyebrow badge">COMING NEXT</p><div class="next-books">'
              '<article>' + PF_IMG.format('PEOPLE FIRST — WTF! cover: five workers carrying an orange pyramid with a relaxed boss on top') +
              '<div><p class="eyebrow">FIRST</p><h2>PEOPLE FIRST — WTF!</h2><p>Damn good organizational advice. For people who want their people to have a good Tuesday.</p>'
              '<a class="text-link" href="/assets/why-i-wrote.pdf">A first look: Why I wrote this book ↗</a></div></article>'
              '<article>' + AE_IMG.format('THE DIGITAL JOURNEYMEN – The Agents Edition cover: a human hand passing a yellow baton to a wireframe robot hand') +
              '<div><p class="eyebrow">THEN</p><h2>THE DIGITAL JOURNEYMEN – The Agents Edition</h2><p>Damn good digital advice for APIs in the age of AI. The agents will run into exactly the same walls.</p>'
              '<a class="text-link" href="/#agents">APIs in the age of AI →</a></div></article>'
              f'</div><p class="next-more"><a class="text-link" href="{EN}">Why it’s two books now →</a></p></section>'),
    ),
    'de': dict(
        file=OUT / 'de' / 'index.html',
        link=('auf dieser Website.', f'auf <a href="{BOOKLET}">dieser Website</a>.'),
        html=('<section class="booklet-next home-next" id="booklet"><p class="eyebrow badge">ALS NÄCHSTES</p><div class="next-books">'
              '<article>' + PF_IMG.format('PEOPLE FIRST — WTF! Cover: fünf Arbeitende tragen eine orange Pyramide, oben sitzt entspannt der Chef') +
              '<div><p class="eyebrow">ZUERST</p><h2>PEOPLE FIRST — WTF!</h2><p>Verdammt gute Gedanken zur Organisation. Für Menschen, die wollen, dass ihre Leute einen guten Dienstag haben.</p>'
              '<a class="text-link" href="/assets/why-i-wrote.pdf">Ein erster Blick: Warum ich dieses Buch schreibe · EN ↗</a></div></article>'
              '<article>' + AE_IMG.format('THE DIGITAL JOURNEYMEN – The Agents Edition Cover: eine Menschenhand übergibt einer Drahtgitter-Roboterhand einen gelben Staffelstab') +
              '<div><p class="eyebrow">DANACH</p><h2>THE DIGITAL JOURNEYMEN – The Agents Edition</h2><p>Verdammt gute digitale Gedanken für APIs im Zeitalter der AI. Die Agents werden an genau denselben Wänden stehen.</p>'
              '<a class="text-link" href="/de/#agents">APIs im Zeitalter der AI →</a></div></article>'
              f'</div><p class="next-more"><a class="text-link" href="{DE}">Warum es jetzt zwei Bücher werden →</a></p></section>'),
    ),
}

CSS = ('\n/* coming-next */.home-next{margin:0 auto;max-width:1200px;padding:70px 50px}'
       '.home-next>.eyebrow{margin-bottom:10px}.home-next .next-more{margin-top:36px}'
       '@media(max-width:620px){.home-next{padding:44px 24px}}\n')

SIGN = '<div class="article-end"><span>/hugs/kay</span></div>'


def build():
    build_post(EN, DE, IMAGE, 'coming-next', COPY, width=1600, height=1200)
    for lang, route in [('en', EN), ('de', DE)]:
        page = OUT / route.strip('/') / 'index.html'
        s = page.read_text()
        old, new = BLOCK[lang]['link']
        if new not in s:
            assert old in s, f'link sentence missing in {page}'
            s = s.replace(old, new, 1)
        if SIGN not in s:
            s = re.sub(r'(<div class="article-text">.*?</div>)', lambda m: m.group(1) + SIGN, s, count=1, flags=re.S)
        page.write_text(s)

    for lang, c in BLOCK.items():
        f = c['file']
        s = f.read_text()
        s = re.sub(r'<section class="booklet agents-edition" id="agents-edition">.*?</section>', '', s, flags=re.S)
        s, n = re.subn(r'<section class="booklet(?: home-next)?[^"]*" id="booklet">.*?</section>', lambda m: c['html'], s, count=1, flags=re.S)
        if n == 0:
            s, n = re.subn(r'<section class="booklet-next home-next" id="booklet">.*?</section>', lambda m: c['html'], s, count=1, flags=re.S)
        assert n == 1, f'booklet section missing in {f}'
        f.write_text(s)

    css = OUT / 'style.css'
    t = css.read_text()
    if '/* coming-next */' not in t:
        css.write_text(t + CSS)
    print('Generated Coming Next EN/DE; homepage books folded into one block.')


if __name__ == '__main__':
    build()
