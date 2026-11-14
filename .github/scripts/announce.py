# Ogłasza nowe projekty z library/feed.xml na Discordzie (i później Telegram itd.).
# Nowy projekt = nowy <guid> w feed.xml, którego nie było w poprzednim commicie.
# Uruchamiane przez .github/workflows/announce-new-project.yml - nic nie trzeba robić ręcznie.
import json, os, re, subprocess, sys, urllib.request, xml.etree.ElementTree as ET

FEED = 'library/feed.xml'
LIB = 'https://vizmaker-ai-view.github.io/library/'

def items(xml):
    if not xml.strip(): return []
    root = ET.fromstring(xml)
    out = []
    for it in root.iter('item'):
        guid = it.findtext('guid', '')
        out.append({'guid': guid, 'key': guid.replace('vm-library-', ''),
                    'title': it.findtext('title', ''), 'desc': it.findtext('description', '')})
    return out

def prev_feed(before):
    if not before or set(before) == {'0'}: return ''
    try: return subprocess.run(['git', 'show', f'{before}:{FEED}'], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError: return ''

def thumb(key):
    # miniaturka z filmu YouTube projektu (pole yt w LESSONS w library/index.html)
    html = open('library/index.html', encoding='utf-8').read()
    m = re.search(r"key:\s*'%s'[^}]*?\byt:\s*'([\w-]+)'" % re.escape(key), html)
    return f'https://i.ytimg.com/vi/{m.group(1)}/hqdefault.jpg' if m else None

def link(key, src):
    return f'{LIB}?p={key}&utm_source={src}&utm_medium=social&utm_campaign=library_new_project'

def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method='POST',
                                 headers={'Content-Type': 'application/json', 'User-Agent': 'VizMaker-Announcer'})
    with urllib.request.urlopen(req) as r: print('posted', r.status)

def discord(p):
    hook = os.environ.get('DISCORD_WEBHOOK')
    if not hook: print('DISCORD_WEBHOOK not set - skip'); return
    embed = {'title': p['title'], 'url': link(p['key'], 'discord'), 'description': p['desc'] +
             f"\n\n👉 **[Open the project for free]({link(p['key'], 'discord')})**", 'color': 0x2EE6C9,
             'footer': {'text': 'VizMaker AI Project Library · new free project'}}
    if thumb(p['key']): embed['image'] = {'url': thumb(p['key'])}
    post(hook, {'username': 'VizMaker', 'avatar_url': 'https://www.vizmaker.com/vizmaker-logo-line-white.png',
                'content': os.environ.get('DISCORD_MENTION', '') + ' 🎁 **New FREE project in the VizMaker Library!**',
                'embeds': [embed]})

if __name__ == '__main__':
    now = items(open(FEED, encoding='utf-8').read())
    if os.environ.get('TEST') == 'true':
        new = now[:1]                                   # test ręczny: ogłoś najnowszy projekt
    else:
        old = {i['guid'] for i in items(prev_feed(os.environ.get('BEFORE', '')))}
        new = [i for i in now if i['guid'] not in old]
        if not old and len(new) > 1: new = new[:1]      # zabezpieczenie: nie spamuj całym feedem
    print('new projects:', [i['key'] for i in new])
    for p in reversed(new): discord(p)                  # najstarszy z nowych pierwszy
