#!/usr/bin/env python3
"""Build a navigable video catalog and reviewed-context links; no content inference."""
import collections
import csv
import json
from kb import ROOT, read_jsonl

TOPICS = {
    'Call funnels and show rates': ['call funnel', 'show rate', 'show up', 'confirmation', 'sales calls'],
    'Webinars and challenge funnels': ['webinar', 'challenge', 'virtual event'],
    'Ads, targeting and creatives': ['paid ad', 'facebook', 'meta ', 'creative', 'pixel', 'retarget', 'cpm', 'content ad'],
    'Offers and ascension': ['offer', 'low ticket', 'low-ticket', 'high-ticket', 'recurring'],
    'Sales teams and follow-up': ['closer', 'sales team', 'follow-up', 'follow up', 'email'],
    'Consultations and case stories': ['live', 'business asked', 'case stud', 'testimonial', 'scaled', 'business update'],
    'Leadership and operations': ['ceo', 'team', 'belief', 'mindset', 'bottleneck', 'plateau', 'time', 'ai ']
}

def topic_tags(title):
    return [topic for topic, words in TOPICS.items() if any(w in title.lower() for w in words)] or ['Other / needs review']

def generate(root=ROOT):
    sources = {s['id']: s for s in read_jsonl(root / 'data/sources.jsonl')}
    claims = read_jsonl(root / 'data/claims.jsonl')
    relations = json.loads((root / 'data/video-relations.json').read_text())
    rows = []
    for s in sources.values():
        if s['kind'] != 'youtube_video': continue
        contexts = sorted({x['context_source_id'] for x in relations if x['video_source_id'] == s['id']})
        claim_ids = [c['id'] for c in claims if c['source_id'] in contexts and c['review_state'] == 'reviewed_paraphrase']
        rows.append({'source_id': s['id'], 'video_url': s['url'], 'title': s['title'], 'channel_membership_verified': s.get('channel_membership_verified', False), 'published_date': s['published_date'], 'duration_display': s.get('duration_display', ''), 'topics_from_title_only': topic_tags(s['title']), 'official_context_urls': [sources[x]['url'] for x in contexts], 'reviewed_context_claim_ids': claim_ids, 'transcript_state': s['transcript_state'], 'content_reviewed': False})
    rows.sort(key=lambda x: x['title'].lower())
    (root / 'data/video-catalog.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    with (root / 'reports/video-inventory.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader()
        for row in rows: w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v for k,v in row.items()})
    lines = ['# Video library — v0.3.0', '', '265 distinct video cards reconciled with the official channel’s displayed count on October 16, 2026. Two additional candidate videos remain outside that confirmed channel inventory.', '', 'Browse labels below are **editorial tags inferred from titles**, not reviewed video-content classifications. Channel membership does not prove Jeremy speaks throughout a video. Promotional title outcomes are not independently verified results.', '', 'The catalog links reviewed article notes where available. These are companion context, not exact transcripts. All video-content review states remain incomplete.', '']
    for topic in list(TOPICS) + ['Other / needs review']:
        selected = [x for x in rows if topic in x['topics_from_title_only']]
        if not selected: continue
        lines += ['## '+topic, '', '| Video | Duration shown | Companion context |', '|---|---|---|']
        for row in selected:
            title = row['title'].replace('|', '\\|')
            contexts = ', '.join('[article/skill]('+u+')' for u in row['official_context_urls']) or 'Not mapped'
            if row['reviewed_context_claim_ids']: contexts += ' — '+str(len(row['reviewed_context_claim_ids']))+' reviewed context notes'
            lines.append('| ['+title+']('+row['video_url']+') | '+row['duration_display']+' | '+contexts+' |')
        lines.append('')
    (root / 'reports/VIDEO_LIBRARY.md').write_text('\n'.join(lines)+'\n')
    return {'videos': len(rows), 'channel_verified': sum(x['channel_membership_verified'] for x in rows), 'with_official_context': sum(bool(x['official_context_urls']) for x in rows), 'with_reviewed_context_notes': sum(bool(x['reviewed_context_claim_ids']) for x in rows)}

if __name__ == '__main__':
    print(json.dumps(generate(), indent=2))
