#!/usr/bin/env python3
"""Import saved public YouTube Data API playlistItems pages; never fetch media/captions."""
import argparse
import json
from pathlib import Path
from datetime import date
from kb import source_id, write_jsonl

def convert(pages, channel_id, observed):
    rows, tokens, seen = [], [], set()
    for page in pages:
        if page.get('nextPageToken'):
            tokens.append(page['nextPageToken'])
        for item in page.get('items', []):
            snippet = item['snippet']
            if snippet.get('channelId') != channel_id:
                raise ValueError('Unexpected playlist owner; verify channel identity')
            vid = snippet.get('resourceId', {}).get('videoId')
            if not vid or vid in seen:
                continue
            seen.add(vid)
            url = 'https://www.youtube.com/watch?v=' + vid
            published = item.get('contentDetails', {}).get('videoPublishedAt')
            rows.append({'id': source_id(url), 'url': url, 'title': snippet['title'], 'kind': 'youtube_video', 'published_date': published[:10] if published else None, 'observed_date': observed, 'availability': 'public_page' if published else 'unknown', 'processing_state': 'metadata_reviewed', 'confidence': 'medium', 'locator': 'YouTube Data API playlistItems metadata; no content reviewed', 'rights': 'metadata_only; transcript rights not assessed', 'provenance': [{'method': 'saved_youtube_api_export', 'channel_id': channel_id}], 'official': True, 'transcript_state': 'not_checked', 'timestamp_state': 'not_reviewed', 'notes': 'Channel identity must be independently confirmed before ingest.'})
    # Exported pages alone cannot prove page-token continuity or all content surfaces.
    return rows, {'pages_imported': len(pages), 'next_page_tokens_seen': tokens, 'final_page_has_next': bool(pages and pages[-1].get('nextPageToken')), 'coverage_verified': False, 'remaining_checks': ['Check request/response page-token chain and uploads playlist identity', 'Reconcile channel Videos/Shorts/Live and removals; public uploads only']}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('pages', nargs='+', type=Path)
    p.add_argument('--channel-id', required=True)
    p.add_argument('--observed', default=date.today().isoformat(), help='Observation date; set explicitly in local timezone')
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    rows, report = convert([json.loads(x.read_text()) for x in a.pages], a.channel_id, a.observed)
    write_jsonl(a.out, rows)
    print(json.dumps(report, indent=2))
