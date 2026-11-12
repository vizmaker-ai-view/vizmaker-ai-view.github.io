# Generuje library/updates.ics (kalendarz subskrypcyjny "nowe projekty w bibliotece").
# Edytuj RELEASES i uruchom:  python3 library/build_ics.py
import datetime as dt
URL = 'https://vizmaker-ai-view.github.io/library/'
# (data, godzina UTC, tytuł, opis) - 17:00 UTC = 18:00 Warszawa (zima)
start = dt.date(2026, 11, 16)  # poniedziałek
RELEASES = [(start + dt.timedelta(weeks=i), 17, 'New AI project in the VizMaker Library',
             'A new project with a video tutorial and prompts is live. Open it: ' + URL + '?p=latest') for i in range(12)]
# Konkretne premiery projektów: (data, godzina UTC, tytuł, opis) - dopisuj tu nowe projekty
RELEASES = [(dt.date(2026, 11, 12), 17, 'New project: Turn any 3D scene into a realistic Live Preview',
             'Open the project: ' + URL + '?p=default')] + RELEASES
RELEASES = [(dt.date(2026, 11, 12), 15, 'New project: Stop searching 3D Warehouse - make your own models with AI',
             'Generate your own 3D model with AI in VizMaker. Open the project: ' + URL + '?p=yt8')] + RELEASES
# TEST (12.11.2026): stare projekty co godzinę 17:00-21:00 Warszawa - usunąć po teście
OLD = [('yt1', 'Place your 3D model in Google Earth and turn it into real context visuals'),
       ('yt2', 'Realistic AI animation from a viewport'),
       ('yt3', 'The fastest way to show clients your interior ideas'),
       ('yt4', 'Create your AI avatar and full ad campaign for free'),
       ('live', 'Live Preview: 3D scene to realistic render')]
RELEASES = [(dt.date(2026, 11, 12), 16 + i, 'New project: ' + t, 'Open the project: ' + URL + '?p=' + k) for i, (k, t) in enumerate(OLD)] + RELEASES
def z(d, h, m=0): return dt.datetime(d.year, d.month, d.day, h, m).strftime('%Y%m%dT%H%M%SZ')
L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//VizMaker//AI Project Library//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
     'X-WR-CALNAME:VizMaker AI Project Library', 'X-WR-CALDESC:New AI projects for architects and interior designers - every week',
     'REFRESH-INTERVAL;VALUE=DURATION:PT1H', 'X-PUBLISHED-TTL:PT1H']
now = dt.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
for d, h, t, desc in RELEASES:
    L += ['BEGIN:VEVENT', 'UID:library-update-%s-%02d@vizmaker.com' % (d.strftime('%Y%m%d'), h), 'DTSTAMP:' + now,
          'DTSTART:' + z(d, h), 'DTEND:' + z(d, h, 30), 'SUMMARY:\U0001F195 ' + t, 'DESCRIPTION:' + desc, 'URL:' + URL, 'LOCATION:' + URL,
          'BEGIN:VALARM', 'TRIGGER:PT0M', 'ACTION:DISPLAY', 'DESCRIPTION:' + t, 'END:VALARM', 'END:VEVENT']
L.append('END:VCALENDAR')
def fold(line):  # RFC 5545: linie max 75 bajtów, kontynuacja od spacji
    b, out, cur = line.encode('utf-8'), [], b''
    for ch in line:
        c = ch.encode('utf-8')
        if len(cur) + len(c) > (75 if not out else 74): out.append(cur); cur = b''
        cur += c
    out.append(cur)
    return '\r\n '.join(x.decode('utf-8') for x in out)
open(__file__.replace('build_ics.py', 'updates.ics'), 'w', newline='').write('\r\n'.join(fold(x) for x in L) + '\r\n')
print('ok', len(RELEASES), 'events')

# ---- RSS dla Mailchimp (RSS-to-email): nowy projekt = nowy <item> na górze ----
# (klucz projektu, data publikacji, tytuł, opis) - najnowszy pierwszy; dopisuj tu przy każdym nowym projekcie
FEED = [('default', dt.datetime(2026, 11, 12, 16, 35), 'Turn any 3D scene into a realistic Live Preview',
         'The VizMaker plugin turns any 3D scene into a photorealistic live preview. Open the guide project in 3D, watch the tutorial and copy the prompt.'),
        ('yt8', dt.datetime(2026, 11, 12, 15, 0), 'Stop searching 3D Warehouse: make your own models with AI',
         'Can\'t find the right model? Generate your own 3D model with AI in VizMaker. Open the project in 3D and follow the tutorial.'),
        ('live', dt.datetime(2026, 11, 5, 15, 0), 'Live Preview: 3D scene to realistic render', 'Turn any 3D scene into a realistic live preview.'),
        ('yt4', dt.datetime(2026, 11, 4, 15, 0), 'Create your AI avatar and full ad campaign for free', 'AI avatar and a full ad campaign in VizMaker.'),
        ('yt3', dt.datetime(2026, 11, 3, 15, 0), 'The fastest way to show clients your interior ideas', 'Show interior ideas to clients in minutes.'),
        ('yt2', dt.datetime(2026, 11, 2, 15, 0), 'Realistic AI animation from a viewport', 'Realistic AI animation straight from your viewport.'),
        ('yt1', dt.datetime(2026, 11, 1, 15, 0), 'Place your 3D model in Google Earth and turn it into real context visuals', 'Put your model in Google Earth and render real context.')]
from email.utils import format_datetime
from xml.sax.saxutils import escape
items = ''.join('<item><title>%s</title><link>%s?p=%s&amp;utm_source=mailchimp&amp;utm_medium=email&amp;utm_campaign=library_rss</link>'
                '<guid isPermaLink="false">vm-library-%s</guid><pubDate>%s</pubDate><description>%s</description></item>\n'
                % (escape(t), URL, k, k, format_datetime(d.replace(tzinfo=dt.timezone.utc)), escape(desc)) for k, d, t, desc in FEED)
rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>VizMaker AI Project Library</title>'
       '<link>%s</link><description>New AI projects for architects and interior designers - every week.</description>\n%s</channel></rss>\n' % (URL, items))
open(__file__.replace('build_ics.py', 'feed.xml'), 'w').write(rss)
print('feed ok', len(FEED), 'items')
