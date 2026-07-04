# FINDINGS 2026-07-03 — spatial two-point Jordan kernel (the #025 identified object)

STATUS: [HEURISTIQUE sandbox] — machine (real judge_v2) arbitrates. Stage-2 continuum
form is [DERIVATION] (class inherited from the DRUM cross-kernel derivation); the exact
continuum derivation for THIS spatial LG system is OPEN (see "remaining").

## Object and why it escapes #025
K(z,zbar; w,wbar): field 1 = observation point, field 2 = source point, of the M1 Jordan
one-way coupling on spatial LG carriers. A transfer kernel depends on NO drive: the #025
preparation-erasure axis does not exist. The forced content = G12 = 0 + G21 double pole
(k/lambda^2), non-erasable by licit gauge [#021 GATE A machine]. spatial_carrier (7th
condition, the DRUM killer) satisfied by construction (LG plane coordinates).

## Tooling
- TOOLING GAP CAUGHT: judge_v2.mixed_discriminant is INTRA-field (dz dzbar). The decisive
  two-point entanglement is CROSS-field: d_z d_wbar log K — implemented locally
  (cross_disc); judge-hardening candidate, pending (one judge patch per session, #024
  consumed this session's).
- Numeric nonzero checks on random sample points (no simplify on log expressions —
  timeout discipline).
- full_conj_2f = swap both pairs + I->-I (pairing test, two-field mirror).

## Command
    python3 spatial_kernel_test.py    # in the repo (imports judge_v2, awake_defective_pair)

## Sandbox results (kernel_sandbox_20260703.txt)
STAGE 1 (finite 2-mode kernel, Jordan numbers lam=-0.57, k=one-way entry):
- K2 Jordan (diag + one-way cross): cross-disc != 0 (sum law #004, two-field side),
  non-paired -> gate PASS.
- Product control (single term): cross-disc ~ 1e-16 -> FAIL (product wall confirmed).
- TRUNCATION ARTIFACT CAUGHT (self-audit): a 2-mode set {+1p0,-1p1} is not
  conjugation-closed -> spurious pairing residual on a naive Hermitian control. Clean
  conjugation-closed controls: Hermitian = half + mirror(half) -> paired residual
  EXACTLY 0 -> FAIL; Jordan one-way half -> non-paired -> PASS. DISCRIMINATION LAW
  (kernel level): reciprocity <=> conjugation-paired kernel; one-wayness <=> the
  unpaired half survives alone.
STAGE 2 (continuum class rep, spatial carrier):
- K = log(z - wbar): certify_2field = CROSS-CONJUGATE (holo field1, anti field2);
  cross-disc != 0; NON-paired; transcendental -> TARGET CORNER of the 2-field cube: PASS.
- Primitive (z-wbar)(log(z-wbar)-1): same class, PASS.
- Historical traps all behave: log(z-w) holo-holo FAIL; PAIRED sum
  log(z-wbar)+log(zbar-w) -> full_conj_2f-invariant residual 0.0 -> FAIL (the
  "transcendant apparie" trap = precisely the RECIPROCAL continuum kernel); product
  log(z)*log(wbar) cross-separable FAIL.
Structure: one-way <=> single log (non-paired); reciprocal <=> paired sum. The
one-wayness is exactly what deletes the mirror partner.

## Remaining before any claim beyond [DERIVATION]
1. Machine run (real judge_v2) — blocking.
2. The exact continuum derivation for the spatial LG system: DRUM derived
   log(z1-zbar2) from 2D CFT propagators; asserting the same class here is inheritance,
   not derivation. Open task: the mode-sum over the LG-continuum with one-way weights ->
   closed form, then judge.
3. Measurability note [CONJECTURE, do not oversell]: a transfer kernel IS an observable
   protocol (response at r1 to a source at r2) — potentially the strongest measurability
   profile yet; to be argued only after 1-2.

## MACHINE CERTIFIED (2026-07-03) — status upgraded to [ESTABLISHED machine]
Machine run = sandbox digit-for-digit (kernel_machine_20260703.txt), real judge_v2
certify_2field/rephasing_test. Setup: lambda=-0.57, k=-0.7643-0.2364i, G12=4e-17~0.
STAGE 1: K2 Jordan PASS (cross-disc 1.5e-2, non-paired); product term FAIL (3.9e-16);
conjugation-closed Hermitian = EXACTLY paired (residual 0.0) FAIL; one-way half PASS.
KERNEL DISCRIMINATION LAW [ESTABLISHED machine]: reciprocity <=> mirror-paired kernel;
one-wayness <=> the unpaired half survives alone (one-wayness deletes the mirror partner).
STAGE 2: log(z-wbar) and primitive PASS the 2-field TARGET CORNER (CROSS-CONJUGATE,
cross-disc != 0, non-paired, transcendental, spatial carrier); traps all FAIL (paired
sum = the reciprocal continuum kernel, residual exactly 0). Registry #026 engraved.
REMAINING LOCK: exact continuum derivation for the spatial LG system (DRUM class
inherited, not derived) — next build: LG mode-sum with one-way weights -> closed form
-> judge. Measurability note stays [CONJECTURE] until then.
