# Coverage report — v0.2.0

As of October 16, 2026. Counts are reproduced by `python3 tools/kb.py coverage`; detailed source rows are in `source-inventory.csv`.

**188 canonical source records; 11 reviewed claim paraphrases from 4 sources. Full coverage is not verified.** Metadata reviewed does not mean content extracted. There are no independently verified outcome claims and no full transcript collection.

| Surface | Inventoried | Denominator / limitations |
|---|---:|---|
| Official skills | 38 landing pages | 38 reported by [official catalog](https://jeremyhaynes.com/skills/); 38/38 landing links resolved. At least 12 returned visible email-gated body notices; full-body access for the remaining pages is not implied. One skill has reviewed claim notes. |
| Blog + case-study sources | 129 unique records | 127 blog + 2 case-study records, including additional targeted discoveries. No verified total published article denominator. |
| Blog archive navigation | 64 URLs attempted; 17 parsed | 138 listing observations; 134 resolved-document observations before URL deduplication. Four listing resolutions yielded no usable document metadata. Cached pagination differs: first page advertises 64; readable page 61 advertises 61. This is not a coherent live snapshot. |
| Official YouTube | 1 channel, 2 officially linked videos | Channel verified by official site's outbound link. Channel listing returned a stale footer; both linked video fetches failed. No public upload denominator, playlist completeness or caption availability established. |
| Other YouTube candidates | 3 | IDs found via third-party transcript/summary indexes; ownership and availability unverified. No copied transcripts. |
| Podcasts | 8 episode records | Public discovery metadata; only the Manos page received a usable direct page review in the final check. Audio not listened to. Most entries need originating host/RSS resolution. |
| Other interviews/appearances | 3 | Two written interview pages and one derivative interview index. Inventory open-ended; primary media checks pending. |
| Public PDFs | 0 authenticated | Searches yielded unrelated namesakes and references to restricted student material. Zero found is not evidence that none exist. |
| Agency site / case-study archive | 1 site lead | Officially linked; independent page inventory pending. Two official-site case narratives already cataloged. |

The 188 total also includes the official homepage and two catalog pages. Three publisher chapter records are stored for two podcasts; they are metadata, not timecoded factual extraction.

## Availability and extraction

158 sources have a readable public landing/page response, 12 show a body gate, 11 are search-result-only, 4 have unknown availability, and 3 failed content fetches. These are observation states, not guarantees of current global availability. Browser search may serve cached text. Direct public-site requests returned HTTP 403; automated collection stopped rather than changing identity or bypassing the restriction. Robots and sitemap access could not be established.

180 sources are metadata reviewed, 4 extracted into limited claim notes, and 4 remain discovery leads. “Extracted” means the represented short notes were checked against visible text; it does not mean the entire work was exhaustively processed.

## Highest-priority gaps and completion criteria

1. **Recover v0.1 workbook.** Obtain original bytes, hash, inventory tabs/rows, preserve provenance and recheck every source before merging.
2. **YouTube public inventory.** Resolve current channel ID through the official link, retrieve authorized public Data API uploads metadata with recorded pagination, reconcile Videos/Shorts/Live, and document deletions/unavailable entries. Never infer access to private/unlisted material.
3. **Archive completeness.** Obtain a permitted sitemap/export or a consistent full public archive pass. Reconcile 47 archive URLs without parsed listings, four unresolved listing clicks, duplicates, changing dates, redirects and missing articles. The apparent 17/64 is URL-attempt coverage, not article coverage.
4. **Transcripts and timecodes.** Check each video's authorized caption availability; acquire only permitted text. Review speaker attribution and align intervals against media. Currently no claim has verified media timestamps.
5. **Skills body permissions.** Preserve the distinction between public catalog and gated files. Seek rights-holder permission or authorized supplied files; do not submit an email or unlock content automatically.
6. **Guest appearances.** Expand host-specific discovery, resolve originating feeds, cross-link mirrors, and review episodes. Fresh & Fit is mentioned in a skill but no exact qualifying episode was verified; it remains a research question, not an invented source record.
7. **PDFs and case evidence.** Verify author identity and public permissions before acquisition. Seek primary case evidence, baseline dates, denominator, spend, margins and attribution. Student-only ad-fatigue SOP remains excluded.
8. **Deep extraction and temporal mapping.** Review high-value sources in full, build source families, reconcile contextual numeric variants, and expand evaluation beyond a tiny smoke benchmark.

## Research limits

Search engines are incomplete and results are personalized/cached. Undated pages retain null publication dates; relative update labels are not converted to invented exact dates. Matching names do not establish identity. No claim to “most complete in the world” can be tested with the available evidence.
