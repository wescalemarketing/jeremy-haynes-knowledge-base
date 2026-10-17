# Jeremy Haynes Public Knowledge Repository

Version **0.4.0**, researched **October 16, 2026** (America/Bogota). An independent, source-grounded research project; no affiliation or endorsement implied.

The official channel Videos tab was inventoried through the browser: **265 distinct cards**, matching its displayed count. Browse the [video library](reports/VIDEO_LIBRARY.md), [video CSV](reports/video-inventory.csv), and [context guide](reports/CONTEXT_GUIDE.md). This is a metadata inventory, not 265 reviewed transcripts.

This release contains **450 deduplicated source records**, **37 reviewed claim paraphrases**, **10 framework records**, publisher chapter markers, and an offline citation-first search tool. It is a working research foundation with a partial public-source inventory. It is **not a complete collection or a production pre-call agent**.

Start with [coverage and gaps](reports/COVERAGE.md), the [audit of earlier work](reports/LEGACY_AUDIT.md), and [source inventory CSV](reports/source-inventory.csv). The original v0.1 workbook was not available; no workbook contents were silently carried forward.

## Install for an agent

Start at [AGENT_START.md](AGENT_START.md). A shell-capable agent can install this self-contained skill/data package into an explicitly selected folder and start querying without API keys or external Python packages.

```bash
python3 install.py --dest ./.agent-resources/jeremy-haynes-knowledge
python3 ./.agent-resources/jeremy-haynes-knowledge/tools/agent.py search "confirmation trust urgency"
```

Installation verifies the release manifest and refuses to overwrite a different installation. Chat-only agents can use the hosted data read-only; no link can grant execution permissions to an agent.

## Run locally

Python 3.9+ with SQLite FTS5; no third-party packages, API keys, or network required for the supplied corpus.

```bash
python3 tools/kb.py validate
python3 tools/kb.py build
python3 tools/kb.py search "confirmation trust urgency" --claims-only
python3 tools/kb.py evaluate
python3 -m unittest discover -s tests -v
python3 tools/kb.py coverage
python3 tools/kb.py export
```

Search returns claim/source IDs, a URL, a heading locator and an evidence type. Metadata-only hits locate research material; they do not support substantive answers. The search engine retrieves brief original research notes, not full articles or transcripts. No text-generation service is called.

## Project map

| Path | Purpose |
|---|---|
| `data/sources.jsonl` | Versioned source ledger; dates, availability, state, identity confidence, rights, provenance |
| `data/video-relations.json` | 69 official article/skill links to confirmed channel videos |
| `data/channel-snapshot-audit.json` | Browser collection scope, observed count and reconciliation evidence |
| `data/claims.jsonl` | Source-linked paraphrases; exact heading locators, scope and confidence |
| `data/frameworks.json` | Evidence-linked conceptual summaries and unresolved variants |
| `data/chapters.jsonl` | Publisher-supplied chapter markers, explicitly unverified against media |
| `data/discovery.json` | Metadata-only discovery staging, including listing titles and transient browser references |
| `data/blog-page-audit.json` | Outcomes for all 64 requested blog archive URLs |
| `data/research-log.json` | Queries, restrictions, excluded identities and next research actions |
| `schemas/` | Source and claim data contracts |
| `tools/` | Offline ingestion, canonicalization, search, evaluation and import adapters |
| `docs/` | Ingestion, RAG, evaluation, pre-call agent, rights and private publishing specifications |
| `reports/` | Audit, coverage, machine-readable counts, CSV and validation evidence |

## Extending the corpus

Follow [the ingestion procedure](docs/INGESTION.md). Stage and review metadata, then use `python3 tools/kb.py ingest reviewed-sources.jsonl`. Conflicting revisions require explicit human reconciliation; they are never silently overwritten. Rebuild the search index after approved changes. Preserve related blog/video/podcast versions as separate sources and link them; do not count derivatives as independent corroboration.

For an available legacy workbook:

```bash
python3 tools/audit_workbook.py /absolute/path/Jeremy_Haynes_Knowledge_Repository_v0.1.xlsx --out /tmp/legacy-audit.json
```

This produces untrusted review staging, not automatically approved claims.

For saved public YouTube Data API playlist exports:

```bash
python3 tools/import_youtube.py page-01.json page-02.json --channel-id VERIFIED_CHANNEL_ID --observed 2026-10-16 --out /tmp/youtube-staging.jsonl
```

The adapter imports metadata only. It does not prove pagination completeness or acquire captions. See the channel reconciliation requirements in the ingestion specification.

## Publishing

Public repository: https://github.com/wescalemarketing/jeremy-haynes-knowledge-base

Agents: start with [AGENT_START.md](AGENT_START.md), clone this repository, and run the verified installer into an explicit destination. The [here.now viewer](https://jovial-pellet-79m7.here.now/) provides searchable browsing; anonymous hosting expires unless claimed. See [publishing instructions](docs/PUBLISHING.md).

Do not commit prospect/client data, credentials, raw gated content, media, or unlicensed transcript archives. Source works remain the property of their respective rights holders; private hosting does not grant reuse rights.
