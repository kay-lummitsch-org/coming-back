"""Publish the approved bilingual Sven post without rewriting its paragraphs."""
from pathlib import Path
import html
import re
from build_german import alternates, german_shell, switch, german_subscription

ROOT = Path(__file__).parent
OUT = ROOT / 'public'
EN = '/writing/who-needs-a-meeting/'
DE = '/de/artikel/wer-braucht-ein-meeting/'
IMAGE = 'sven-whisk-clean.png'

def build():
    template = (OUT/'writing/until-the-cat-jumps/index.html').read_text()
    template = re.sub(r'<link rel="alternate"[^>]*>', '', template)
    template = re.sub(r'<div class="language-switch".*?</div>', '', template)
    for language, route in [('en', EN), ('de', DE)]:
        text = (ROOT/f'content/sven-whisk-{language}.txt').read_text().strip()
        title, body = text.split('\n\n', 1)
        paragraphs = body.split('\n\n')
        assert paragraphs.pop() == '/hugs/kay'
        desc = ('What happens between people when they really work together.' if language == 'en'
                else 'Was zwischen Menschen entsteht, wenn sie wirklich zusammenarbeiten.')
        esc = lambda s: html.escape(s, quote=True)
        source = template
        for pattern, replacement in [
            (r'<title>.*?</title>', '<title>'+esc(title)+' | Kay Lummitsch</title>'),
            (r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="https://kaylummitsch.com{route}">'),
        ]:
            source = re.sub(pattern, lambda m: replacement, source, count=1)
        for key, value in [('name="description"',desc),('property="og:title"',title),
                           ('name="twitter:title"',title),('property="og:description"',desc),
                           ('name="twitter:description"',desc),('property="og:url"','https://kaylummitsch.com'+route),
                           ('property="og:image"','https://kaylummitsch.com/assets/'+IMAGE),
                           ('name="twitter:image"','https://kaylummitsch.com/assets/'+IMAGE),
                           ('property="og:image:alt"',title),('name="twitter:image:alt"',title),
                           ('property="article:published_time"','2026-10-20')]:
            source = re.sub(r'<meta '+key+r' content="[^"]*">', lambda m: '<meta '+key+' content="'+esc(value)+'">', source)
        home = '/de/' if language == 'de' else '/'
        back = 'Alle Posts &amp; Artikel' if language == 'de' else 'All posts &amp; articles'
        date = 'Auf dieser Website seit: <time datetime="2026-10-20">20. Oktober 2026</time>' if language == 'de' else 'Published on this site: <time datetime="2026-10-20">20 October 2026</time>'
        alt = 'Sven in der Küche mit Pfanne und grossem Schneebesen.' if language == 'de' else 'Sven in the kitchen with a frying pan and a large whisk.'
        subscription = re.search(r'<section class="subscription".*?</section>', template, re.S)[0]
        if language == 'de': subscription = german_subscription()
        main = (f'<main id="main" class="reading"><a class="back" href="{home}#writing">← {back}</a>'
                f'<p class="eyebrow">POST / KAY LUMMITSCH</p><h1>{esc(title)}</h1><p class="published-date">{date}</p>'
                f'<img class="reading-cover" src="/assets/{IMAGE}" alt="{esc(alt)}" width="1445" height="1088">'
                '<div class="article-text">'+''.join('<p>'+esc(p)+'</p>' for p in paragraphs)+'</div>'
                '<div class="article-end"><span>/hugs/kay</span></div>'
                f'<a class="back" href="{home}#writing">← {back}</a>'+subscription+'</main>')
        source = re.sub(r'<main\b.*?</main>', lambda m: main, source, count=1, flags=re.S)
        if language == 'de':
            source = german_shell(source, title, desc, EN, DE)
        else:
            source = source.replace('</nav></header>', '</nav>'+switch(EN, DE, 'en')+'</header>', 1)
            source = source.replace('</head>', alternates(EN, DE)+'</head>', 1)
        folder = OUT/route.strip('/')
        folder.mkdir(parents=True, exist_ok=True)
        (folder/'index.html').write_text(source)
        homefile = OUT/home.strip('/')/'index.html'
        homepage = homefile.read_text()
        card = (f'<a class="story" href="{route}"><div class="story-image"><img src="/assets/{IMAGE}" alt="{esc(alt)}" loading="lazy" width="1445" height="1088"></div>'
                f'<div class="story-meta">Post <span>↗</span></div><h3>{esc(title)}</h3><p class="published-date">{date}</p><p>{esc(desc)}</p>'
                '<span class="read">'+('Auf Deutsch lesen →' if language == 'de' else 'Read the post →')+'</span></a>')
        if f'href="{route}"' not in homepage:
            homepage = homepage.replace('<div class="stories">', '<div class="stories">'+card, 1)
        homefile.write_text(homepage)
    print('Generated CB24 in German and English.')
