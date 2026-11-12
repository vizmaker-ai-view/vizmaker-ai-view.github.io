# Generuje library/updates.ics (kalendarz subskrypcyjny "nowe projekty w bibliotece").
# Edytuj RELEASES i uruchom:  python3 library/build_ics.py
import datetime as dt
URL = 'https://vizmaker-ai-view.github.io/library/'
# (data, godzina UTC, tytuł, opis) - 17:00 UTC = 18:00 Warszawa (zima)
start = dt.date(2026, 11, 16)  # poniedziałek
RELEASES = [(start + dt.timedelta(weeks=i), 17, 'New AI project in the VizMaker Library',
             'A new project with a video tutorial and prompts is live. Open it: ' + URL + '?p=latest') for i in range(12)]
# Konkretne premiery projektów: (data, godzina UTC, tytuł, opis) - dopisuj tu nowe projekty
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
