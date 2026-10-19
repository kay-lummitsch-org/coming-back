from pathlib import Path
import json, html, re
from datetime import date
import xml.etree.ElementTree as ET

ROOT=Path(__file__).parent
OUT=ROOT/'public'
OUT.mkdir(exist_ok=True)
texts=json.loads((ROOT/'content/source-texts.json').read_text())
texts['on-how-we-see-people']=(ROOT/'content/on-how-we-see-people.txt').read_text()
texts['100-percent-kay']=(ROOT/'content/100-percent-kay.txt').read_text()
posts=[
 ('until-the-cat-jumps','Your Transformation Works. Until the Cat Jumps.','Article','Motorcycling, yoga, and what survives the return to everyday life.','until-the-cat-jumps.webp','until-the-cat-jumps'),
 ('on-how-we-see-people','On How We See People','Article','When a Difference Makes the Difference','on-how-we-see-people.webp','on-how-we-see-people'),
 ('rethink-your-pretzel','What Happens If AI Really Kicks In?','Article','Whose Chair Tips Over First?','rethink-your-pretzel.webp','rethink-your-pretzel'),
 ('100-percent-kay','100% Kay','Post','A call from Uli. A little discomfort. And a few words about writing with AI.','kay.webp','100-percent-kay'),
 ('undercover-kay','Undercover Kay','Article','I love the tears. And the moment a boss realises: I had no idea. What happens next?','undercover-kay.webp','libfile_5e97d541ae508191b0ea993f3dbabecf'),
 ('workarounder','Workarounder','Post','What could we do if we didn’t have to work around our organizations?','workarounder.webp','libfile_3ab6bd800f0c81918737556f2e3fa887'),
 ('the-dunning-kruger-approximation','The Dunning–Kruger Approximation','Article','A little knowledge. A lot of confidence. And some very uncooperative leaves.','dunning-kruger.webp','libfile_0b5997c1e0e08191abfc41d4bd5034fe'),
 ('tuesday-1017','Tuesday, 10:17 AM','Post','Every organization has its aspirations. And then there is Tuesday.','tuesday.webp','libfile_7146b0a842b481918b27074ebaa1a4df'),
 ('the-promise','The Promise','Post','What if we gave 10,000 people back just one hour a week?','promise.webp','libfile_c0cfe72db8588191a0d57c42a5ad175c'),
 ('your-most-wasted-resource-is-human','Your Most Wasted Resource Is Human','Article','What I learned when I left the ivory tower and put on work clothes.','human.webp','libfile_7cc035c7c02c81918fd570df24902cf7'),
]
# Dates record first publication on this website, not inferred LinkedIn dates.
site_dates = {
 'until-the-cat-jumps':'2026-10-19',
 'on-how-we-see-people':'2026-10-16', '100-percent-kay':'2026-10-16',
 'rethink-your-pretzel':'2026-10-14', 'undercover-kay':'2026-10-13',
 'workarounder':'2026-10-11', 'the-dunning-kruger-approximation':'2026-10-11',
 'tuesday-1017':'2026-10-11', 'the-promise':'2026-10-11',
 'your-most-wasted-resource-is-human':'2026-10-11',
}
def dated(slug):
 value=site_dates[slug]
 label=date.fromisoformat(value).strftime('%d %B %Y').lstrip('0')
 result=f'<p class="published-date">Published on this site: <time datetime="{value}">{label}</time></p>'
 if slug=='100-percent-kay':
  result+='<p class="published-date original-date">Originally posted on LinkedIn: <time datetime="2026-10-15">15 October 2026</time></p>'
 return result
