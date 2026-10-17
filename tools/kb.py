#!/usr/bin/env python3
"""Offline, standard-library research ledger and citation-first search. Python 3.9+."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
STATES = {'discovered', 'metadata_reviewed', 'extracted', 'verified', 'excluded'}
AVAILABILITY = {'public_page', 'public_metadata_gated_body', 'fetch_failed', 'unknown', 'search_result_only'}

def canonical(url):
    p = urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('Expected an HTTP(S) source URL without credentials')
    host = p.hostname.lower()
    q = parse_qs(p.query)
    if host in ('youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be'):
        video = p.path.strip('/') if host == 'youtu.be' else q.get('v', [None])[0]
        if p.path.startswith(('/embed/', '/shorts/', '/live/')):
            video = p.path.split('/')[2]
        if video and re.fullmatch(r'[A-Za-z0-9_-]{11}', video):
            return 'https://www.youtube.com/watch?v=' + video
        host = 'www.youtube.com'
    q = {k: v for k, v in q.items() if not k.startswith('utm_') and k not in ('fbclid', 'gclid')}
    path = p.path or '/'
    if host == 'jeremyhaynes.com':
        path = path.rstrip('/') + '/'
    return urlunsplit(('https', host, path, urlencode(sorted(q.items()), doseq=True), ''))

def source_id(url):
    return 'src_' + hashlib.sha256(canonical(url).encode()).hexdigest()[:16]

def read_jsonl(path):
    if not Path(path).exists():
        return []
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]

def write_jsonl(path, rows):
    Path(path).write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True) + '\n' for x in rows))

def validate_source(s):
    required = {'id', 'url', 'title', 'kind', 'published_date', 'observed_date', 'availability', 'processing_state', 'confidence', 'locator', 'rights', 'provenance'}
    if required - s.keys():
        raise ValueError('Missing fields: ' + ', '.join(sorted(required - s.keys())))
    if source_id(s['url']) != s['id']:
        raise ValueError('Source ID does not match canonical URL')
    if not s['title'] or s['processing_state'] not in STATES or s['availability'] not in AVAILABILITY:
        raise ValueError('Invalid title/state/availability')
    if s['kind'] not in {'blog', 'skill', 'podcast', 'official_site', 'youtube_video', 'case_study', 'youtube_channel', 'interview', 'appearance', 'catalog', 'pdf'}:
        raise ValueError('Invalid source kind')
    if not s['provenance'] or not isinstance(s['provenance'], list) or not s['rights'] or not s['locator']:
        raise ValueError('Missing provenance, rights or locator')
    for key in ('observed_date', 'published_date'):
        if s[key] is not None:
            date.fromisoformat(s[key])
    if s['published_date'] and s['published_date'] > s['observed_date']:
        raise ValueError('Future publication date needs quarantine/review')
    if s['confidence'] not in ('high', 'medium', 'low'):
        raise ValueError('Invalid identity confidence')
    if s['availability'] in ('fetch_failed', 'unknown', 'search_result_only') and s['processing_state'] in ('extracted', 'verified'):
        raise ValueError('Cannot extract/verify unavailable content')
    return s

def ingest(path, target):
    """Fail atomically on duplicates with conflicting metadata; never silently overwrite."""
    old = read_jsonl(target)
    by_id = {s['id']: s for s in old}
    for s in read_jsonl(path):
        validate_source(s)
        if s['id'] in by_id and s != by_id[s['id']]:
            raise ValueError('Conflicting revision; review and version explicitly: ' + s['id'])
        by_id[s['id']] = s
    write_jsonl(target, sorted(by_id.values(), key=lambda x: x['id']))

def validate(root=ROOT):
    sources = read_jsonl(root / 'data/sources.jsonl')
    claims = read_jsonl(root / 'data/claims.jsonl')
    ids = set()
    for s in sources:
        validate_source(s)
        if s['id'] in ids:
            raise ValueError('Duplicate source ID')
        ids.add(s['id'])
    cids = set()
    for c in claims:
        required = {'id', 'source_id', 'paraphrase', 'locator', 'start_seconds', 'end_seconds', 'topics', 'claim_type', 'attribution_confidence', 'empirical_confidence', 'scope', 'review_state', 'observed_date'}
        if required - c.keys():
            raise ValueError('Missing claim fields')
        if c['id'] in cids or c['source_id'] not in ids or not c['locator'] or not c['paraphrase']:
            raise ValueError('Invalid claim identity/evidence')
        cids.add(c['id'])
        if (c['start_seconds'] is None) != (c['end_seconds'] is None) or (c['start_seconds'] is not None and (c['start_seconds'] < 0 or c['end_seconds'] <= c['start_seconds'])):
            raise ValueError('Invalid time range')
        if c['review_state'] not in ('reviewed_paraphrase', 'needs_review'):
            raise ValueError('Invalid claim state')
        if c['claim_type'] not in ('attributed_recommendation', 'self_reported_result', 'researcher_inference', 'empirical_finding'):
            raise ValueError('Invalid claim type')
        if c['attribution_confidence'] not in ('high', 'medium', 'low') or c['empirical_confidence'] not in ('unverified', 'low', 'medium', 'high'):
            raise ValueError('Invalid claim confidence')
        date.fromisoformat(c['observed_date'])
    for f in json.loads((root / 'data/frameworks.json').read_text()):
        if not set(f['claim_ids']) <= cids:
            raise ValueError('Framework cites missing claims')
    for chapter in read_jsonl(root / 'data/chapters.jsonl'):
        if chapter['source_id'] not in ids or chapter['start_seconds'] < 0 or chapter['end_seconds'] <= chapter['start_seconds']:
            raise ValueError('Invalid publisher chapter')
    relations_path = root / 'data/video-relations.json'
    if relations_path.exists():
        for relation in json.loads(relations_path.read_text()):
            if relation['video_source_id'] not in ids or relation['context_source_id'] not in ids:
                raise ValueError('Video relation cites missing source')
    return {'sources': len(sources), 'claims': len(claims)}

def connect(db):
    con = sqlite3.connect(str(db))
    con.execute('CREATE VIRTUAL TABLE IF NOT EXISTS evidence USING fts5(id UNINDEXED, source_id UNINDEXED, text, locator UNINDEXED, url UNINDEXED, evidence_type UNINDEXED)')
    return con

def build(db, root=ROOT):
    con = connect(db)
    con.execute('DELETE FROM evidence')
    sources = {s['id']: s for s in read_jsonl(root / 'data/sources.jsonl')}
    for s in sources.values():
        if s['processing_state'] == 'excluded':
            continue
        con.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?)', (s['id'], s['id'], s['title'], s['locator'], s['url'], 'metadata_only'))
    for c in read_jsonl(root / 'data/claims.jsonl'):
        s = sources[c['source_id']]
        if c['review_state'] != 'reviewed_paraphrase' or s['processing_state'] == 'excluded':
            continue
        con.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?)', (c['id'], c['source_id'], c['paraphrase'] + ' ' + ' '.join(c['topics']), c['locator'], s['url'], 'reviewed_paraphrase'))
    con.commit()
    con.close()

def search(query, db, limit=8, claims_only=False):
    tokens = re.findall(r'\w+', query.lower())
    if not tokens:
        return []
    # Quote tokens: a user query cannot inject FTS operators or SQL.
    match = ' OR '.join('"' + t + '"' for t in tokens)
    con = connect(db)
    rows = con.execute('SELECT id,source_id,text,locator,url,evidence_type,bm25(evidence) AS score FROM evidence WHERE evidence MATCH ? ' + ("AND evidence_type='reviewed_paraphrase' " if claims_only else '') + 'ORDER BY score,id LIMIT ?', (match, limit)).fetchall()
    con.close()
    result = [dict(zip(('id', 'source_id', 'text', 'locator', 'url', 'evidence_type', 'score'), r)) for r in rows]
    # Context links are navigation, not a claim that an article is an exact transcript.
    relations_path = ROOT / 'data/video-relations.json'
    if relations_path.exists():
        relations = json.loads(relations_path.read_text())
        sources = {s['id']: s for s in read_jsonl(ROOT / 'data/sources.jsonl')}
        for hit in result:
            hit['related_video_urls'] = sorted({sources[x['video_source_id']]['url'] for x in relations if x['context_source_id'] == hit['source_id']})
    return result

def evaluate(db, root=ROOT):
    cases = read_jsonl(root / 'data/evaluation.jsonl')
    results = []
    for case in cases:
        found = search(case['query'], db, 5, claims_only=True)
        actual = {x['id'] for x in found}
        passed = bool(actual & set(case['expected_claim_ids'])) if case['expected_claim_ids'] else not found
        results.append({'id': case['id'], 'passed': passed, 'retrieved': sorted(actual), 'expected_any': case['expected_claim_ids']})
    return {'scope': 'Small offline retrieval smoke benchmark; not answer faithfulness or production readiness', 'passed': sum(x['passed'] for x in results), 'total': len(results), 'results': results}

def coverage(root=ROOT):
    sources = read_jsonl(root / 'data/sources.jsonl')
    data = {'as_of': '2026-10-16', 'version': (root / 'VERSION').read_text().strip(), 'sources': len(sources), 'claims': len(read_jsonl(root / 'data/claims.jsonl')), 'by_kind': dict(collections.Counter(s['kind'] for s in sources)), 'by_state': dict(collections.Counter(s['processing_state'] for s in sources)), 'by_availability': dict(collections.Counter(s['availability'] for s in sources)), 'full_coverage_verified': False}
    snapshot = root / 'data/channel-snapshot-audit.json'
    if snapshot.exists():
        data['official_videos_tab_snapshot'] = json.loads(snapshot.read_text())
    (root / 'reports/coverage.json').write_text(json.dumps(data, indent=2) + '\n')
    return data

def export_csv(root=ROOT):
    rows = read_jsonl(root / 'data/sources.jsonl')
    keys = sorted({key for row in rows for key in row})
    with (root / 'reports/source-inventory.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()})

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['validate', 'ingest', 'build', 'search', 'evaluate', 'coverage', 'export'])
    p.add_argument('value', nargs='?')
    p.add_argument('--db', default=str(ROOT / 'local-index.sqlite'))
    p.add_argument('--claims-only', action='store_true')
    a = p.parse_args()
    if a.command == 'validate': result = validate()
    elif a.command == 'ingest':
        if not a.value: p.error('ingest requires reviewed JSONL file')
        ingest(a.value, ROOT / 'data/sources.jsonl'); result = validate()
    elif a.command == 'build': build(a.db); result = {'index': a.db}
    elif a.command == 'search': result = search(a.value or '', a.db, claims_only=a.claims_only)
    elif a.command == 'evaluate': result = evaluate(a.db)
    elif a.command == 'coverage': result = coverage()
    else: export_csv(); result = {'export': 'reports/source-inventory.csv'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if a.command == 'evaluate' and result['passed'] != result['total']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
