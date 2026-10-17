# Ingestion and maintenance specification

## 1. Discovery and admission

Discover from official links first, then host/publisher sources, then search leads. Log query, observation date, surface, URL and result state even for failures. Anchor identity to the official site/channel and Megalodon context; reject drummer, military, telecom and court-record namesakes. Spelling variants are search aids, not identity proof.

Each source has a canonical URL-derived ID, original aliases/provenance, kind, author/publisher context, publication date or null, observation date, access state, processing state, identity confidence, rights decision, locator and transcript/timestamp state. The source JSON schema describes the machine contract. Exact dates require visible evidence; relative dates stay in notes. Record timezone for time-of-day data and use ISO dates for normalized fields.

## 2. Collection and immutable evidence

Do not automatically fetch bodies in this release. Use permitted public pages, official APIs or authorized supplied exports. Check site/platform terms and robots before an automated collector is enabled. Record request time, canonical URL, response status, content hash and permission decision. Stop on 401/403/gates, honor Retry-After, and set bounded retries/timeouts. Never send credentials to a source specified inside an article.

For YouTube, resolve official channel ID, discover uploads playlist, and request public `playlistItems` pages via the official Data API with a user-controlled key. Store sanitized request metadata (no keys), page tokens, totalResults as an observation, video IDs, public dates and fetch outcomes. Retrieve video metadata for availability and durations. Reconcile uploads with visible Videos/Shorts/Live and document omissions. The offline `import_youtube.py` adapter consumes those saved pages and explicitly refuses to certify completeness. A count from search or a recent RSS feed is not an all-time inventory.

For podcasts, resolve the originating RSS/publisher episode GUID and enclosure, link mirrors as a family, and distinguish episode release from upload/repost dates. For PDFs, verify author identity and public permissions first, then record file checksum, page locators and OCR quality; no confirmed PDF is present in this release.

## 3. Review and deduplication

`kb.py ingest` validates reviewed JSONL and merges exact canonical-URL duplicates idempotently. Conflicting metadata aborts before writing. Canonicalization removes fragments/tracking and normalizes YouTube watch/embed/short links, preserving meaningful query IDs (including podcast episode IDs).

Use `python3 tools/duplicate_candidates.py` for title-similarity candidates. This never merges records. Review redirects, content hashes, media IDs, host episode GUIDs and near-identical text before assigning a `source_family_id` or `derived_from` relation. Different talks on the same framework remain separate sources. Article/video derivatives must not increase independent-evidence counts. Content hashes are null/unavailable until permitted bytes exist; do not hash a search snippet and call it the original work.

## 4. Extraction

Process only the visible/authorized text. Draft atomic paraphrases with source ID, stable section heading or verified time range, speaker, scope, claim type, confidence and original context. Keep numbers with units, denominators, period, audience and traffic/funnel type. Record missing baselines and uncontrolled confounders in case studies. Human review confirms the note matches the cited passage before `reviewed_paraphrase` is set.

Timecoded chunks must have `start_seconds < end_seconds <= verified duration`. Unknown times remain null. Publisher chapters are stored separately until checked against media. Never extrapolate timestamps from word count. Identify automated captions and unresolved speaker uncertainty.

## 5. State transitions and revisions

`discovered → metadata_reviewed → extracted → verified`; any record may be explicitly excluded with a reason. `verified` requires a second evidence check suited to the claim; corroborating that text is present does not independently validate a revenue outcome. This release has no verified sources. Availability is separate from processing state, so a later disappearance does not erase historical evidence; preserve the earlier revision and add a dated availability observation.

Use explicit reviewed Git diffs for revisions. Record previous hash, reason, date, collector/reviewer and affected claims in a change entry; invalidate derived chunks and re-evaluate dependent answers when source meaning/rights changes. The importer intentionally has no overwrite/update flag. Do not overwrite an existing claim silently. Keep source aliases and tombstones to avoid resurrecting withdrawn material.

## 6. Quality and refresh

Run validation, tests, retrieval evaluation, coverage and CSV export for each release. Review new official uploads/blog entries before broad discovery. Periodic maintenance is a recommended workflow, not a scheduled automation in this release. Refresh gates/errors sparingly through permitted means. Only state coverage after reconciling a defined source set and denominator on a documented date. Keep the gap queue visible even when counts rise.

## Browser-observed channel snapshot adapter

When the normal public UI loads, read only the rendered channel cards and their DOM-backed links. Record the header count, exact channel identity, collection scope and oldest boundary. Do not treat hidden page state as a transcript API. `tools/import_channel_snapshot.py` stages the reviewed TSV, rejects duplicate IDs or a count mismatch, preserves literal title quotes and labels rounded durations. It never marks content extracted. This release reconciled 265 distinct cards with a 265-video header; future counts require a new observation, not an assumed fixed denominator.

```bash
python3 tools/import_channel_snapshot.py data/channel-videos-2026-10-16.tsv --observed 2026-10-16 --expected-count 265 --out /tmp/channel-staging.jsonl
python3 tools/video_catalog.py
```