def esc(s):return html.escape(s,quote=True)
def nav():return '''<a class="skip" href="#main">Skip to content</a><header><a class="name" href="/">KAY LUMMITSCH<span>People &amp; Transformation</span></a><nav aria-label="Main navigation"><a href="/#approach">The approach</a><a href="/#writing">Posts &amp; articles</a><a href="/#booklet">Booklets</a><a href="/#contact">Let’s talk ↗</a></nav></header>'''
def foot():return '''<footer><span>© 2026 Kay Lummitsch</span><a href="https://www.linkedin.com/in/lummitsch/" target="_blank" rel="noopener noreferrer">Find me on LinkedIn ↗</a><span>Made with curiosity. /kay</span></footer>'''
SENDER_SCRIPT = """<script>
(function(s,e,n,d,er){s['Sender']=er;s[er]=s[er]||function(){(s[er].q=s[er].q||[]).push(arguments)};s[er].l=1*new Date();s[er].on=function(event,callback){s[er].listeners=s[er].listeners||{};(s[er].listeners[event]=s[er].listeners[event]||[]).push(callback)};var a=e.createElement(n),m=e.getElementsByTagName(n)[0];a.async=1;a.src=d;m.parentNode.insertBefore(a,m)})(window,document,'script','https://cdn.sender.net/accounts_resources/universal.js','sender');
sender('17c1f235ed7798');
</script>"""
def subscription():return '''<section class="subscription" id="subscribe" aria-labelledby="subscribe-heading"><div class="subscription-copy"><p class="eyebrow">STAY CURIOUS</p><h2 id="subscribe-heading">Good questions.<br>Worth keeping.</h2><p>New articles. Fresh questions. A little discomfort.<br>Straight to your inbox.</p></div><div class="subscription-form"><div style="text-align: left" class="sender-form-field" data-sender-form-id="epYyZ1"></div><p class="subscription-note">Sign up for new articles and posts from Kay. Confirm your email to join. Unsubscribe anytime. Your email address is processed by Sender to manage your subscription.</p><a class="subscription-fallback" href="https://stats.sender.net/forms/epYyZ1/view" target="_blank" rel="noopener noreferrer">Form not loading? Open the signup page.</a></div></section>'''
def share_metadata(title, desc, path, image, article_date=None):
 url='https://kaylummitsch.com'+path
 image_url='https://kaylummitsch.com/assets/'+image
 kind='article' if article_date else 'website'
 tags=(f'<link rel="canonical" href="{esc(url)}">'
  f'<meta property="og:type" content="{kind}">'
  '<meta property="og:site_name" content="Kay Lummitsch">'
  '<meta property="og:locale" content="en_GB">'
  f'<meta property="og:title" content="{esc(title)}">'
  f'<meta property="og:description" content="{esc(desc)}">'
  f'<meta property="og:url" content="{esc(url)}">'
  f'<meta property="og:image" content="{esc(image_url)}">'
  f'<meta property="og:image:alt" content="{esc(title)}">'
  '<meta name="twitter:card" content="summary_large_image">'
  f'<meta name="twitter:title" content="{esc(title)}">'
  f'<meta name="twitter:description" content="{esc(desc)}">'
  f'<meta name="twitter:image" content="{esc(image_url)}">'
  f'<meta name="twitter:image:alt" content="{esc(title)}">')
 if article_date:tags+=f'<meta property="article:published_time" content="{article_date}">'
 return tags

