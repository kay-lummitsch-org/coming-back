"""Publish the approved Turning Sixty text and its German counterpart."""
from pathlib import Path
import html, json, re
from build_german import alternates, german_shell, switch, german_subscription

ROOT = Path(__file__).parent
OUT = ROOT / 'public'
EN = '/writing/turning-sixty/'
DE = '/de/artikel/sechzig-werden/'
IMAGE = 'turning-sixty-original.webp'

def inline(paragraph):
    result = ''
    for element in paragraph['paragraph']['elements']:
        run = element.get('textRun')
        if not run:
            continue
        value = html.escape(run['content'].rstrip('\n'))
        style = run.get('textStyle', {})
        if style.get('bold'): value = '<strong>'+value+'</strong>'
        if style.get('italic'): value = '<em>'+value+'</em>'
        if style.get('link', {}).get('url'):
            value = '<a href="'+html.escape(style['link']['url'], quote=True)+'">'+value+'</a>'
        result += value
    return result

def build():
    data = json.loads((ROOT/'content/turning-sixty.json').read_text())
    template = (OUT/'writing/who-needs-a-meeting/index.html').read_text()
    template = re.sub(r'<link rel="alternate"[^>]*>', '', template)
    template = re.sub(r'<div class="language-switch".*?</div>', '', template)
    for lang, route in [('en', EN), ('de', DE)]:
        title = 'TURNING SIXTY' if lang == 'en' else 'SECHZIG WERDEN'
        subtitle = 'Grief, humility, and many unanswered questions.' if lang == 'en' else 'Trauer, Demut und viele unbeantwortete Fragen.'
        paras = [inline(p) for p in data[lang] if inline(p).strip()]
        assert html.unescape(paras.pop(0)) == subtitle
        assert paras.pop() == '/hugs/kay'
        esc = lambda s: html.escape(s, quote=True)
        source = template
        source = re.sub(r'<title>.*?</title>', '<title>'+title+' | Kay Lummitsch</title>', source, count=1)
        source = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://kaylummitsch.com'+route+'">', source)
        for key, value in [('name="description"',subtitle),('property="og:title"',title),('name="twitter:title"',title),('property="og:description"',subtitle),('name="twitter:description"',subtitle),('property="og:url"','https://kaylummitsch.com'+route),('property="og:image"','https://kaylummitsch.com/assets/'+IMAGE),('name="twitter:image"','https://kaylummitsch.com/assets/'+IMAGE),('property="og:image:alt"','Photo by Sven Loof'),('name="twitter:image:alt"','Photo by Sven Loof'),('property="article:published_time"','2026-11-01')]:
            source = re.sub(r'<meta '+key+r' content="[^"]*">', lambda m: '<meta '+key+' content="'+esc(value)+'">', source)
        home = '/de/' if lang == 'de' else '/'
        back = 'Alle Posts &amp; Artikel' if lang == 'de' else 'All posts &amp; articles'
        date = 'Auf dieser Website seit: <time datetime="2026-11-01">1. November 2026</time>' if lang == 'de' else 'Published on this site: <time datetime="2026-11-01">1 November 2026</time>'
        alt = 'Kay blickt auf einem herbstlichen Balkon durch ein Fernglas. Foto von Sven Loof.' if lang == 'de' else 'Kay looking through binoculars on an autumn balcony. Photo by Sven Loof.'
        caption = ('Nein, ich habe es nicht auf das Titelblatt von Reader’s Digest geschafft. Aber offenbar darf man sich mit sechzig ein wenig künstlerische Freiheit erlauben. KI-generiertes fiktives Cover auf Grundlage eines Fotos von Sven Loof.' if lang == 'de' else 'No, I didn’t make the cover of Reader’s Digest. But apparently, turning sixty comes with a little artistic licence. AI-generated mock cover, based on a photograph by Sven Loof.')
        subscription = german_subscription() if lang == 'de' else re.search(r'<section class="subscription".*?</section>', template, re.S)[0]
        main = (f'<main id="main" class="reading"><a class="back" href="{home}#writing">← {back}</a><p class="eyebrow">'+('ARTIKEL' if lang == 'de' else 'ARTICLE')+f' / KAY LUMMITSCH</p><h1>{title}</h1><p class="deck">{esc(subtitle)}</p><p class="published-date">{date}</p>'
                f'<figure style="margin:0 0 2rem"><img class="reading-cover" src="/assets/{IMAGE}" alt="{esc(alt)}" width="1600" height="1200"><figcaption>Photo by Sven Loof</figcaption></figure>'
                '<div class="article-text">'+''.join('<p>'+p+'</p>' for p in paras)+'</div>'
                f'<figure style="margin:2rem 0"><img src="/assets/turning-sixty-rd-cover.webp" alt="'+('Fiktives KI-Cover von Reader’s Digest mit Kay.' if lang == 'de' else 'Fictional AI-generated Reader’s Digest cover featuring Kay.')+f'" width="1086" height="1448" loading="lazy" style="display:block;width:100%;height:auto"><figcaption>{esc(caption)}</figcaption></figure>'
                '<div class="article-end"><span>/hugs/kay</span></div>'+f'<a class="back" href="{home}#writing">← {back}</a>'+subscription+'</main>')
        source = re.sub(r'<main\b.*?</main>', lambda m: main, source, count=1, flags=re.S)
        if lang == 'de': source = german_shell(source, title, subtitle, EN, DE)
        else:
            source = source.replace('</nav></header>', '</nav>'+switch(EN, DE, 'en')+'</header>', 1)
            source = source.replace('</head>', alternates(EN, DE)+'</head>', 1)
        folder = OUT/route.strip('/'); folder.mkdir(parents=True, exist_ok=True)
        (folder/'index.html').write_text(source)
        homefile = OUT/home.strip('/')/'index.html'
        homepage = homefile.read_text()
        card = (f'<a class="story" href="{route}"><div class="story-image"><img src="/assets/{IMAGE}" alt="{esc(alt)}" loading="lazy" width="1600" height="1200"></div><div class="story-meta">'+('Artikel' if lang == 'de' else 'Article')+f' <span>↗</span></div><h3>{title}</h3><p class="published-date">{date}</p><p>{esc(subtitle)}</p><span class="read">'+('Auf Deutsch lesen →' if lang == 'de' else 'Read the article →')+'</span></a>')
        if f'href="{route}"' not in homepage: homepage = homepage.replace('<div class="stories">', '<div class="stories">'+card, 1)
        homefile.write_text(homepage)
    print('Generated Turning Sixty in English and German.')
