"""Build the bilingual post "Poor Markwayne" from preserved text sources."""
from build_apis_sexy import build_post

EN = '/writing/poor-markwayne/'
DE = '/de/artikel/armer-markwayne/'
IMAGE = 'poor-markwayne.jpg'
PUBLISHED = '2026-11-20'

COPY = {
    'en': dict(
        description='On the difficulty of explaining the world of IT.',
        alt='AI-generated illustration: in a TV studio, a man in glasses whispers into the ear of a puzzled politician. In thought bubbles, technicians work in a server room while an AI robot kicks cartoon servers wearing boxing gloves.',
        caption='AI-generated illustration',
        eyebrow='POST',
        back='All posts &amp; articles',
        date=f'Published on this site: <time datetime="{PUBLISHED}">20 November 2026</time>',
        meta='Post',
        read='Read the post →',
    ),
    'de': dict(
        description='Über die Schwierigkeit, die Welt der IT zu erklären.',
        alt='KI-generierte Illustration: In einem TV-Studio flüstert ein Mann mit Brille einem ratlosen Politiker etwas ins Ohr. In Gedankenblasen arbeiten Techniker im Serverraum, während ein AI-Roboter Comic-Server mit Boxhandschuhen wegkickt.',
        caption='KI-generierte Illustration',
        eyebrow='POST',
        back='Alle Posts &amp; Artikel',
        date=f'Auf dieser Website seit: <time datetime="{PUBLISHED}">20. November 2026</time>',
        meta='Post',
        read='Auf Deutsch lesen →',
    ),
}


def build():
    build_post(EN, DE, IMAGE, 'markwayne', COPY, deck=True, signed=True)
    print('Generated Poor Markwayne EN/DE.')


if __name__ == '__main__':
    build()