def page(title,desc,body,path='/',image='kay.webp',article_date=None):return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Kay Lummitsch</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#f45b16"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css">{share_metadata(title,desc,path,image,article_date)}{SENDER_SCRIPT if 'data-sender-form-id' in body else ''}</head><body>{nav()}{body}{foot()}</body></html>'''
cards=''.join(f'''<a class="story" href="/writing/{slug}/"><div class="story-image"><img src="/assets/{img}" alt="{esc(title)}" loading="lazy" width="1200" height="675"></div><div class="story-meta">{kind} <span>↗</span></div><h3>{esc(title)}</h3>{dated(slug)}<p>{esc(desc)}</p><span class="read">Read the {kind.lower()} →</span></a>''' for slug,title,kind,desc,img,_ in posts)
body=f'''<main id="main"><section class="hero"><div class="hero-copy"><h1>PEOPLE<br>FIRST<span class="orange">.</span><br><span class="hero-question">NOW WHAT?</span></h1><p class="intro">Let’s unlock human potential by removing the organizational barriers we create and keep in place.</p><a class="button" href="#approach">Let’s get into it <span>↓</span></a></div><div class="hero-art"><div class="orange-bang"><span>LESS<br>FRICTION.<br>MORE<br>AGENCY.</span></div><p>Better work.<br>Better results.<br>Better organizations.</p></div></section>
<section class="tuesday" id="approach"><p class="eyebrow">THE GAP WE NEED TO CLOSE</p><h2>Great aspirations.<br>Then it’s Tuesday,<br><span>10:17 AM.</span></h2><div class="tuesday-copy"><p>People First. Customer First. Empowerment. Trust.</p><p>Someone is waiting for a decision. Someone is chasing information. Someone has found another workaround.</p><p class="strong">What did we put in their way?</p><a class="text-link" href="/writing/tuesday-1017/">Meet Tuesday →</a></div></section>
<section class="approach"><div><p class="eyebrow">HOW WE RUN THE BUSINESS</p><h2>Build the conditions<br>for a damn<br>good job.</h2></div><div class="approach-list"><article><span>01</span><div><h3>Make good work possible.</h3><p>Find the barriers with the people closest to the work. Change the decisions, structures and habits that keep those barriers in place.</p></div></article><article><span>02</span><div><h3>Give people room to act.</h3><p>Put information, tools and authority where they can make a difference. Let speaking up lead to visible action.</p></div></article><article><span>03</span><div><h3>Keep the promises we sell.</h3><p>Bring customer promises, resources and the reality of delivery together. Then check whether the changes actually help.</p></div></article></div></section>
<section class="about" id="kay"><div class="portrait"><img src="/assets/kay.webp" alt="Kay Lummitsch" loading="lazy" width="800" height="1000"><span>SAME PERSON.<br>DIFFERENT WORK CLOTHES.</span></div><div class="about-copy"><p class="eyebrow">A LITTLE CONTEXT</p><h2>From the boardroom.<br>To the boiler room.<br>And back again.</h2><p>Seafarer. Submarine navigator. Programmer. Coach. API program leader. Teacher. International speaker. Facility technician.</p><p>I’ve spent years exploring what organizations could become. Then I picked up a grass trimmer and learned how much I still had to learn.</p><p>Doing the work changed my understanding of what people know, what organizations fail to hear, and what it takes to make a good working day possible.</p><p class="strong">I’m bringing those worlds together.</p><a class="text-link" href="/writing/your-most-wasted-resource-is-human/">Read the story →</a></div></section>
<section class="metrics" aria-label="Reach and experience"><dl><div><dt>LinkedIn followers</dt><dd>14K+</dd></div><div><dt>Booklets shared. Free of charge.</dt><dd>20K+</dd></div><div><dt>Years in the digital world</dt><dd>20+</dd></div></dl></section>
<section class="writing" id="writing"><div class="section-heading"><div><p class="eyebrow">IDEAS TO TAKE TO WORK</p><h2>Posts &amp; articles.</h2></div><p>Questions. Stories. A little discomfort.<br>Let’s get curious before we get corrective.</p></div><div class="stories">{cards}</div></section>
{subscription()}
<section class="booklet" id="booklet"><div class="book-image"><img src="/assets/booklet.webp" alt="People First — WTF! Booklet cover" loading="lazy" width="1200" height="800"></div><div><p class="eyebrow badge">UPCOMING</p><h2>PEOPLE FIRST<br>— WTF!</h2><p class="book-sub">DAMN GOOD ORGANIZATIONAL ADVICE.</p><p>A small book for people who want their people to have a good Tuesday. Short chapters. Real work. Uncomfortable questions. And room to think.</p><p>Currently in the making.</p><a class="text-link" href="/assets/why-i-wrote.pdf">A first look: Why I wrote this book ↗</a></div></section>
<section class="booklet classic" id="tdjm"><div><p class="eyebrow badge">ALL-TIME CLASSIC</p><h2>THE DIGITAL<br>JOURNEYMEN.</h2><p class="book-sub">DAMN GOOD DIGITAL ADVICE.</p><p>For people who really want to embrace change. A small book from my years in digital transformation. Short chapters. Big questions. Very little patience for protecting the status quo.</p><p>The technology has moved on. The people questions are still with us.</p><a class="text-link" href="/booklets/the-digital-journeymen/">Rediscover the booklet →</a></div><a class="book-image" href="/booklets/the-digital-journeymen/" aria-label="Explore The Digital Journeymen"><img src="/assets/tdjm-cover.webp" alt="The Digital Journeymen cover with orange All-Time Classic sticker" loading="lazy" width="1600" height="1128"></a></section>
<section class="contact" id="contact"><p class="eyebrow">THE MANDATE</p><h2>What is getting<br>in your people’s way?</h2><div><p>I’m looking for one company serious about changing that — with a salaried leadership mandate, the authority to act, and the backing to follow through.</p><p>Something getting in your people’s way? Let’s talk.</p><div class="contact-actions"><a class="button light" href="https://www.linkedin.com/in/lummitsch/" target="_blank" rel="noopener noreferrer">YOU BETTER CALL KAY. ↗</a><a class="button contact-email" href="mailto:kay@kaylummitsch.com">Email Kay ↗</a></div><p class="contact-channel">Connect on LinkedIn or email kay@kaylummitsch.com.</p></div></section></main>'''
(OUT/'index.html').write_text(page('People & Transformation','People & Transformation. Less friction. More agency. Better work. Kay Lummitsch brings organizational change and the reality of everyday work together.',body))
headings={'The leaves disagreed','“Now I’ve got it.”','A little knowledge. A very complete explanation.','Murphy arranges the site visit','The bottle-cleaner trap','How do we practise Humility — and avoid the “I know it all” trap?','LESS FRICTION','PEOPLE EMPOWERMENT & MORE AGENCY','A VOICE THAT COUNTS','POTENTIAL PUT TO WORK','I left the ivory tower.','The people our ease of life rests on.','“Wie geht’s?”','What if we actually meant “People First”?','And now there is AI.','So here is what I know now.','Only call me if you mean it.','And if nobody calls?'}
for slug,title,kind,desc,img,key in posts:
 text='' if slug=='until-the-cat-jumps' else texts[key].strip()
 if slug=='the-dunning-kruger-approximation':
  text=text[text.find('THE DUNNING–KRUGER APPROXIMATION\nOh,'):]
 if slug=='your-most-wasted-resource-is-human':
  text=text[text.find('YOUR MOST WASTED RESOURCE IS HUMAN.\nAnd I\'m'):]
 lines=[l.strip() for l in text.splitlines() if l.strip()]
 if lines and lines[0].casefold()==title.casefold():lines=lines[1:]
 if slug=='your-most-wasted-resource-is-human' and lines[0]=='YOUR MOST WASTED RESOURCE IS HUMAN.':lines=lines[1:]
 if slug=='on-how-we-see-people':
  lines=[line for line in lines if line not in {desc, '/hugs/kay'}]
 if slug=='100-percent-kay':
  lines=[line for line in lines if line != '/thanks/uli/hugs/kay']
 parts=[]
 for line in lines:
  if slug=='rethink-your-pretzel' and line in {
   'Every system works perfectly on its own. Together, they’re idiots.',
   'In an office built around repetitive administrative work, agents could perform 80% of the standard tasks better and faster.',
   'You must plan for the possibility that your own role becomes unnecessary.',
   'Your role is not guaranteed. Your dignity is.',
   'Mine too.', 'Where do we actually add value?', 'START TO ADD VALUE!'}:
   parts.append('<p><strong>'+esc(line)+'</strong></p>')
  elif line in headings or (slug=='on-how-we-see-people' and line in {'HOW WE SEE PEOPLE','How this article came about:'}):
   if line=='Murphy arranges the site visit':parts.append('<figure><img src="/assets/learning-curve.webp" alt="Illustrative confidence curve: early certainty, discovery of complexity, and gradual understanding. Not the curve measured in the original Dunning–Kruger study." loading="lazy"><figcaption>An illustration of confidence while learning, not a measured research curve.</figcaption></figure>')
   parts.append('<h2>'+esc(line)+'</h2>')
  else:parts.append('<p>'+esc(line)+'</p>')
 if slug=='until-the-cat-jumps':
  parts=[(ROOT/'content/until-the-cat-jumps.html').read_text()]
 source_note='<p class="archive-note">This article preserves the original Comeback text, including the role terminology used at the time.</p>' if slug=='your-most-wasted-resource-is-human' else ''
 signature = "/hugs/kay" if slug in {"rethink-your-pretzel","on-how-we-see-people"} else "/kay"
 if slug=='100-percent-kay':signature='/thanks/uli/hugs/kay'
 if slug=='until-the-cat-jumps':signature='/hugs/kay'
 main=f'''<main id="main" class="reading"><a class="back" href="/#writing">← All posts &amp; articles</a><p class="eyebrow">{kind} / KAY LUMMITSCH</p><h1>{esc(title)}</h1>{dated(slug)}<p class="deck">{esc(desc)}</p><img class="reading-cover" src="/assets/{img}" alt="{esc(title)}" width="1200" height="675">{source_note}<div class="article-text">{''.join(parts)}</div><div class="article-end"><span>{signature}</span><a href="https://www.linkedin.com/in/lummitsch/" target="_blank" rel="noopener noreferrer">Visit my LinkedIn profile ↗</a></div><a class="back" href="/#writing">← Explore more ideas</a>{subscription()}</main>'''
 folder=OUT/'writing'/slug;folder.mkdir(parents=True,exist_ok=True);rendered = page(title,desc,main,path=f'/writing/{slug}/',image=img,article_date=site_dates[slug])
 if slug=='until-the-cat-jumps':
  rendered=rendered.replace(f'alt="{esc(title)}" width="1200" height="675"', 'alt="Kay’s black-and-white tomcat walking towards the camera on grey asphalt" width="1732" height="908"')
 if slug=='on-how-we-see-people':
  rendered=rendered.replace('Visit my LinkedIn profile ↗','Read and discuss on LinkedIn ↗').replace('href="https://www.linkedin.com/in/lummitsch/" target="_blank" rel="noopener noreferrer">Read and discuss','href="https://www.linkedin.com/pulse/how-we-see-people-kay-lummitsch-jqzze/" target="_blank" rel="noopener noreferrer">Read and discuss')
 if slug=='100-percent-kay':
  rendered=rendered.replace('Visit my LinkedIn profile ↗','Read and discuss on LinkedIn ↗').replace('href="https://www.linkedin.com/in/lummitsch/" target="_blank" rel="noopener noreferrer">Read and discuss','href="https://www.linkedin.com/feed/update/urn:li:activity:7516459664654381056/" target="_blank" rel="noopener noreferrer">Read and discuss')
 (folder/'index.html').write_text(rendered)
