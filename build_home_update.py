"""Homepage focus: mandate invitation up top, shorter post list, e-mail as main contact.

Runs after all other builders so it sees the final homepages. Idempotent.
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent
OUT = ROOT / 'public'
HOME_POSTS = 6

COPY = {
    'en': dict(
        home='/', overview='/writing/', rides='/interview-rides/', other_overview='/de/beitraege/',
        invite='I’m looking for companies that want to find out what’s really getting in their people’s way. As part of your leadership team, or for the time it takes to change it.',
        invite_link='Let’s talk →',
        mandate_old='I’m looking for one company serious about changing that — with a salaried leadership mandate, the authority to act, and the backing to follow through.',
        mandate_new='I’m looking for companies serious about changing that — as part of the leadership team, or for the time it takes. With the authority to act and the backing to follow through.',
        all_posts='All posts &amp; articles →',
        overview_title='Posts &amp; articles', overview_eyebrow='IDEAS TO TAKE TO WORK',
        overview_back='← Back to the homepage',
        overview_desc='All posts and articles by Kay Lummitsch on people, organizations and the reality of everyday work.',
        channel='Write to kay@kaylummitsch.com.',
        rides_footer='Interview Rides',
    ),
    'de': dict(
        home='/de/', overview='/de/beitraege/', rides='/de/interview-rides/', other_overview='/writing/',
        invite='Ich suche Unternehmen, die herausfinden wollen, was ihren Leuten wirklich im Weg steht. Als Teil der Führung oder für die Zeit, die es braucht, das zu ändern.',
        invite_link='Lass uns reden →',
        mandate_old='Ich suche ein Unternehmen, das daran ernsthaft etwas ändern will – mit einem angestellten Führungsmandat, dem Handlungsspielraum und der Rückendeckung, Veränderungen auch durchzuziehen.',
        mandate_new='Ich suche Unternehmen, die daran ernsthaft etwas ändern wollen – als Teil der Führung oder für die Zeit, die es braucht. Mit Handlungsspielraum und der Rückendeckung, Veränderungen auch durchzuziehen.',
        all_posts='Alle Posts &amp; Artikel →',
        overview_title='Posts &amp; Artikel', overview_eyebrow='GEDANKEN FÜR DEN ARBEITSALLTAG',
        overview_back='← Zur Startseite',
        overview_desc='Alle Posts und Artikel von Kay Lummitsch über Menschen, Organisationen und den echten Arbeitsalltag.',
        channel='Schreib an kay@kaylummitsch.com.',
        rides_footer='Interview Rides',
    ),
}

STORY = re.compile(r'<a class="story" href="[^"]*">.*?</a>(?=<a class="story"|</div>|$)', re.S)


def stories_block(source):
    match = re.search(r'<div class="stories">(.*?)</div></section>', source, re.S)
    return match, STORY.findall(match.group(1))


def update_home(lang, c):
    path = OUT / c['home'].strip('/') / 'index.html' if c['home'] != '/' else OUT / 'index.html'
    source = path.read_text()

    # 1. Mandate as an invitation, directly under the hero line.
    source = re.sub(r'<p class="mandate-invite">.*?</p>', '', source, flags=re.S)
    invite = f'<p class="mandate-invite">{c["invite"]} <a href="{c["home"]}#contact">{c["invite_link"]}</a></p>'
    source = re.sub(r'(<p class="intro">.*?</p>)', lambda m: m[1] + invite, source, count=1, flags=re.S)
    source = source.replace(c['mandate_old'], c['mandate_new'])

    # 2. Interview Rides leave the homepage; the subpage stays, linked in the footer.
    source = re.sub(r'<section class="rides-teaser".*?</section>\s*', '', source, flags=re.S)

    # 3. Only the newest posts on the homepage, plus a link to the overview.
    match, cards = stories_block(source)
    all_cards = ''.join(cards)
    source = source[:match.start(1)] + ''.join(cards[:HOME_POSTS]) + source[match.end(1):]
    source = re.sub(r'<p class="all-posts">.*?</p>', '', source, flags=re.S)
    more = f'<p class="all-posts"><a class="text-link" href="{c["overview"]}">{c["all_posts"]}</a></p>'
    source = re.sub(r'(<div class="stories">.*?</div>)(</section>)', lambda m: m[1] + more + m[2], source, count=1, flags=re.S)

    # 4. E-mail becomes the main contact; LinkedIn stays in the footer only.
    source = re.sub(r'<div class="contact-actions">.*?</div>',
                    '<div class="contact-actions"><a class="button light" href="mailto:kay@kaylummitsch.com">YOU BETTER CALL KAY. ↗</a></div>',
                    source, count=1, flags=re.S)
    source = re.sub(r'<p class="contact-channel">.*?</p>', f'<p class="contact-channel">{c["channel"]}</p>', source, count=1, flags=re.S)

    path.write_text(source)
    return source, all_cards


def write_overview(lang, c, home_source, all_cards):
    source = home_source
    main = (f'<main id="main" class="posts-overview"><section class="writing" id="writing"><a class="back" href="{c["home"]}">{c["overview_back"]}</a>'
            f'<div class="section-heading"><div><p class="eyebrow">{c["overview_eyebrow"]}</p><h1>{c["overview_title"]}.</h1></div></div>'
            f'<div class="stories">{all_cards}</div></section></main>')
    source = re.sub(r'<main\b.*?</main>', main, source, count=1, flags=re.S)
    source = re.sub(r'<title>.*?</title>', f'<title>{c["overview_title"]} | Kay Lummitsch</title>', source, count=1)
    for key in ['property="og:title"', 'name="twitter:title"']:
        source = re.sub(r'<meta ' + key + r' content="[^"]*">', f'<meta {key} content="{c["overview_title"]}">', source)
    for key in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        source = re.sub(r'<meta ' + key + r' content="[^"]*">', f'<meta {key} content="{c["overview_desc"]}">', source)
    source = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://kaylummitsch.com{c["overview"]}">', source)
    source = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="https://kaylummitsch.com{c["overview"]}">', source)
    # Pair the two overview pages in the language switch and alternates.
    en, de = ('/writing/', '/de/beitraege/')
    source = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', source)
    source = source.replace('</head>', ''.join(f'<link rel="alternate" hreflang="{code}" href="https://kaylummitsch.com{url}">' for code, url in [('en', en), ('de', de), ('x-default', en)]) + '</head>', 1)
    source = re.sub(r'(<div class="language-switch".*?</div>)',
                    lambda m: m[1].replace('href="/de/"', f'href="{de}"').replace('href="/"', f'href="{en}"'),
                    source, count=1, flags=re.S)
    # Sender script is only needed where the signup form is embedded.
    if 'data-sender-form-id' not in source:
        source = re.sub(r'<script>\s*\(function\(s,e,n,d,er\).*?</script>', '', source, count=1, flags=re.S)
    folder = OUT / c['overview'].strip('/')
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(source)


def footer_rides_link():
    for file in OUT.rglob('index.html'):
        source = file.read_text()
        if 'class="footer-rides"' in source or '<footer>' not in source:
            continue
        de = '<html lang="de">' in source
        href = COPY['de' if de else 'en']['rides']
        link = f'<a class="footer-rides" href="{href}">Interview Rides</a>'
        source = re.sub(r'(<footer>.*?LinkedIn[^<]*</a>)', lambda m: m[1] + link, source, count=1, flags=re.S)
        file.write_text(source)


def build():
    for lang, c in COPY.items():
        home_source, all_cards = update_home(lang, c)
        write_overview(lang, c, home_source, all_cards)
    footer_rides_link()


if __name__ == '__main__':
    build()
