"""Build the bilingual post "APIs no longer need to be sexy" from preserved text sources."""
from pathlib import Path
import html, re
from build_german import alternates, german_shell, switch, german_subscription

ROOT = Path(__file__).parent
OUT = ROOT / 'public'
EN = '/writing/apis-no-longer-need-to-be-sexy/'
DE = '/de/artikel/apis-muessen-nicht-mehr-sexy-sein/'
IMAGE = 'api-museum.jpg'
PUBLISHED = '2026-11-20'

COPY = {
    'en': dict(
        description='Why API design still matters when AI can talk to anything.',
        alt='AI-generated image: a small group of visitors in a vast, minimalist museum hall looks at a monumental black canvas that shows only the word API in large white letters.',
        caption='AI-generated concept image',
        eyebrow='POST',
        back='All posts &amp; articles',
        date=f'Published on this site: <time datetime="{PUBLISHED}">20 November 2026</time>',
        meta='Post',
        read='Read the post →',
    ),
    'de': dict(
        description='Warum API-Design wichtig bleibt, auch wenn AI mit allem sprechen kann.',
        alt='KI-generiertes Bild: Eine kleine Gruppe von Besuchern steht in einer grossen, minimalistischen Museumshalle vor einem monumentalen schwarzen Bild, auf dem nur das Wort API in grossen weissen Buchstaben steht.',
        caption='KI-generiertes Konzeptbild',
        eyebrow='POST',
        back='Alle Posts &amp; Artikel',
        date=f'Auf dieser Website seit: <time datetime="{PUBLISHED}">20. November 2026</time>',
        meta='Post',
        read='Auf Deutsch lesen →',
    ),
}


def body(text):
    return ''.join('<p>' + html.escape(block).replace('\n', '<br>') + '</p>' for block in text.split('\n\n'))


def build():
    build_post(EN, DE, IMAGE, 'apis-sexy', COPY)
    print('Generated APIs no longer need to be sexy EN/DE.')


def build_post(EN, DE, IMAGE, slug, COPY, width=1536, height=1024, deck=False, signed=False):
    """Bilingual post page plus homepage card. With deck, the second block is the subtitle;
    with signed, /hugs/kay goes before a final P.S. block."""
    template = (OUT / 'writing/who-needs-a-meeting/index.html').read_text()
    template = re.sub(r'<link rel="alternate"[^>]*>', '', template)
    template = re.sub(r'<div class="language-switch".*?</div>', '', template)
    esc = lambda s: html.escape(s, quote=True)
    for lang, route in [('en', EN), ('de', DE)]:
        c = COPY[lang]
        title, text = (ROOT / f'content/{slug}-{lang}.txt').read_text().strip().split('\n\n', 1)
        subtitle = ''
        if deck:
            subtitle, text = text.split('\n\n', 1)
        ps = ''
        if signed:
            text, ps = text.rsplit('\n\n', 1)
            assert ps.startswith('P.S.')
        source = template
        source = re.sub(r'<title>.*?</title>', '<title>' + esc(title) + ' | Kay Lummitsch</title>', source, count=1)
        source = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://kaylummitsch.com' + route + '">', source)
        for key, value in [('name="description"', c['description']), ('property="og:title"', title), ('name="twitter:title"', title),
                           ('property="og:description"', c['description']), ('name="twitter:description"', c['description']),
                           ('property="og:url"', 'https://kaylummitsch.com' + route),
                           ('property="og:image"', 'https://kaylummitsch.com/assets/' + IMAGE), ('name="twitter:image"', 'https://kaylummitsch.com/assets/' + IMAGE),
                           ('property="og:image:alt"', c['alt']), ('name="twitter:image:alt"', c['alt']),
                           ('property="article:published_time"', PUBLISHED)]:
            source = re.sub(r'<meta ' + key + r' content="[^"]*">', lambda m: '<meta ' + key + ' content="' + esc(value) + '">', source)
        home = '/de/' if lang == 'de' else '/'
        sub = german_subscription() if lang == 'de' else re.search(r'<section class="subscription".*?</section>', template, re.S)[0]
        main = (f'<main id="main" class="reading"><a class="back" href="{home}#writing">← {c["back"]}</a>'
                f'<p class="eyebrow">{c["eyebrow"]} / KAY LUMMITSCH</p><h1>{esc(title)}</h1>'
                + (f'<p class="deck">{esc(subtitle)}</p>' if subtitle else '') +
                f'<p class="published-date">{c["date"]}</p>'
                f'<figure style="margin:0 0 2rem"><img class="reading-cover" src="/assets/{IMAGE}" alt="{esc(c["alt"])}" width="{width}" height="{height}"><figcaption>{c["caption"]}</figcaption></figure>'
                f'<div class="article-text">{body(text)}</div>'
                + ('<div class="article-end"><span>/hugs/kay</span></div>' if signed else '')
                + (f'<div class="article-text">{body(ps)}</div>' if ps else '') +
                f'<a class="back" href="{home}#writing">← {c["back"]}</a>{sub}</main>')
        source = re.sub(r'<main\b.*?</main>', lambda m: main, source, count=1, flags=re.S)
        if lang == 'de':
            source = german_shell(source, title, c['description'], EN, DE)
        else:
            source = source.replace('</nav></header>', '</nav>' + switch(EN, DE, 'en') + '</header>', 1)
            source = source.replace('</head>', alternates(EN, DE) + '</head>', 1)
        folder = OUT / route.strip('/')
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(source)
        homefile = OUT / home.strip('/') / 'index.html'
        homepage = homefile.read_text()
        card = (f'<a class="story" href="{route}"><div class="story-image"><img src="/assets/{IMAGE}" alt="{esc(c["alt"])}" loading="lazy" width="{width}" height="{height}"></div>'
                f'<div class="story-meta">{c["meta"]} <span>↗</span></div><h3>{esc(title)}</h3><p class="published-date">{c["date"]}</p>'
                f'<p>{esc(c["description"])}</p><span class="read">{c["read"]}</span></a>')
        if f'href="{route}"' not in homepage:
            homepage = homepage.replace('<div class="stories">', '<div class="stories">' + card, 1)
        homefile.write_text(homepage)


if __name__ == '__main__':
    build()
