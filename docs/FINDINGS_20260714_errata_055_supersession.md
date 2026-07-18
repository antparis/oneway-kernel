# FINDINGS 2026-07-14 — Errata: #055 supersession note (#056)

Status: [ESTABLISHED machine+judge] for #055's underlying result (already
certified 2026-07-13); this note itself is pure bookkeeping, zero new
execution, zero new judge call.

## What changed
#055 (2026-07-13) certified that exchange-Hermiticity (Delta = K - M(S(K)))
and reciprocity (R = K - S(K)) are INDEPENDENT axes, not the same thing.
Four quadrants occupied: decoy (Delta=0,R!=0), C0/C1 (Delta!=0,R=0),
one-way (Delta!=0,R!=0), reciprocal-Hermitian trivial (Delta=0,R=0).

## Semantic debt closed by this entry
#026, #027, #028, #040, #045 used "exchange-Hermiticity" as if it were a
reciprocity certificate. Originals NOT rewritten (append-only). K3 in
DETECTOR_RULES_20260703.md relabeled (section 6, errata) from required
gate to independent discriminant -- still valid against the Bergman decoy
(P6), no longer sufficient alone for a one-wayness/reciprocity verdict.

## What this does NOT do
Does not touch #055's own open flag (comparative phase-law witness for
#040, C1 test in judge). Does not touch the ASYM/positivity question
(#052, size-cone). Both are separate, live chantiers.

Trace: DETECTOR_RULES_20260703.md section 6, IDEAS_REGISTRY.md #056.
