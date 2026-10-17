#!/usr/bin/env python3
"""Report possible title duplicates for review; never merge works automatically."""
import json
import re
from itertools import combinations
from kb import ROOT, read_jsonl

def candidates(rows, threshold=0.65):
    words = {s['id']: set(re.findall(r'\w+', s['title'].lower())) - {'the', 'a', 'to', 'and', 'how', 'of', 'in'} for s in rows}
    result = []
    for a, b in combinations(rows, 2):
        left, right = words[a['id']], words[b['id']]
        similarity = len(left & right) / len(left | right) if left | right else 0
        if similarity >= threshold:
            result.append({'source_ids': [a['id'], b['id']], 'titles': [a['title'], b['title']], 'jaccard': round(similarity, 3), 'state': 'needs_human_review'})
    return sorted(result, key=lambda x: -x['jaccard'])

if __name__ == '__main__':
    print(json.dumps(candidates(read_jsonl(ROOT / 'data/sources.jsonl')), indent=2, ensure_ascii=False))
