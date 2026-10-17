# Pre-call agent specification — draft, not deployed

## Purpose and boundaries

Prepare a useful, source-cited pre-call briefing and educational sequence for a consenting prospect. Separate Jeremy-derived principles, operator-supplied offer facts and agent hypotheses. It must never invent offer outcomes, guarantees, urgency, client proof, consumption or suitability. It does not impersonate Jeremy or claim endorsement.

## Inputs

Use a separate access-controlled client system for prospect ID, tenant, booking ID/time/timezone/status, communication consent and suppression state, acquisition channel, prospect-volunteered goals/questions, and observed content events. Offer inputs include approved claims, pricing, delivery, eligibility, limitations, proof assets, support terms and available educational content with rights cleared. Define measurement windows and denominators for spend, qualified bookings, held calls, closes, refunds and collected cash. Unknown facts remain unknown.

## Evidence-grounded decision flow

1. Validate booking, timezone, consent and tenant access. Stop if cancelled, suppressed, unauthorized or consent is missing. Do not infer consent from mere inclusion in a CRM.
2. Ask for missing offer/traffic/funnel facts needed for diagnosis. Use the four-pillar framework as a diagnostic checklist rather than asserting a cause from one metric (`clm_fix_01`, `clm_fix_02`).
3. Identify the buyer's stated trust, timing and information concerns. Recommend an approved main video and breakout topics using `clm_confirm_01` and `clm_confirm_02`. Any urgency must be independently true for this offer.
4. Match approved assets to open questions. Keep page, email and setter explanations consistent (`clm_confirm_04`). Link to real suitability/support evidence (`clm_confirm_05`). Do not claim every prospect needs the same number of videos.
5. Propose a bounded sequence that fits time to call, the prospect's consent/preferences, and operator policy. The Hammer Them counts are contextual source recommendations (`clm_fix_03`, `clm_hammer_01`, `clm_hammer_02`), not default sending commands. Require human approval for campaign activation.
6. Update the briefing only from observed events. Distinguish page load, play, depth and self-report (`clm_confirm_03`). Never mark a prospect “educated” from an email open or aggregate percentage alone.
7. Hand off a concise briefing to the closer: stated need, known facts, questions remaining, assets offered, measured activity, uncertainties and evidence links. Avoid unsupported psychological profiles or wealth inference.

## Output contract

```json
{
  "booking_id": "operator-supplied",
  "status": "draft_requires_human_review",
  "known_facts": [],
  "missing_inputs": [],
  "buyer_questions": [],
  "recommended_assets": [],
  "draft_sequence": [],
  "closer_brief": "",
  "evidence": [{"claim_id": "clm_confirm_01", "source_id": "resolve-from-ledger", "locator": "Choose the Main Video From the Buyer’s Concern"}],
  "assumptions": [],
  "human_decisions_required": ["approve content and cadence"]
}
```

## Operational controls

Run in read-only/draft mode initially. A future sender must recheck consent/suppression immediately before dispatch, cancel queued actions on cancellation/reschedule, use idempotency keys `(tenant, booking, sequence_version, step)`, cap sends by operator policy, handle timezones/quiet hours, support opt-out and human takeover, and log the approved content/version. CRM writes and outreach require explicit deployment authorization. No connector credentials or prospect records are stored in this project.

## Success measurement

Define qualified-booking → held-call show rate, held-call → sale close rate, collected cash per qualified booking, refunds, complaints and opt-outs. Compare cohorts by traffic source and booking lead time. A controlled experiment or careful staged comparison is required before crediting sequence changes with revenue improvements. Track customer understanding and suitability alongside conversion; avoid universal uplift promises from self-reported case stories.

Release only after rights, retrieval, citation, suppression, retry, tenant isolation and human-control tests pass. A draft system prompt and scenario fixture are included as design artifacts; no live agent or automated outreach has been installed.

## v0.3 evidence expansion

The reviewed article corpus now includes friction/intent (`clm_friction_v03_*`), activation/ascension (`clm_ascension_v03_*`), creative testing (`clm_creative_v03_*`), conversion signals (`clm_pixel_v03_*`), webinar math (`clm_webinar_v03_*`), sales bench readiness (`clm_bench_v03_*`) and follow-up (`clm_followup_v03_*`). Use these as conditional diagnostic evidence. Video URLs attached to search results are companion navigation; they do not replace the written citation or imply the spoken claim has been checked.
