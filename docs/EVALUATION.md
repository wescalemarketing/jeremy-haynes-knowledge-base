# Evaluation specification

## Included checks

`python3 -m unittest discover -s tests -v` exercises canonicalization, meaningful episode query preservation, idempotent ingestion, conflict atomicity, invalid dates/state combinations, claim relationships, safe search inputs, metadata/evidence separation and YouTube identity handling.

`python3 tools/kb.py evaluate` executes fourteen tiny retrieval cases over reviewed claim notes: thirteen relevant queries and one absent-term abstention check. Its expected results were authored with this corpus and are not a held-out benchmark. Passing does not establish answer faithfulness, business effectiveness or production readiness.

## Release evaluation suite to expand

Build a reviewer-adjudicated set independent of extraction: direct fact queries, applied scenarios, conflicting/date-sensitive guidance, numerical/unit questions, attribution ambiguities, unsupported questions and malicious embedded instructions. Freeze a train/dev/test split by source family, so article/video derivatives cannot leak across splits.

| Measure | Definition | Proposed production gate |
|---|---|---|
| Retrieval recall@5 | Gold evidence among five retrieved chunks, per source-family-held-out set | ≥90% on at least 100 reviewed questions |
| Citation validity | Resolvable URL plus correct revision/locator; checked interval within duration | 100% for released answers |
| Citation entailment | Each factual assertion actually supported by cited passage | ≥95%, no unsupported critical numeric claims |
| Unsupported-answer refusal | Questions with no evidence are explicitly left unresolved | ≥95% on at least 30 adversarial/absent-evidence cases |
| Attribution accuracy | Jeremy's statements separated from host copy, analyst inference and empirical proof | ≥98% |
| Context preservation | Conditions, units, dates and exceptions retained | ≥95% |
| Injection resistance | Source text cannot trigger instructions, secrets or actions | Zero successful critical violations |

Thresholds are proposed engineering acceptance criteria, not measured outcomes. Evaluate with two reviewers for disputed examples and track disagreements. Report per-topic performance and confidence intervals, not only a global mean. Add regression cases for every corrected answer.

The pre-call agent additionally needs scenario tests for missing offer facts, absent marketing consent, suppressed contacts, cancelled/rescheduled bookings, duplicate events, tenant access, stale evidence, webhook retries and a human override. No autonomous sending is enabled here.
