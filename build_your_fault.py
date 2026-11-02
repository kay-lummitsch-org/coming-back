"""Build the approved bilingual Your Fault article from preserved text sources."""
from pathlib import Path
import html, re
from build_german import alternates, german_shell, switch, german_subscription
ROOT=Path(__file__).parent
OUT=ROOT/'public'
EN='/writing/congratulations-its-your-fault/'
DE='/de/artikel/herzlichen-glueckwunsch-deine-schuld/'
IMAGE='your-fault.jpg'

def body(text):
    blocks=[]
    for block in text.split('\n\n'):
        if block=='---': blocks.append('<hr>')
        elif block.startswith('- '): blocks.append('<ul>'+''.join('<li>'+html.escape(line[2:])+'</li>' for line in block.splitlines())+'</ul>')
        elif block.startswith('1. '): blocks.append('<ol>'+''.join('<li>'+html.escape(re.sub(r'^\d+\. ', '', line))+'</li>' for line in block.splitlines())+'</ol>')
        else: blocks.append('<p>'+html.escape(block).replace('\n','<br>')+'</p>')
    return ''.join(blocks)

def references(lang):
    if lang=='de':
        heading='Zum Weiterlesen'
        berne='Über wiederkehrende Beziehungsspiele – und den eigenen Anteil daran.'
        argyris='Über organisationale Abwehrroutinen, die vor Peinlichkeit schützen und Lernen verhindern.'
        friedman='Über Führung, emotionale Reaktivität und Selbstverantwortung innerhalb eines Systems.'
        note='Für die Bücher von Argyris und Friedman ist hier keine deutsche Ausgabe bestätigt; deshalb sind die Originaltitel angegeben.'
    else:
        heading='Further reading'
        berne='On the recurring games we play with one another — and the part we play ourselves.'
        argyris='On defensive routines that protect us from embarrassment while preventing us from learning.'
        friedman='On leadership, emotional reactivity and taking responsibility for ourselves within a system.'
        note='No German editions of the Argyris and Friedman titles have been confirmed here; their original titles are listed.'
    return f'''<section class="further-reading"><h2>{heading}</h2><p><strong>Eric Berne</strong><br>EN: <a href="https://ericberne.com/games-people-play/">Games People Play</a><br>DE: <a href="https://www.rowohlt.de/buch/dr-med-eric-berne-spiele-der-erwachsenen-9783644002432">Spiele der Erwachsenen – Psychologie der menschlichen Beziehungen</a><br>{berne}</p><p><strong>Chris Argyris</strong><br>EN: <a href="https://search.worldcat.org/title/Overcoming-organizational-defenses-%3A-facilitating-organizational-learning/oclc/442644367">Overcoming Organizational Defenses: Facilitating Organizational Learning</a><br>{argyris}</p><p><strong>Edwin H. Friedman</strong><br>EN: <a href="https://churchpublishing.org/products/9781596272804-a-failure-of-nerve">A Failure of Nerve: Leadership in the Age of the Quick Fix</a><br>{friedman}</p><p class="archive-note">{note}</p></section>'''

def build():
    template=(OUT/'writing/who-needs-a-meeting/index.html').read_text()
    template=re.sub(r'<link rel="alternate"[^>]*>','',template)
    template=re.sub(r'<div class="language-switch".*?</div>','',template)
    for lang,route in [('en',EN),('de',DE)]:
        text=(ROOT/f'content/your-fault-{lang}.txt').read_text().strip()
        title,text=text.split('\n\n',1)
        assert text.endswith('/hugs/kay')
        text=text[:-len('/hugs/kay')].rstrip()
        description=('Five uncomfortable questions about blame, leadership and our own part in the problem.' if lang=='en' else 'Fünf unbequeme Fragen über Schuld, Führung und den eigenen Anteil am Problem.')
        esc=lambda s:html.escape(s,quote=True)
        source=template
        source=re.sub(r'<title>.*?</title>','<title>'+esc(title)+' | Kay Lummitsch</title>',source,count=1)
        source=re.sub(r'<link rel="canonical"[^>]*>','<link rel="canonical" href="https://kaylummitsch.com'+route+'">',source)
        alt=('AI-generated image: a strong male hand files KAY alongside Board, Culture, Market and Employees in an orange cabinet labelled THOSE TO BLAME.' if lang=='en' else 'KI-generiertes Bild: Eine kräftige Männerhand ordnet KAY neben Board, Culture, Market und Employees in einen orangefarbenen Schrank mit der Aufschrift THOSE TO BLAME ein.')
        for key,value in [('name="description"',description),('property="og:title"',title),('name="twitter:title"',title),('property="og:description"',description),('name="twitter:description"',description),('property="og:url"','https://kaylummitsch.com'+route),('property="og:image"','https://kaylummitsch.com/assets/'+IMAGE),('name="twitter:image"','https://kaylummitsch.com/assets/'+IMAGE),('property="og:image:alt"',alt),('name="twitter:image:alt"',alt),('property="article:published_time"','2026-11-02')]:
            source=re.sub(r'<meta '+key+r' content="[^"]*">',lambda m:'<meta '+key+' content="'+esc(value)+'">',source)
        home='/de/' if lang=='de' else '/'
        back='Alle Posts &amp; Artikel' if lang=='de' else 'All posts &amp; articles'
        date=('Auf dieser Website seit: <time datetime="2026-11-02">2. November 2026</time>' if lang=='de' else 'Published on this site: <time datetime="2026-11-02">2 November 2026</time>')
        sub=german_subscription() if lang=='de' else re.search(r'<section class="subscription".*?</section>',template,re.S)[0]
        main=(f'<main id="main" class="reading"><a class="back" href="{home}#writing">← {back}</a><p class="eyebrow">'+('ARTIKEL' if lang=='de' else 'ARTICLE')+f' / KAY LUMMITSCH</p><h1>{esc(title)}</h1><p class="published-date">{date}</p><figure style="margin:0 0 2rem"><img class="reading-cover" src="/assets/{IMAGE}" alt="{esc(alt)}" width="1536" height="1024"><figcaption>'+('KI-generiertes Konzeptbild · ChatGPT' if lang=='de' else 'AI-generated concept image · ChatGPT')+'</figcaption></figure><div class="article-text">'+body(text)+'</div><div class="article-end"><span>/hugs/kay</span></div>'+references(lang)+f'<a class="back" href="{home}#writing">← {back}</a>'+sub+'</main>')
        source=re.sub(r'<main\b.*?</main>',lambda m:main,source,count=1,flags=re.S)
        if lang=='de': source=german_shell(source,title,description,EN,DE)
        else:
            source=source.replace('</nav></header>','</nav>'+switch(EN,DE,'en')+'</header>',1)
            source=source.replace('</head>',alternates(EN,DE)+'</head>',1)
        folder=OUT/route.strip('/');folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(source)
        homefile=OUT/home.strip('/')/'index.html';homepage=homefile.read_text()
        card=f'<a class="story" href="{route}"><div class="story-image"><img src="/assets/{IMAGE}" alt="{esc(alt)}" loading="lazy" width="1536" height="1024"></div><div class="story-meta">'+('Artikel' if lang=='de' else 'Article')+f' <span>↗</span></div><h3>{esc(title)}</h3><p class="published-date">{date}</p><p>{esc(description)}</p><span class="read">'+('Auf Deutsch lesen →' if lang=='de' else 'Read the article →')+'</span></a>'
        if f'href="{route}"' not in homepage:homepage=homepage.replace('<div class="stories">','<div class="stories">'+card,1)
        homefile.write_text(homepage)
    print('Generated Your Fault EN/DE.')
