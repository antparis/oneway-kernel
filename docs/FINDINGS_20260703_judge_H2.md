# FINDINGS 2026-07-03 — judge hardening H2: 4-pairing cross-field discriminant

STATUS: [HEURISTIQUE sandbox mechanics] — the REAL arbitration is the machine run
(real judge_v2: battery identity + self-test). This session's SINGLE judge patch
(rule respected; H3 exchange-Hermiticity stays queued for next session).

## What the patch does (PURE ADDITION, no existing code path modified)
Ports into judge_v2.py the 4-pairing cross-field discriminant machine-validated
locally in spatial_kernel_test.py (#026) and continuum_kernel_derivation.py (#027):
new function cross_discriminant_2field(K) -> dict pairing -> (entangled, median),
numeric central FD on log K with INDEPENDENT variables, branch-safe (|K|>1e-6),
covers (z,w), (z,wbar), (zbar,w), (zbar,wbar).

## Safety protocol (all automatic, all DEMONSTRATED in sandbox)
0. Refuses without dated backup judge_v2_backup_20260703.py.
1. Refuses double application (demonstrated).
2. PRE-patch 12-case 1-field battery RECORDED (no hardcoded expectations).
3. POST-patch STRICT before/after identity (12/12 demonstrated); any deviation =>
   auto-restore backup + abort (DEMONSTRATED live on the first sandbox run).
4. New-function self-test 4/4: one-way -> (zbar,wbar) only; Bergman -> (z,wbar) only;
   product -> none; paired sum -> ALL FOUR (audit catch: my initial expectation was
   wrong — log of a SUM does not separate, our own sum law #004; the paired-sum
   signature lives in full_conj_2f / exchange-Hermiticity, not in cross-disc).

## Commands (in order, wait for PRESENT/backup confirmation between steps)
    cp ~/Desktop/oxieml-star/judge_v2.py ~/Desktop/oxieml-star/judge_v2_backup_20260703.py
    cd ~/Desktop/oxieml-star && python3 patch_judge_v2_cross_disc.py

## Expected on machine
[pre] 12 cases recorded; [patch] appended; [post] 12/12 IDENTICAL; self-test 4/4 OK;
"PATCH H2 APPLIED AND VERIFIED". Any deviation: auto-restored, paste me the output.
Then engrave #033.

## MACHINE CERTIFIED (2026-07-03) — status upgraded to [ESTABLISHED machine]
Machine run = sandbox digit-for-digit (judge_H2_machine_20260703.txt). Backup
judge_v2_backup_20260703.py created BEFORE patch (rule respected). [pre] 12-case
1-field battery recorded; [patch] pure append; [post] battery identity 12/12
IDENTICAL (zero regression, no hardcoded expectations — strict before/after);
self-test 4/4: one-way -> (zbar,wbar) only; Bergman -> (z,wbar) only; product ->
none; paired sum -> ALL FOUR (sum law #004: log of a sum does not separate — the
pairing signature lives in full_conj_2f / exchange-Hermiticity, not in cross-disc).
No auto-restore triggered. judge_v2.py now exposes cross_discriminant_2field
(4-pairing, numeric FD, independent variables, branch-safe). Registry #033 engraved.
Hardening queue after H2: H1 (narrow annuli grid) and H3 (exchange-Hermiticity leg)
remain — one judge patch per session, next sessions.
