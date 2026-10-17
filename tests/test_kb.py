import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import kb
from import_youtube import convert
from duplicate_candidates import candidates
from import_channel_snapshot import convert as convert_snapshot, duration_estimate

class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.sample = copy.deepcopy(kb.read_jsonl(kb.ROOT / 'data/sources.jsonl')[0])

    def test_youtube_aliases_share_identity(self):
        urls = ['https://youtu.be/sD55I_RH5ho?t=12', 'https://www.youtube.com/embed/sD55I_RH5ho?feature=oembed', 'https://www.youtube.com/watch?v=sD55I_RH5ho&utm_source=x', 'https://www.youtube.com/shorts/sD55I_RH5ho']
        self.assertEqual(len({kb.source_id(u) for u in urls}), 1)

    def test_podcast_episode_id_is_preserved(self):
        self.assertNotEqual(kb.source_id('https://podcasts.apple.com/show?i=100'), kb.source_id('https://podcasts.apple.com/show?i=101'))

    def test_credentials_and_non_web_urls_rejected(self):
        for url in ('file:///tmp/source', 'https://secret@example.com/path', 'javascript:alert(1)'):
            with self.assertRaises(ValueError): kb.canonical(url)

    def test_ingestion_idempotent(self):
        incoming, target = self.dir/'incoming.jsonl', self.dir/'target.jsonl'
        kb.write_jsonl(incoming, [self.sample])
        kb.ingest(incoming, target)
        before = target.read_bytes()
        kb.ingest(incoming, target)
        self.assertEqual(target.read_bytes(), before)

    def test_conflicting_batch_cannot_partially_modify_ledger(self):
        incoming, target = self.dir/'incoming.jsonl', self.dir/'target.jsonl'
        kb.write_jsonl(target, [self.sample])
        before = target.read_bytes()
        other = copy.deepcopy(self.sample)
        other['url'] = 'https://example.org/new'
        other['id'] = kb.source_id(other['url'])
        conflict = copy.deepcopy(self.sample)
        conflict['title'] += ' changed'
        kb.write_jsonl(incoming, [other, conflict])
        with self.assertRaises(ValueError): kb.ingest(incoming, target)
        self.assertEqual(target.read_bytes(), before)

    def test_unavailable_content_cannot_be_extracted(self):
        self.sample.update(availability='fetch_failed', processing_state='extracted')
        with self.assertRaises(ValueError): kb.validate_source(self.sample)

    def test_bad_and_future_dates_rejected(self):
        for value in ('2026-02-30', '2027-01-01'):
            self.sample['published_date'] = value
            with self.assertRaises(ValueError): kb.validate_source(self.sample)

    def test_full_ledger_and_claim_references(self):
        result = kb.validate()
        self.assertGreater(result['sources'], 0)
        self.assertGreater(result['claims'], 0)

    def test_metadata_does_not_become_evidence(self):
        db = self.dir/'index.sqlite'
        kb.build(db)
        self.assertTrue(kb.search('hypnotized', db))
        self.assertEqual(kb.search('hypnotized', db, claims_only=True), [])

    def test_search_handles_operators_and_sql_text(self):
        db = self.dir/'index.sqlite'
        kb.build(db)
        kb.search('" OR 1=1; DROP TABLE evidence; --', db)
        self.assertTrue(kb.search('confirmation', db, claims_only=True))

    def test_retrieval_smoke(self):
        db = self.dir/'index.sqlite'
        kb.build(db)
        result = kb.evaluate(db)
        self.assertEqual(result['passed'], result['total'])

    def test_youtube_channel_mismatch_rejected(self):
        item = {'snippet': {'channelId': 'wrong', 'title': 'Title', 'resourceId': {'videoId': 'sD55I_RH5ho'}}}
        with self.assertRaises(ValueError): convert([{'items': [item]}], 'expected', '2026-10-16')

    def test_youtube_duplicates_and_incomplete_page_report(self):
        item = {'snippet': {'channelId': 'expected', 'title': 'Title', 'resourceId': {'videoId': 'sD55I_RH5ho'}}, 'contentDetails': {'videoPublishedAt': '2026-01-01T00:00:00Z'}}
        rows, report = convert([{'items': [item, item], 'nextPageToken': 'next'}], 'expected', '2026-10-16')
        self.assertEqual(len(rows), 1)
        kb.validate_source(rows[0])
        self.assertTrue(report['final_page_has_next'])
        self.assertFalse(report['coverage_verified'])

    def test_title_similarity_only_reports_candidates(self):
        rows = [{'id': 'a', 'title': 'Scale paid advertising'}, {'id': 'b', 'title': 'Scale paid advertising'}]
        self.assertEqual(len(candidates(rows)), 1)
        self.assertEqual(len(rows), 2)

    def test_channel_snapshot_rejects_count_mismatch(self):
        row = {'video_id': 'sD55I_RH5ho', 'title': 'Title', 'duration_label': '52 minutes'}
        with self.assertRaises(ValueError): convert_snapshot([row], '2026-10-16', 265)
        with self.assertRaises(ValueError): convert_snapshot([row, row], '2026-10-16', 2)

    def test_channel_snapshot_duration_is_explicitly_rounded(self):
        self.assertEqual(duration_estimate('1 hour, 1 minute'), 3660)
        rows = convert_snapshot([{'video_id': 'sD55I_RH5ho', 'title': 'Title', 'duration_label': '52 minutes'}], '2026-10-16', 1)
        self.assertIsNone(rows[0]['published_date'])
        self.assertEqual(rows[0]['duration_precision'], 'rounded_minutes')
        self.assertEqual(rows[0]['processing_state'], 'metadata_reviewed')

    def test_context_search_preserves_article_citation_and_video_navigation(self):
        db = self.dir/'index.sqlite'
        kb.build(db)
        hits = kb.search('funnel friction capacity', db, claims_only=True)
        hit = next(x for x in hits if x['id'] == 'clm_friction_v03_01')
        self.assertIn('jeremyhaynes.com/', hit['url'])
        self.assertIn('https://www.youtube.com/watch?v=fMiSOqBTBEA', hit['related_video_urls'])

if __name__ == '__main__':
    unittest.main()
