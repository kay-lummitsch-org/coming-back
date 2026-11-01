"""Approved November 2026 invitation and bilingual enquiry pages."""
from pathlib import Path
import re
from build_german import alternates, switch, de_nav
ROOT=Path(__file__).parent;OUT=ROOT/'public'

def form(de):
 t=({ 'name':'Name','email':'E-Mail','topic':'Was beschäftigt Dich gerade?','hint':'Ein Stichwort reicht. Bitte keine vertraulichen Einzelheiten oder Daten anderer Personen eingeben.','date':'Wunschdatum im November','time':'Wunschzeit','weekend':'Am Wochenende nach persönlicher Absprache','platform':'Wie möchtest Du sprechen?','meet':'Google Meet','phone':'Telefon','other':'Andere Plattform auf Anfrage','note':'Weitere Terminwünsche / Plattformwunsch (optional)','consent':'Ich möchte zur Terminabstimmung kontaktiert werden. Meine Angaben werden dafür bei Cloudflare gespeichert und Kay per E-Mail zugestellt.','privacy':'Datenschutz','submit':'Vertrauliche Anfrage senden','success':'Danke! Ich melde mich bei Dir, um einen Termin zu vereinbaren.','explain':'Das ist eine Terminanfrage, noch keine Buchungsbestätigung. Nach persönlicher Bestätigung erhältst Du die Kalendereinladung mit Meet-Link oder wir stimmen Telefon bzw. eine andere Plattform ab.','nojs':'Für das Formular bitte JavaScript aktivieren oder eine E-Mail an kay@kaylummitsch.com schreiben.','closed':'Die November-Aktion ist beendet. Du erreichst mich weiterhin unter kay@kaylummitsch.com.'} if de else {
 'name':'Name','email':'Email','topic':'What is on your mind?','hint':'A short topic is enough. Please do not include confidential details or other people’s personal data.','date':'Preferred date in November','time':'Preferred time','weekend':'Weekends by personal arrangement','platform':'How would you like to talk?','meet':'Google Meet','phone':'Phone','other':'Other platform on request','note':'Other preferred times / platform request (optional)','consent':'Please contact me to arrange this conversation. My details will be stored with Cloudflare for this purpose and emailed to Kay.','privacy':'Privacy','submit':'Send confidential enquiry','success':'Thank you! I’ll get in touch to arrange a time.','explain':'This is a meeting request, not a confirmed booking. Once we agree on a time, you’ll receive a calendar invitation with a Meet link, or we’ll arrange a phone call or another platform.','nojs':'Please enable JavaScript for the form or email kay@kaylummitsch.com.','closed':'The November invitation has ended. You can still reach me at kay@kaylummitsch.com.'})
 privacy='/de/datenschutz/' if de else '/privacy/'
 return f'''<p>{t['explain']}</p><p><strong>{'Mo–Fr' if de else 'Mon–Fri'}: 18:00–18:30 · 18:30–19:00 · 19:00–19:30 CET (Europe/Zurich).</strong><br>{t['weekend']}.</p><p class="november-closed" hidden>{t['closed']}</p><form id="november-form" data-language="{'de' if de else 'en'}">
 <label>{t['name']}<input name="name" autocomplete="name" maxlength="100" required></label>
 <label>{t['email']}<input name="email" type="email" autocomplete="email" maxlength="254" required></label>
 <label>{t['topic']}<textarea name="topic" maxlength="1000" required aria-describedby="topic-hint"></textarea></label><p id="topic-hint" class="november-hint">{t['hint']}</p>
 <label>{t['date']}<input name="preferredDate" type="date" min="2026-11-01" max="2026-11-30" required></label>
 <label>{t['time']}<select name="slot" required><option value="">—</option><option value="18:00">18:00–18:30 CET</option><option value="18:30">18:30–19:00 CET</option><option value="19:00">19:00–19:30 CET</option><option value="arrange">{t['weekend']}</option></select></label>
 <label>{t['platform']}<select name="platform"><option value="meet">{t['meet']}</option><option value="phone">{t['phone']}</option><option value="other">{t['other']}</option></select></label>
 <label>{t['note']}<textarea name="note" maxlength="500"></textarea></label>
 <div class="november-honeypot" aria-hidden="true"><label>Company<input name="company" tabindex="-1" autocomplete="off"></label></div>
 <label class="november-consent"><input name="consent" type="checkbox" required><span>{t['consent']} <a href="{privacy}">{t['privacy']}</a>.</span></label>
 <p id="november-error" role="alert" tabindex="-1" hidden></p><button type="submit" class="november-cta">{t['submit']}</button>
 </form><div id="november-success" tabindex="-1" role="status" hidden><h2>{t['success']}</h2><p>{t['explain']}</p></div><noscript><p>{t['nojs']}</p></noscript>'''

def build():
 template=(OUT/'writing/turning-sixty/index.html').read_text()
 for de,route in [(False,'/november/'),(True,'/de/november/')]:
  title='Was steht Deinen Leuten im Weg?' if de else 'What is getting in your people’s way?'
  deck=('30 Minuten. Kostenlos und unverbindlich. Und was wir besprechen, bleibt unter uns.' if de else '30 minutes. Free. No obligation. And what we discuss stays between us.')
  promise=('Keine Aufzeichnung. Keine automatische Transkription. Keine Newsletter-Anmeldung.' if de else 'No recording. No automatic transcription. No newsletter signup.')
  main=f'<main id="main" class="reading november-page"><p class="eyebrow">NOVEMBER 2026</p><h1>{title}</h1><p class="deck">{deck}</p><p>{promise}</p>'+form(de)+'</main>'
  s=re.sub(r'<main\b.*?</main>',lambda m:main,template,count=1,flags=re.S)
  s=re.sub(r'<title>.*?</title>',f'<title>{title} | Kay Lummitsch</title>',s,count=1)
  s=re.sub(r'<meta (?:name="(?:description|twitter:[^"]+)"|property="(?:og:[^"]+|article:[^"]+)")[^>]*>','',s)
  s=re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>','',s)
  s=re.sub(r'<div class="language-switch".*?</div>',switch('/november/','/de/november/','de' if de else 'en'),s,count=1)
  s=s.replace('<html lang="en">',f'<html lang="{"de" if de else "en"}">')
  if de:
   s=re.sub(r'<a class="skip".*?</header>',de_nav('/november/','/de/november/'),s,count=1,flags=re.S)
   s=s.replace('Find me on LinkedIn ↗','Auf LinkedIn verbinden ↗').replace('Made with curiosity. /kay','Mit Neugier gemacht. /kay')
  s=s.replace('</head>',f'<meta name="description" content="{deck}"><link rel="canonical" href="https://kaylummitsch.com{route}">'+alternates('/november/','/de/november/')+'</head>',1)
  p=OUT/route.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 for p in OUT.rglob('*.html'):
  s=p.read_text()
  if '/november.js' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/november.css"><script src="/november.js" defer></script></head>',1)
  p.write_text(s)
