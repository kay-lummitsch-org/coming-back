"""German preview and explicit language pairs for the existing static site."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).parent
OUT = ROOT / 'public'
PAIRS = {
 '/': '/de/',
 '/writing/on-how-we-see-people/': '/de/artikel/menschenbild/',
 '/writing/100-percent-kay/': '/de/artikel/100-prozent-kay/',
}

def switch(en, de, language):
    def item(code, url):
        if code == language:
            return f'<span aria-current="page">{code.upper()}</span>'
        return f'<a href="{url}" hreflang="{code}" lang="{code}" aria-label="'+('Deutsch' if code == 'de' else 'English')+f'">{code.upper()}</a>'
    return '<div class="language-switch" aria-label="'+('Sprache wählen' if language == 'de' else 'Choose language')+'">'+item('de', de)+'<span aria-hidden="true">|</span>'+item('en', en)+'</div>'

def alternates(en, de):
    return ''.join(f'<link rel="alternate" hreflang="{code}" href="https://kaylummitsch.com{url}">' for code,url in [('en',en),('de',de),('x-default',en)])

def de_nav(en, de):
    return '<a class="skip" href="#main">Zum Inhalt</a><header><a class="name" href="/de/">KAY LUMMITSCH<span>Menschen &amp; Transformation</span></a><nav aria-label="Hauptnavigation"><a href="/de/#approach">Mein Ansatz</a><a href="/de/#writing">Posts &amp; Artikel</a><a href="/de/#booklet">Booklets</a><a href="/de/#contact">Lass uns reden ↗</a></nav>'+switch(en,de,'de')+'</header>'

def german_shell(source, title, desc, en, de):
    source = source.replace('<html lang="en">','<html lang="de">').replace('content="en_GB"','content="de_CH"')
    source = re.sub(r'<title>.*?</title>', '<title>'+html.escape(title)+' | Kay Lummitsch</title>',source,count=1)
    for key in ['name="description"','property="og:description"','name="twitter:description"']:
        source=re.sub(r'<meta '+key+r' content="[^"]*">','<meta '+key+' content="'+html.escape(desc,quote=True)+'">',source)
    for key in ['property="og:title"','name="twitter:title"']:
        source=re.sub(r'<meta '+key+r' content="[^"]*">','<meta '+key+' content="'+html.escape(title,quote=True)+'">',source)
    source=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="https://kaylummitsch.com{de}">',source)
    source=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="https://kaylummitsch.com{de}">',source)
    source=re.sub(r'<a class="skip".*?</header>',de_nav(en,de),source,count=1,flags=re.S)
    source=source.replace('Find me on LinkedIn ↗','Auf LinkedIn verbinden ↗').replace('Made with curiosity. /kay','Mit Neugier gemacht. /kay')
    source=source.replace('</head>',alternates(en,de)+'</head>',1)
    return source

def build():
    home=(OUT/'index.html').read_text()
    german=german_shell(home,'Menschen & Transformation','Organisationsbarrieren abbauen. Menschen Handlungsspielraum geben. Bessere Arbeit ermöglichen. Kay Lummitsch, Zürich.','/','/de/')
    translations={
     'PEOPLE<br>FIRST':'MENSCHEN<br>ZUERST', 'NOW WHAT?':'UND JETZT?',
     'Let’s unlock human potential by removing the organizational barriers we create and keep in place.':'Menschen können mehr. Wenn wir die organisatorischen Barrieren abbauen, die wir selbst schaffen und aufrechterhalten.',
     'Let’s get into it':'Schauen wir genauer hin', 'LESS<br>FRICTION.<br>MORE<br>AGENCY.':'WENIGER<br>REIBUNG.<br>MEHR<br>SPIELRAUM.',
     'Better work.<br>Better results.<br>Better organizations.':'Bessere Arbeit.<br>Bessere Ergebnisse.<br>Bessere Organisationen.',
     'THE GAP WE NEED TO CLOSE':'ZWISCHEN ANSPRUCH UND ALLTAG',
     'Great aspirations.<br>Then it’s Tuesday,<br><span>10:17 AM.</span>':'Grosse Versprechen.<br>Dann ist Dienstag,<br><span>10:17 Uhr.</span>',
     'People First. Customer First. Empowerment. Trust.':'Menschen zuerst. Kunden zuerst. Eigenverantwortung. Vertrauen.',
     'Someone is waiting for a decision. Someone is chasing information. Someone has found another workaround.':'Jemand wartet auf eine Entscheidung. Jemand läuft einer Information hinterher. Jemand hat wieder einen Workaround gefunden.',
     'What did we put in their way?':'Was haben wir ihnen in den Weg gestellt?', 'Meet Tuesday →':'Dienstag kennenlernen · EN →',
     'HOW WE RUN THE BUSINESS':'WIE WIR UNSERE ORGANISATION FÜHREN',
     'Build the conditions<br>for a damn<br>good job.':'Die Bedingungen<br>für verdammt gute<br>Arbeit schaffen.',
     'Make good work possible.':'Gute Arbeit möglich machen.',
     'Find the barriers with the people closest to the work. Change the decisions, structures and habits that keep those barriers in place.':'Die Hindernisse mit den Menschen finden, die die Arbeit machen. Entscheidungen, Strukturen und Gewohnheiten verändern, die diese Hindernisse aufrechterhalten.',
     'Give people room to act.':'Menschen Handlungsspielraum geben.',
     'Put information, tools and authority where they can make a difference. Let speaking up lead to visible action.':'Informationen, Werkzeuge und Entscheidungsbefugnisse dorthin bringen, wo sie etwas bewirken. Dafür sorgen, dass auf offene Worte sichtbares Handeln folgt.',
     'Keep the promises we sell.':'Die Versprechen halten, die wir verkaufen.',
     'Bring customer promises, resources and the reality of delivery together. Then check whether the changes actually help.':'Kundenversprechen, Ressourcen und die tatsächliche Arbeit zusammenbringen. Und dann prüfen, ob die Veränderungen wirklich helfen.',
     'SAME PERSON.<br>DIFFERENT WORK CLOTHES.':'DERSELBE MENSCH.<br>ANDERE ARBEITSKLEIDUNG.', 'A LITTLE CONTEXT':'EIN BISSCHEN HINTERGRUND',
     'From the boardroom.<br>To the boiler room.<br>And back again.':'Aus der Chefetage.<br>In den Technikraum.<br>Und wieder zurück.',
     'Seafarer. Submarine navigator. Programmer. Coach. API program leader. Teacher. International speaker. Facility technician.':'Seefahrer. U-Boot-Navigator. Programmierer. Coach. API-Programmleiter. Dozent. Internationaler Speaker. Haustechniker.',
     'I’ve spent years exploring what organizations could become. Then I picked up a grass trimmer and learned how much I still had to learn.':'Jahrelang habe ich daran gearbeitet, was aus Organisationen werden könnte. Dann nahm ich einen Freischneider in die Hand und merkte, wie viel ich noch zu lernen hatte.',
     'Doing the work changed my understanding of what people know, what organizations fail to hear, and what it takes to make a good working day possible.':'Die Arbeit selbst zu machen hat meinen Blick verändert: auf das Wissen der Menschen, auf das, was Organisationen überhören, und auf die Bedingungen für einen guten Arbeitstag.',
     'I’m bringing those worlds together.':'Ich bringe diese Welten zusammen.', 'Read the story →':'Die Geschichte lesen · EN →',
     'Reach and experience':'Reichweite und Erfahrung', 'LinkedIn followers':'Follower auf LinkedIn', 'Booklets shared. Free of charge.':'Booklets geteilt. Kostenlos.', 'Years in the digital world':'Jahre in der digitalen Welt',
     'IDEAS TO TAKE TO WORK':'GEDANKEN FÜR DEN ARBEITSALLTAG', 'Posts &amp; articles.':'Posts &amp; Artikel.',
     'Questions. Stories. A little discomfort.<br>Let’s get curious before we get corrective.':'Fragen. Geschichten. Ein bisschen Unbehagen.<br>Erst neugierig werden. Dann korrigieren.',
     'UPCOMING':'IN ARBEIT', 'DAMN GOOD ORGANIZATIONAL ADVICE.':'VERDAMMT GUTE GEDANKEN ZUR ORGANISATION.',
     'A small book for people who want their people to have a good Tuesday. Short chapters. Real work. Uncomfortable questions. And room to think.':'Ein kleines Buch für Menschen, die wollen, dass ihre Leute einen guten Dienstag haben. Kurze Kapitel. Echte Arbeit. Unbequeme Fragen. Und Platz zum Denken.',
     'Currently in the making.':'Entsteht gerade.', 'A first look: Why I wrote this book ↗':'Ein erster Blick: Warum ich dieses Buch schreibe · EN ↗',
     'ALL-TIME CLASSIC':'DER KLASSIKER', 'DAMN GOOD DIGITAL ADVICE.':'VERDAMMT GUTE GEDANKEN ZUM DIGITALEN WANDEL.',
     'For people who really want to embrace change. A small book from my years in digital transformation. Short chapters. Big questions. Very little patience for protecting the status quo.':'Für Menschen, die Veränderung wirklich wollen. Ein kleines Buch aus meinen Jahren in der digitalen Transformation. Kurze Kapitel. Grosse Fragen. Sehr wenig Geduld für das Bewahren des Status quo.',
     'The technology has moved on. The people questions are still with us.':'Die Technologie hat sich weiterentwickelt. Die Fragen zu uns Menschen sind geblieben.',
     'Rediscover the booklet →':'Das Booklet wiederentdecken · EN →', 'THE MANDATE':'DAS MANDAT',
     'What is getting<br>in your people’s way?':'Was steht Ihren<br>Leuten im Weg?',
     'I’m looking for one company serious about changing that — with a salaried leadership mandate, the authority to act, and the backing to follow through.':'Ich suche ein Unternehmen, das daran ernsthaft etwas ändern will – mit einem angestellten Führungsmandat, dem Handlungsspielraum und der Rückendeckung, Veränderungen auch durchzuziehen.',
     'Something getting in your people’s way? Let’s talk.':'Steht Deinen Leuten etwas im Weg? Lass uns reden.', 'Email Kay ↗':'Kay eine E-Mail schreiben ↗',
     'Connect on LinkedIn or email kay@kaylummitsch.com.':'Auf LinkedIn verbinden oder an kay@kaylummitsch.com schreiben.',
    }
    for old,new in translations.items():german=german.replace(old,new)
    german=german.replace('href="/#','href="/de/#')
    # Keep untranslated content explicit rather than pretending these are German pages.
    german=german.replace('Read the article →','Auf Englisch lesen →').replace('Read the post →','Auf Englisch lesen →')
    german=german.replace('Published on this site:','Auf dieser Website seit:').replace('Originally posted on LinkedIn:','Ursprünglich auf LinkedIn:').replace('October 2026','Oktober 2026')
    german=re.sub(r'(>\d{1,2}) Oktober',r'\1. Oktober',german)
    german=german.replace('Article <span>','Artikel <span>').replace('Explore The Digital Journeymen','The Digital Journeymen entdecken')
    german=german.replace('On How We See People','Menschenbild').replace('When a Difference Makes the Difference','Wenn Unterschiede Unterschiede machen')
    german=german.replace('href="/writing/on-how-we-see-people/"','href="/de/artikel/menschenbild/"').replace('href="/writing/100-percent-kay/"','href="/de/artikel/100-prozent-kay/"')
    german=german.replace('A call from Uli. A little discomfort. And a few words about writing with AI.','Ein Anruf von Uli. Ein bisschen Unbehagen. Und ein paar Worte zum Schreiben mit KI.')
    for target in ['/de/artikel/menschenbild/','/de/artikel/100-prozent-kay/']:
        german=re.sub(r'(<a class="story" href="'+re.escape(target)+r'".*?<span class="read">)Auf Englisch lesen',r'\1Auf Deutsch lesen',german,flags=re.S)
    german=re.sub(r'<section class="subscription".*?</section>',german_subscription(),german,flags=re.S)
    write('/de/',german)
    german_article('menschenbild-de.txt','Menschenbild','Wenn Unterschiede Unterschiede machen','/writing/on-how-we-see-people/','/de/artikel/menschenbild/','on-how-we-see-people.webp')
    german_article('100-percent-kay-de.txt','100% Kay','Ein Anruf von Uli. Ein bisschen Unbehagen. Und ein paar Worte zum Schreiben mit KI.','/writing/100-percent-kay/','/de/artikel/100-prozent-kay/','kay.webp')
    # English pages retain their URLs; paired articles switch to their actual translation.
    for file in OUT.rglob('index.html'):
        if 'de' in file.relative_to(OUT).parts:continue
        route='/'+file.parent.relative_to(OUT).as_posix().strip('./')+'/'
        if route=='//':route='/'
        source=file.read_text()
        de=PAIRS.get(route,'/de/')
        source=source.replace('</nav></header>','</nav>'+switch(route,de,'en')+'</header>',1)
        if route in PAIRS:source=source.replace('</head>',alternates(route,de)+'</head>',1)
        file.write_text(source)

def german_subscription():
    return '<section class="subscription" id="subscribe"><div class="subscription-copy"><p class="eyebrow">NEUGIERIG BLEIBEN</p><h2>Gute Fragen.<br>Zum Weiterdenken.</h2><p>Neue Artikel. Frische Gedanken. Ein bisschen Unbehagen.<br>Direkt in Dein Postfach.</p></div><div class="subscription-form"><a class="button" href="https://stats.sender.net/forms/epYyZ1/view" target="_blank" rel="noopener noreferrer">Auf dem Laufenden bleiben ↗</a><p class="subscription-note">Das Anmeldeformular ist auf Englisch. Versand über Sender. Du kannst Dich jederzeit abmelden.</p></div></section>'

def write(route,source):
    folder=OUT/route.strip('/');folder.mkdir(parents=True,exist_ok=True);(folder/'index.html').write_text(source)

def german_article(filename,title,desc,en,de,image):
    source=(OUT/en.strip('/')/'index.html').read_text()
    source=german_shell(source,title,desc,en,de)
    text=(ROOT/'content'/filename).read_text().strip()
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    if filename=='menschenbild-de.txt':lines=lines[2:]
    parts=[]
    for line in lines:
        if line=='DAS MENSCHENBILD':parts.append('<h2>Das Menschenbild</h2>')
        elif line=='Wie dieser Artikel entstanden ist:':parts.append('<h2>'+html.escape(line)+'</h2>')
        else:parts.append('<p>'+html.escape(line)+'</p>')
    body='<main id="main" class="reading"><a class="back" href="/de/#writing">← Alle Posts &amp; Artikel</a><p class="eyebrow">'+('ARTIKEL' if filename=='menschenbild-de.txt' else 'POST')+' / KAY LUMMITSCH</p><h1>'+html.escape(title)+'</h1><p class="deck">'+html.escape(desc)+'</p><img class="reading-cover" src="/assets/'+image+'" alt="'+html.escape(title)+'"><div class="article-text">'+''.join(parts)+'</div><div class="article-end"><a href="https://www.linkedin.com/'+('pulse/how-we-see-people-kay-lummitsch-jqzze/' if filename=='menschenbild-de.txt' else 'feed/update/urn:li:activity:7516459664654381056/')+'" target="_blank" rel="noopener noreferrer">Auf LinkedIn mitreden · EN ↗</a></div><a class="back" href="/de/#writing">← Weitere Gedanken entdecken</a>'+german_subscription()+'</main>'
    source=re.sub(r'<main\b.*?</main>',body,source,flags=re.S,count=1)
    # Publication date metadata from the English archive does not describe this unpublished translation.
    source=re.sub(r'<meta property="article:published_time"[^>]*>','',source)
    write(de,source)

if __name__=='__main__':build()