print('Generated home and',len(posts),'reading pages.')

booklet_body='''<main id="main" class="booklet-reading"><a class="back" href="/#booklet">← The booklets</a><section class="booklet-hero"><div><p class="eyebrow badge">ALL-TIME CLASSIC / KAY LUMMITSCH</p><h1>THE DIGITAL<br>JOURNEYMEN.</h1><p class="book-sub">DAMN GOOD DIGITAL ADVICE.</p><p class="booklet-intro">For people who really want to embrace change.</p><div class="booklet-actions"><a class="button" href="/assets/the-digital-journeymen.pdf" target="_blank" rel="noopener">Read the booklet ↗</a><a class="text-link" href="/assets/the-digital-journeymen.pdf" download="The-Digital-Journeymen.pdf">Download PDF ↓</a></div><p class="booklet-detail">32 pages · English · Free to read</p></div><div class="book-image"><img src="/assets/tdjm-cover.webp" alt="The Digital Journeymen. Damn Good Digital Advice. Cover by Kay Lummitsch with All-Time Classic sticker." width="1600" height="1128"></div></section>
<section class="booklet-context"><p class="eyebrow">WHY IT STILL MATTERS TO ME</p><h2>There’s nothing<br>but people.</h2><div><p>I wrote this book after years of working on an API program and talking to people trying to change their organizations.</p><p>We had tools. We had strategies. We had very convincing explanations for why real change would have to wait.</p><p>So I put my questions into a small book. Corporate DNA. Resistance. The status quo. And a little Pippi Longstocking.</p><p class="strong">Reading it today, I recognise the questions that still keep me busy.</p><p>PEOPLE FIRST — WTF! is where I’m taking them next.</p><p class="archive-note">This is the original booklet with an updated cover. The chapters, acknowledgements and historical contact details inside remain as published.</p></div></section>
<section class="booklet-preview"><p class="eyebrow">A LOOK INSIDE</p><h2>Short chapters.<br>Room to think.</h2><figure><img src="/assets/tdjm-dna.webp" alt="Original pages 6 and 7: On Changing One’s Digital DNA" loading="lazy" width="2000" height="705"><figcaption>On changing one’s digital DNA · Pages 6–7</figcaption></figure><figure><img src="/assets/tdjm-people.webp" alt="Original pages 22 and 23: There’s Nothing but People, and Change Comes Only from People" loading="lazy" width="2000" height="705"><figcaption>There’s nothing but people · Pages 22–23</figcaption></figure><a class="button" href="/assets/the-digital-journeymen.pdf" target="_blank" rel="noopener">Read all 32 pages ↗</a></section>
<section class="booklet-next"><p class="eyebrow badge">THE NEXT CHAPTER / UPCOMING</p><h2>PEOPLE FIRST — WTF!</h2><p>Damn good organizational advice. Currently in the making.</p><a class="text-link" href="/#booklet">Meet the new booklet →</a></section></main>'''
booklet_dir=OUT/'booklets/the-digital-journeymen'
booklet_dir.mkdir(parents=True,exist_ok=True)
(booklet_dir/'index.html').write_text(page('The Digital Journeymen','Damn good digital advice for people who really want to embrace change. Read and download Kay Lummitsch’s original 32-page booklet.',booklet_body,path='/booklets/the-digital-journeymen/',image='tdjm-cover.webp'))

from build_german import build as build_german
build_german()

from build_interview_rides import build as build_interview_rides
build_interview_rides()

# Search discovery: regenerate alongside published HTML pages.
SITE_URL = 'https://kaylummitsch.com'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', SITEMAP_NS)
urlset = ET.Element(f'{{{SITEMAP_NS}}}urlset')
for published_page in sorted(OUT.rglob('index.html')):
    # Future noindex pages should not be advertised to search engines.
    if re.search(r'<meta\b[^>]*\bcontent=[\"\'][^\"\']*\bnoindex\b', published_page.read_text(), re.I):
        continue
    relative = published_page.parent.relative_to(OUT).as_posix()
    route = '/' if relative == '.' else f'/{relative}/'
    url = ET.SubElement(urlset, f'{{{SITEMAP_NS}}}url')
    ET.SubElement(url, f'{{{SITEMAP_NS}}}loc').text = SITE_URL + route
ET.indent(urlset, space='  ')
ET.ElementTree(urlset).write(OUT/'sitemap.xml', encoding='utf-8', xml_declaration=True)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
