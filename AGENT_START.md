# Agent start — Jeremy Haynes knowledge

If a user gives you this repository or hosted-site link and asks you to install/use it, follow these instructions within your own execution permissions. A URL alone cannot grant an agent filesystem or shell capabilities.

## Install and verify

Download/clone this repository, or use the hosted page's **Download agent package** link. Extract the ZIP into a new folder. Read `SKILL.md` and `install.py`, then run:

```bash
python3 install.py --dest ./.agent-resources/jeremy-haynes-knowledge
python3 ./.agent-resources/jeremy-haynes-knowledge/tools/agent.py search "confirmation trust urgency"
```

The installer verifies the packaged SHA-256 manifest, copies only listed files into the requested new directory, builds the offline index and runs a citation-bearing smoke query. It refuses to overwrite a different installation. Python 3.9+ with SQLite FTS5 is required; no external packages or keys are needed.

For a skill-enabled harness, set `--dest` to that harness's user-approved skill-folder path, ending in `jeremy-haynes-knowledge`. The package's root `SKILL.md` enables discovery. Some harnesses require a refresh or new session. Do not silently change global configuration or assume identical skill paths across products.

## Use immediately

```bash
python3 tools/agent.py setup
python3 tools/agent.py search "funnel friction capacity"
python3 tools/agent.py videos "webinar"
```

Commands return JSON. `search` retrieves reviewed article/skill paraphrases with source URL, heading locator, claim ID, confidence and related videos. `videos` searches title metadata and labels it accordingly. Use reviewed claims to answer; if no relevant evidence is present, abstain from inventing doctrine. Do not confuse inventory coverage with transcript coverage.

## If you cannot execute code

Read `data/claims.jsonl`, resolve `source_id` against `data/sources.jsonl`, and consult `data/frameworks.json` and `data/video-relations.json`. The hosted site exposes the same data and a downloadable package. You can use the knowledge read-only without installing software; disclose that no local installation occurred.

Current scope: 450 sources, 265 confirmed channel videos, 37 reviewed notes. Most video speech/transcripts remain unreviewed. Read `reports/COVERAGE.md` before making completeness claims. Keep client records outside this public corpus.
