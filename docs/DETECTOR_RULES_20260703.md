# DETECTOR RULES — consolidated 2026-07-03 (session #021–#027)

Date: 2026-07-03. Machine: ThinkCentre M920q, repo ~/Desktop/oxieml-star/.
Suggested MILO labels: eml_star, established, open
Purpose: SINGLE source for the detector criteria scattered across the session's seven
FINDINGS. Rules only — results live in the FINDINGS and IDEAS_REGISTRY (#001–#027).
Status tags in text only. Authority unchanged: machine execution + SymPy judge.

---

## 0. Authority chain (unchanged, binding)
Marker (PySR or any heuristic) != verdict. A claim is valid ONLY after execution on
Anthony's machine AND certification by judge_v2.py / verify_exact.py. MSE >= 1e-3
invalidates regardless of verdict. One judge patch per session, dated backup first.

## 1. ONE-POINT field gate (hardened battery) [ESTABLISHED]
A single 2D field f(z, zbar) is a target candidate iff ALL legs hold:
 L1  disc = d_z d_zbar log f != 0                (non-factorizable)      [#003]
 L2  NOT real-trapped MODULO GLOBAL PHASE: real-trapped iff full_conj(f) = c*f with
     |c| = 1 constant (full_conj = swap z<->zbar AND I->-I). The bare equality test
     misses mirrors-up-to-phase (z - zbar gave full_conj = -f).           [#021 fix]
 L3  scale-dependent winding                     (runs with radius)      [#003]
 L4  ANTI-NEEDLE EXISTENCE (judge-engraved #024, patch judge_v2 + backup 20260702):
     some NEGATIVE angular Fourier harmonic c_m != 0, m < 0 (FFT probe on circles,
     rel tol 1e-8). The anti needle must TURN. Module-dressed holomorphic decoys
     (all m >= 0) are killed here.
 L5  ANTI-NEEDLE ACTIVITY (numeric batteries, #023): winding NEGATIVE at some radius
     OR DECREASING across some radius (an anti-zero of index -1 is crossed).
     Relation: ACTIVITY (dominance) => EXISTENCE (turning), not conversely
     (z^2 + log(zbar) turns without ever dominating). L4 is the REQUIRED universal
     leg; L5 is a strong sufficient marker used in numeric-only batteries.
 Foundation of L4/L5 (argument principle): a HOLOMORPHIC field has winding >= 0 and
 NON-DECREASING in R (winding = #zeros inside). Hence "scale-dependent" ALONE is
 decoy-vulnerable: module-dressed z^4 + C reproduces a running 0->4 table with zero
 anti content.                                                            [#023]
 LIMIT of the one-point gate [ESTABLISHED #025]: it is FORCING-BLIND — it certifies
 STRUCTURE, not non-erasability. SPARC must include the PREPARATION axis: for a driven
 field, a licit drive (d = M@e1) erases the anti for ANY M => one-point driven
 snapshots are preparation-posed. The one-point target cell is structurally empty;
 the living target is TWO-POINT.

## 2. TWO-POINT kernel gate v2 [ESTABLISHED #026–#027]
For a transfer kernel K(z, zbar; w, wbar) (field 1 = observation point, field 2 =
source point), target-corner candidate iff ALL legs hold:
 K1  CROSS-ENTANGLED: d_a d_b log K != 0 for some cross pairing, tested on ALL FOUR
     pairings (z,w), (z,wbar), (zbar,w), (zbar,wbar) — a single-pairing test is
     incomplete (the derived one-way kernel lives on (zbar,wbar)). Numeric central
     finite differences on log K with INDEPENDENT variables (symbolic diff of
     undefined transcendentals cannot lambdify).                          [#027]
 K2  NON-PAIRED: full_conj_2f(K) != K (two-field mirror: swap both pairs + I->-I).
     The paired sum (half + mirror(half)) is exactly the RECIPROCAL kernel.  [#026]
 K3  EXCHANGE-NON-HERMITIAN (the one-wayness signature): K is reciprocal-compatible
     iff K = full_conj_2f(swap_points(K)) up to a CONSTANT — tested BRANCH-SAFE via
     constancy of exp(Delta) (a +-i*pi log-branch constant flips sign pointwise,
     raw spread ~ pi; exp(Delta) = -1 exposes it). One-wayness DELETES the mirror
     partner (K12 = 0): the unpaired half survives alone.                 [#027]
 K4  TRANSCENDENCE is a SEPARATE cube leg (master law), supplied by the physics
     (Jordan ladder -> Lerch/Li_2); flat weights give the algebraic corner (one-way
     but not the full target).                                            [#027]
 Forcing: a kernel depends on NO drive — the #025 preparation axis does not apply;
 non-erasability comes from the M level (Lindbladian one-way, licit-gauge tested #021).
 KERNEL DISCRIMINATION LAW: reciprocity <=> mirror-paired kernel; one-wayness <=>
 exchange-non-Hermiticity.

## 3. Decoys and pitfalls engraved this session (check EVERY future candidate against)
 P1  Holo/module decoy: running winding without negative/decreasing values
     (z^4 e^{-b zzbar} + C e^{-d zzbar}). Killed by L4/L5.                [#023]
 P2  Judge phase blind-spot: certify_1field exact-invariance misses mirror-up-to-
     global-phase (documented; L2 is the corrected test).                 [#021]
 P3  Far-detuned lineshape falls as Delta^-2 for ANY coupled 2x2 (resolvent
     off-diagonal): NON-discriminating for Jordan. Certificates = phase rigidity
     r -> 0 + secular linear growth (#020).                               [#025]
 P4  Non-conjugation-closed mode sets fake nonzero pairing residuals (truncation
     artifact); clean controls must be conjugation-closed.                [#026]
 P5  Judge adaptive winding grid can MISS narrow annuli (dense uniform grid caught a
     +1 Laguerre ring the adaptive grid missed).                          [#025]
 P6  Bergman reciprocal decoy: -k log(1 - z*wbar) (single-sector diagonal) is
     transcendental, cross-conjugate, non-paired — it PASSED the #026 formula gate;
     only K3 kills it.                                                    [#027]
 P7  Inherited-representative trap: log(z - wbar) (DRUM class) is exchange-Hermitian
     up to branch constant (exp(Delta) = -1) => reciprocal-compatible => WRONG
     one-way representative. Derive, do not inherit.                      [#027]
 P8  mpmath.taylor unstable on lerchphi (high-order FD): verify closed forms by
     PARTIAL SUMS (geometric tail bound), never by numeric Taylor.        [#027]
 P9  SPARC now has THREE axes: encoding (never re-encode real data), gauge/basis
     (licit similarities), and PREPARATION (drive/port choice).           [#025]

## 4. Judge-hardening queue [OPEN] (one patch per session, dated backup first)
 H1  Adaptive winding grid vs narrow annuli (P5).
 H2  Cross-field discriminant on all four pairings in judge_v2 (currently
     mixed_discriminant is intra-field only; 4-pairing version local in
     spatial_kernel_test.py / continuum_kernel_derivation.py).
 H3  Exchange-Hermiticity leg (K3, branch-safe exp(Delta)) as a judge tool.
 Already engraved in the judge: #024 negative-harmonic gate (backup
 judge_v2_backup_20260702.py; 15/15 battery unchanged).

## 5. Trace files (rules sources)
FINDINGS_20260702_awake_defective_pair.md, FINDINGS_20260702_m3_bec_vortex.md,
FINDINGS_20260702_gate_hardening.md, FINDINGS_20260702_neg_harmonic_gate.md,
FINDINGS_20260702_driven_response.md, FINDINGS_20260703_spatial_kernel.md,
FINDINGS_20260703_continuum_kernel_derivation.md. Registry #001–#027.
KICKOFF_20260703.md (+ addendum) = session-restart block.
