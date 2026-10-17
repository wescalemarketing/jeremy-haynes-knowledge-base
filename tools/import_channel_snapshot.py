#!/usr/bin/env python3
"""Convert a reviewed, UI-observed channel TSV to source staging. No network calls."""
import argparse
import csv
from datetime import date
import json
import re
from pathlib import Path
from kb import source_id, write_jsonl

CHANNEL = 'https://www.youtube.com/@JeremyHaynesTraining/videos'
CHANNEL_ID = 'UCuzbImxdBNTUeolGXpLVL0A'

def duration_estimate(label):
    units = {'hour': 3600, 'minute': 60, 'second': 1}
    parts = re.findall(r'(\d+) (hour|minute|second)s?', label)
    if not parts:
        raise ValueError('Unrecognized displayed duration')
    return sum(int(n) * units[u] for n, u in parts)

def convert(rows, observed, expected_count):
    date.fromisoformat(observed)
    ids, result = set(), []
    for row in rows:
        video_id = row['video_id']
        if not re.fullmatch(r'[\w-]{11}', video_id) or video_id in ids or not row['title'].strip():
            raise ValueError('Invalid or duplicate video ID/title')
        ids.add(video_id)
        url = 'https://www.youtube.com/watch?v=' + video_id
        result.append({'id': source_id(url), 'url': url, 'title': row['title'], 'kind': 'youtube_video', 'published_date': None, 'observed_date': observed, 'availability': 'public_page', 'processing_state': 'metadata_reviewed', 'confidence': 'high', 'locator': 'Official channel Videos tab; displayed public video card', 'rights': 'Public metadata only; no media or full captions copied', 'provenance': [{'method': 'native_browser_visible_channel_card', 'discovery_url': CHANNEL, 'channel_id': CHANNEL_ID, 'observed_date': observed}], 'official': True, 'channel_id': CHANNEL_ID, 'channel_membership_verified': True, 'duration_display': row['duration_label'], 'duration_seconds_display_estimate': duration_estimate(row['duration_label']), 'duration_precision': 'displayed_seconds' if 'second' in row['duration_label'] else 'rounded_minutes', 'transcript_state': 'not_checked', 'timestamp_state': 'not_reviewed', 'body_extraction_state': 'not_systematically_extracted', 'content_sha256': None, 'notes': 'Channel membership, title and displayed duration observed. Title outcomes are promotional claims, not verified results. Publication date and content remain to be reviewed.'})
    if len(ids) != expected_count:
        raise ValueError('Snapshot differs from observed channel count; reconcile before import')
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('tsv', type=Path)
    p.add_argument('--observed', required=True)
    p.add_argument('--expected-count', type=int, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    with a.tsv.open() as f:
        rows = convert(list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)), a.observed, a.expected_count)
    write_jsonl(a.out, rows)
    print(json.dumps({'staged': len(rows), 'scope': 'Observed public Videos tab only; not all appearances or historical/deleted uploads'}))
