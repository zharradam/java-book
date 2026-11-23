# Collect site statistics into stats.json for theshipjava.uk/stats/.
# Run hourly by .github/workflows/stats.yml; the JSON lives on the "stats" branch.
#
#   python build/collect_stats.py <previous stats.json or ""> <output stats.json>
#
# Downloads: GitHub resets an asset's download_count to 0 whenever the file is
# replaced (every book rebuild), so totals are carried forward here: when a
# count drops, the last value seen is banked. Downloads between the last poll
# and a replacement are lost, which hourly polling keeps small.
#
# Visits: GoatCounter API (env GOATCOUNTER_TOKEN). Skipped if no token is set.
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timedelta, timezone

REPO = 'zharradam/java-book'
GC = 'https://theshipjava.goatcounter.com/api/v0'
NAMES = {'the-java.pdf': 'PDF', 'the-java.epub': 'EPUB', 'the-java.m4b': 'Audiobook'}


def get(url, token=None):
    req = urllib.request.Request(url, headers={'User-Agent': 'theshipjava-stats', 'Accept': 'application/json'})
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def downloads(prev):
    """Running totals per file, carried across asset replacements."""
    old = {d['file']: d for d in prev.get('downloads', [])}
    rel = get(f'https://api.github.com/repos/{REPO}/releases/tags/latest', os.environ.get('GITHUB_TOKEN'))
    out = []
    for a in rel['assets']:
        if a['name'] not in NAMES:
            continue
        o = old.get(a['name'], {'banked': 0, 'current': 0})
        banked = o['banked'] + (o['current'] if a['download_count'] < o['current'] else 0)
        out.append({'file': a['name'], 'label': NAMES[a['name']], 'banked': banked,
                    'current': a['download_count'], 'total': banked + a['download_count']})
    return sorted(out, key=lambda d: list(NAMES).index(d['file']))


def visits(token):
    end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    start = end - timedelta(days=30)
    q = lambda **k: urllib.parse.urlencode({'start': start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                            'end': end.strftime('%Y-%m-%dT%H:%M:%SZ'), **k})
    def call(path, empty):
        try:
            return get(f'{GC}/{path}', token)
        except Exception as e:
            print(f'GoatCounter {path.split("?")[0]}: {e}', file=sys.stderr)
            if path.startswith('stats/total'):
                raise
            return empty
    total = call(f'stats/total?{q()}', {})
    hits = call(f'stats/hits?{q(limit=100)}', {}).get('hits', [])
    refs = call(f'stats/toprefs?{q(limit=10)}', {}).get('stats', [])
    alltime = call('stats/total?' + urllib.parse.urlencode({'start': '2026-11-01T00:00:00Z',
                                                          'end': end.strftime('%Y-%m-%dT%H:%M:%SZ')}), {})
    pages = [{'path': h['path'], 'title': h.get('title') or '', 'count': h.get('count', 0)}
             for h in hits if not h.get('event')]
    clicks = [{'name': h['path'], 'count': h.get('count', 0)} for h in hits if h.get('event')]
    return {
        'total_30d': total.get('total', 0),
        'total_all': alltime.get('total', 0),
        'daily': [{'day': s['day'], 'count': s.get('daily', 0)} for s in total.get('stats', [])],
        'pages': sorted(pages, key=lambda p: -p['count']),
        'clicks': clicks,
        'referrers': [{'name': r.get('name') or '(direct)', 'count': r.get('count', 0)} for r in refs],
    }


def main(prev_path, out_path):
    prev = {}
    if prev_path and os.path.exists(prev_path):
        with open(prev_path, encoding='utf-8') as f:
            prev = json.load(f)
    stats = {'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'downloads': downloads(prev)}
    token = os.environ.get('GOATCOUNTER_TOKEN')
    if token:
        try:
            stats['visits'] = visits(token)
        except Exception as e:   # keep the last good visit figures rather than blanking the page
            print('GoatCounter failed:', e, file=sys.stderr)
            if 'visits' in prev:
                stats['visits'] = prev['visits']
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=1)
    print(json.dumps(stats['downloads']))


def _selftest():
    global get
    real, counts = get, iter([5, 2, 4])
    get = lambda *a, **k: {'assets': [{'name': 'the-java.pdf', 'download_count': next(counts)}]}
    p = {}
    for want in (5, 7, 9):   # 5, then replaced (5 banked) +2, then +4 -> 9
        p = {'downloads': downloads(p)}
        assert p['downloads'][0]['total'] == want, p
    get = real


if __name__ == '__main__':
    _selftest()
    main(sys.argv[1], sys.argv[2])
