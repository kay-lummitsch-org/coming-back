"""Two booklets: new PEOPLE FIRST — WTF! cover and the Agents Edition as "coming next".

Runs last, after build_agency_update. Idempotent.
"""
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / 'public'

HOME = {
    'en': dict(
        file=OUT / 'index.html',
        alt_old='alt="People First — WTF! Booklet cover"',
        alt_new='alt="People First — WTF! cover: five workers carrying an orange pyramid with a relaxed boss on top"',
        anchor='<p>The technology has moved on. The people questions are still with us.</p>',
        next=('<p class="coming-next"><span class="badge">COMING NEXT:</span> THE DIGITAL JOURNEYMEN – The Agents Edition. '
              'APIs in the age of AI. Same walls. New colleagues.</p>'),
    ),
    'de': dict(
        file=OUT / 'de' / 'index.html',
        alt_old='alt="People First — WTF! Booklet cover"',
        alt_new='alt="People First — WTF! Cover: fünf Arbeitende tragen eine orange Pyramide, oben sitzt entspannt der Chef"',
        anchor='<p>Die Technologie hat sich weiterentwickelt. Die Fragen zu uns Menschen sind geblieben.</p>',
        next=('<p class="coming-next"><span class="badge">ALS NÄCHSTES:</span> THE DIGITAL JOURNEYMEN – The Agents Edition. '
              'APIs im Zeitalter der AI. Dieselben Wände. Neue Kollegen.</p>'),
    ),
}

NEXT_OLD = ('<section class="booklet-next"><p class="eyebrow badge">THE NEXT CHAPTER / UPCOMING</p><h2>PEOPLE FIRST — WTF!</h2>'
            '<p>Damn good organizational advice. Currently in the making.</p><a class="text-link" href="/#booklet">Meet the new booklet →</a></section>')
NEXT_NEW = (
    '<section class="booklet-next"><p class="eyebrow badge">THE NEXT CHAPTERS / UPCOMING</p>'
    '<div class="next-books">'
    '<article><img src="/assets/people-first-cover-portrait.webp" alt="PEOPLE FIRST — WTF! cover" loading="lazy" width="800" height="1236">'
    '<div><p class="eyebrow">FIRST</p><h2>PEOPLE FIRST — WTF!</h2><p>Damn good organizational advice. For people who want their people to have a good Tuesday. Currently in the making.</p>'
    '<a class="text-link" href="/#booklet">Meet the new booklet →</a></div></article>'
    '<article><img src="/assets/agents-edition-cover.webp" alt="THE DIGITAL JOURNEYMEN – The Agents Edition cover: a human hand passing a yellow baton to a wireframe robot hand" loading="lazy" width="800" height="1236">'
    '<div><p class="eyebrow">COMING NEXT</p><h2>THE DIGITAL JOURNEYMEN – The Agents Edition</h2><p>Damn good digital advice for APIs in the age of AI. AI can only act where your organization lets it – through APIs. The agents will run into exactly the same walls.</p>'
    '<a class="text-link" href="/#agents">APIs in the age of AI →</a></div></article>'
    '</div></section>'
)

CSS = ('\n/* books-update */.coming-next{font-weight:700}.coming-next .badge{letter-spacing:1px}'
       '.next-books{display:grid;grid-template-columns:1fr 1fr;gap:50px;margin-top:20px}'
       '.next-books article{display:grid;grid-template-columns:160px 1fr;gap:28px;align-items:start}'
       '.next-books img{border:1px solid #ddd;box-shadow:8px 10px 0 #e6e2da}'
       '.next-books h2{font-size:clamp(26px,2.4vw,36px);margin-bottom:14px}.next-books .eyebrow{margin-bottom:12px}'
       '@media(max-width:900px){.next-books{grid-template-columns:1fr}}'
       '@media(max-width:620px){.next-books article{grid-template-columns:110px 1fr;gap:20px}}\n')


def build():
    for c in HOME.values():
        f = c['file']
        s = f.read_text()
        s = s.replace('src="/assets/booklet.webp"', 'src="/assets/people-first-cover.webp"')
        s = s.replace(c['alt_old'], c['alt_new'])
        if 'class="coming-next"' not in s:
            assert c['anchor'] in s, f'anchor missing in {f}'
            s = s.replace(c['anchor'], c['anchor'] + c['next'], 1)
        f.write_text(s)

    bf = OUT / 'booklets' / 'the-digital-journeymen' / 'index.html'
    s = bf.read_text()
    if 'class="next-books"' not in s:
        assert NEXT_OLD in s, 'booklet-next section missing'
        s = s.replace(NEXT_OLD, NEXT_NEW)
    bf.write_text(s)

    css = OUT / 'style.css'
    t = css.read_text()
    if '/* books-update */' not in t:
        css.write_text(t + CSS)
    print('Updated booklets: new PEOPLE FIRST cover, Agents Edition coming next.')


if __name__ == '__main__':
    build()
