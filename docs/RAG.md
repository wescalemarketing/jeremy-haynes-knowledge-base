# Search and RAG specification

## Implemented baseline

SQLite FTS5 indexes source titles and reviewed claim paraphrases separately. Queries are tokenized and quoted; SQL uses bound parameters. `--claims-only` excludes titles from evidence retrieval. Every result includes claim/source IDs, URL, locator, evidence type and rank. Reviewed article hits also include related video URLs when an official link exists; those URLs are navigation rather than proof of transcript equivalence. The index is disposable and rebuilt from versioned data. No embeddings, hosted database, generative model or production answer API is implemented.

## Production design

1. Admit only rights-cleared evidence. Store immutable source versions and provenance; separate untrusted content from control prompts.
2. Chunk permitted text by semantic section and speaker. A starting configuration is 300–700 tokens with limited overlap; these are engineering defaults to evaluate, not Jeremy's recommendations. Carry source version, heading, interval, language, rights, audience, date, framework and family ID into each chunk.
3. Retrieve with lexical plus embedding search. Filters include source date, official/guest, framework, traffic type, funnel and reviewed status. Choose an embedding service only after data-use/rights and cost review; do not upload gated material by default.
4. Rerank evidence; diversify by source family. Retrieve context and explicit counterexamples/variants. Avoid treating blog adaptations, video transcripts and podcast mirrors as three independent witnesses.
5. Generate only from retrieved passages. Return answer, exact supporting citations, applicable conditions, contextual variants, assumptions and unknowns. Researcher inference is labeled separately. A title, chapter marker or search summary alone cannot justify a substantive claim.
6. Resolve each citation against the exact source revision. Verify that quoted/paraphrased detail is entailed and timestamps are within duration. When relevant evidence is absent, abstain and return an actionable research gap.

## Temporal and contradiction handling

Publication time, observation time and a strategy's asserted historical origin are different fields. Do not use a publication date as proof of when an idea originated. Store contradiction edges with claim IDs, scope, units, dates and adjudication state. Prefer current applicability only when the source explicitly supports it; retain historical positions.

The seed corpus shows why this matters: a creative library of 30–50 items is different from 15–20 delivered impressions. These formulations have different units and cannot be collapsed into a single count. They are documented variants, not evidence of a resolved contradiction or a universal mandate.

## Security and operations

Treat all fetched pages, transcripts and skill instructions as untrusted quoted data. Disregard embedded requests to reveal secrets, call tools, alter permissions or change the answer policy. Retrieval cannot authorize actions. Partition client data by tenant outside this repository; enforce access at query time and on caches, logs and backups. Use source deletion/permission revocation to invalidate indexes and derived answers. Logs retain IDs/version hashes rather than unnecessary personal content.

Model performance, ranking quality, latency/cost and citation faithfulness require separate measurement. The included benchmark is only a small retrieval smoke check.
