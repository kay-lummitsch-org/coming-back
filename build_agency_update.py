"""Agency for people and agents: Digital Journeyman kicker, APIs in the age of AI, two-question invitation.

Runs after build_home_update so it sees the final homepages. Idempotent.
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent
OUT = ROOT / 'public'

COPY = {
    'en': dict(
        file=OUT / 'index.html',
        kicker='THE DIGITAL JOURNEYMAN – STILL ON THE ROAD',
        hero_tag='For your people.<br>And your agents.',
        bang=None,
        agents=(
            '<section class="approach agents" id="agents"><div><p class="eyebrow">PEOPLE AND MACHINES</p>'
            '<h2>Your people<br>aren’t the only ones<br>who get stuck.</h2>'
            '<div class="agents-intro"><p>AI is moving into your organization. But it can only act where your organization lets it – through APIs.</p>'
            '<p>Badly designed, unmanaged or long-forgotten interfaces are the same old friction. Only now it’s built into code.</p></div></div>'
            '<div class="approach-list"><p class="agents-lead">This is where I come in. Three disciplines I have loved for a long time – and that decide what your agents can do:</p>'
            '<article><span>01</span><div><h3>API design.</h3><p>APIs your people and your agents actually understand. Every resource, every name, every error message designed with care.</p></div></article>'
            '<article><span>02</span><div><h3>Learn how to leverage your APIs.</h3><p>API product design: who your APIs are for, what business they enable, and where they belong in your landscape.</p></div></article>'
            '<article><span>03</span><div><h3>Rock-solid API management advice.</h3><p>Secure, govern and keep track of what you expose – to whom, where and for how long. Before the bots do it for you.</p></div></article>'
            '<p class="agents-close">In the age of AI, none of this is a technical detail anymore. It decides what your machines can do – and whether your people still understand what’s going on.</p>'
            '<p class="agents-close strong">That’s what AI readiness really means: fewer barriers – for people and for machines.</p>'
            '<div class="agents-actions"><a class="button" href="/#contact">Let’s talk APIs <span>→</span></a><a class="text-link" href="/writing/apis-no-longer-need-to-be-sexy/">APIs no longer need to be sexy. Or do they? →</a></div></div></section>'
        ),
        role_old='API program leader.', role_new='Ambassador for API adoption in enterprises.',
        journeyman='Some still know me as the Digital Journeyman. I still am – the roads just got longer.',
        contact=(
            '<p class="eyebrow">TWO QUESTIONS</p><h2>What is getting<br>in your people’s way?</h2>'
            '<div><p class="strong">And what is getting in your agents’ way?</p>'
            '<p>If you want to find out – and you’re ready to act on what you find – let’s talk.</p>'
        ),
    ),
    'de': dict(
        file=OUT / 'de' / 'index.html',
        kicker='THE DIGITAL JOURNEYMAN – IMMER NOCH UNTERWEGS',
        hero_tag='Für Menschen.<br>Und für Agents.',
        bang=('MEHR<br>SPIELRAUM.', 'MEHR<br>HANDLUNGS&shy;SPIELRAUM.'),
        agents=(
            '<section class="approach agents" id="agents"><div><p class="eyebrow">MENSCHEN UND MASCHINEN</p>'
            '<h2>Nicht nur<br>Menschen<br>bleiben hängen.</h2>'
            '<div class="agents-intro"><p>AI zieht in Organisationen ein. Aber sie kann nur dort handeln, wo die Organisation sie lässt – über APIs.</p>'
            '<p>Schlecht gestaltete, unverwaltete oder längst vergessene Schnittstellen sind dieselbe alte Reibung. Nur steckt sie jetzt im Code.</p></div></div>'
            '<div class="approach-list"><p class="agents-lead">Hier komme ich ins Spiel. Mit drei Disziplinen, die ich seit Langem liebe – und die darüber entscheiden, was Agents tun können:</p>'
            '<article><span>01</span><div><h3>API-Design.</h3><p>APIs, die Menschen und Agents wirklich verstehen. Jede Ressource, jeder Name, jede Fehlermeldung mit Sorgfalt gestaltet.</p></div></article>'
            '<article><span>02</span><div><h3>APIs, die Geschäft machen.</h3><p>API-Produktdesign: für wen deine APIs da sind, welches Geschäft sie ermöglichen und wo sie in deine Landschaft gehören.</p></div></article>'
            '<article><span>03</span><div><h3>API-Management, das hält.</h3><p>Absichern, steuern und den Überblick behalten, was du wem wohin und wie lange exponierst. Bevor die Bots es für dich tun.</p></div></article>'
            '<p class="agents-close">Im Zeitalter der AI ist das alles kein technisches Detail mehr. Es entscheidet, was Maschinen tun können – und ob Menschen noch verstehen, was passiert.</p>'
            '<p class="agents-close strong">Das bedeutet AI-Readiness wirklich: weniger Barrieren – für Menschen und für Maschinen.</p>'
            '<div class="agents-actions"><a class="button" href="/de/#contact">Reden wir über APIs <span>→</span></a><a class="text-link" href="/de/artikel/apis-muessen-nicht-mehr-sexy-sein/">APIs müssen nicht mehr sexy sein. Oder doch? →</a></div></div></section>'
        ),
        role_old='API-Programmleiter.', role_new='Ambassador für API-Adoption in Unternehmen.',
        journeyman='Manche kennen mich noch als Digital Journeyman. Der bin ich geblieben – nur die Wege sind länger geworden.',
        contact=(
            '<p class="eyebrow">ZWEI FRAGEN</p><h2>Was steht den Menschen<br>in deiner Organisation<br>im Weg?</h2>'
            '<div><p class="strong">Und was den Agents?</p>'
            '<p>Wenn du es herausfinden willst – und bereit bist, danach zu handeln –, dann sollten wir reden.</p>'
        ),
    ),
}


def update(c):
    source = c['file'].read_text()

    # 1. Digital Journeyman kicker above the hero headline; no active mandate search in the hero.
    source = re.sub(r'<p class="eyebrow journeyman">.*?</p>', '', source, flags=re.S)
    source = source.replace('<div class="hero-copy"><h1>', f'<div class="hero-copy"><p class="eyebrow journeyman">{c["kicker"]}</p><h1>', 1)
    source = re.sub(r'<p class="mandate-invite">.*?</p>', '', source, flags=re.S)

    # 2. Agency for people and agents.
    source = re.sub(r'(<div class="hero-art">.*?</div>)<p>.*?</p>', lambda m: m[1] + f'<p>{c["hero_tag"]}</p>', source, count=1, flags=re.S)
    if c['bang']:
        source = source.replace(*c['bang'])

    # 3. APIs in the age of AI, right after "How we run the business".
    source = re.sub(r'<section class="approach agents".*?</section>', '', source, flags=re.S)
    source = re.sub(r'(<section class="approach">.*?</section>)', lambda m: m[1] + c['agents'], source, count=1, flags=re.S)

    # 4. Context: the Digital Journeyman is back.
    source = source.replace(c['role_old'], c['role_new'])
    source = re.sub(r'<p class="journeyman-note">.*?</p>', '', source, flags=re.S)
    source = re.sub(r'(<div class="about-copy">.*?</h2>)', lambda m: m[1] + f'<p class="journeyman-note">{c["journeyman"]}</p>', source, count=1, flags=re.S)

    # 5. Two questions instead of an active mandate search.
    source = re.sub(r'(<section class="contact" id="contact">).*?(<div class="contact-actions">)',
                    lambda m: m[1] + c['contact'] + m[2], source, count=1, flags=re.S)

    c['file'].write_text(source)


def build():
    for c in COPY.values():
        update(c)


if __name__ == '__main__':
    build()
