#!/usr/bin/env python3
"""One-command setup and citation-first queries for agents; no network or API keys."""
import argparse
import json
from kb import ROOT, build, read_jsonl, search, validate

DB = ROOT / 'local-index.sqlite'

def setup():
    counts = validate()
    build(DB)
    smoke = search('confirmation trust urgency', DB, claims_only=True)
    if not smoke or not all(x.get('url') and x.get('locator') for x in smoke):
        raise RuntimeError('Citation smoke query failed')
    return {'status': 'ready', 'version': (ROOT/'VERSION').read_text().strip(), **counts, 'sample_evidence': smoke[0], 'limits': 'Reviewed written notes; video metadata is not reviewed speech'}

def query(text):
    if not DB.exists(): setup()
    hits = search(text, DB, claims_only=True)
    claims = {c['id']: c for c in read_jsonl(ROOT/'data/claims.jsonl')}
    for hit in hits:
        c = claims[hit['id']]
        hit.update(attribution_confidence=c['attribution_confidence'], empirical_confidence=c['empirical_confidence'], scope=c['scope'])
    return {'status': 'evidence_found' if hits else 'no_evidence', 'query': text, 'results': hits, 'answer_instruction': 'Answer only from relevant reviewed evidence, cite URL and locator; abstain when evidence is absent.'}

def videos(text):
    tokens = text.lower().split()
    rows = json.loads((ROOT/'data/video-catalog.json').read_text())
    found = [r for r in rows if all(t in r['title'].lower() for t in tokens)]
    return {'evidence_type': 'title_metadata_only', 'total_matches': len(found), 'results': found[:30], 'limit': 30}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['setup','search','videos'])
    p.add_argument('query', nargs='?', default='')
    a = p.parse_args()
    print(json.dumps(setup() if a.command=='setup' else query(a.query) if a.command=='search' else videos(a.query), ensure_ascii=False, indent=2))
