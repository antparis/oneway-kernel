# FINDINGS 2026-07-14 — Comparative cut-phase witness (#057): #055 open flag CLOSED

Status: [ESTABLISHED machine + judge]. Executed on Anthony's ThinkCentre M920q,
2026-07-14. Numeric harness 10/10, SymPy exact judge 8/8. Sandbox-identical.

## Broken parameter (orthogonal axis, announced before the run)
#040 held fixed: "the rotating jump phase is read on ONE sector". #055 showed
this is a false positive: C1 = F_a(X) + F_a(Y) is strictly reciprocal (R = 0)
yet BOTH sectors carry the rotating cut phase. Broken here: the witness becomes
COMPARATIVE -- W(x) = D_X(x) - D_Y(x), the complex difference of the two
sector jumps.

## Law
W != 0  =>  R != 0   (the witness is SUFFICIENT)
W == 0  =>  INCONCLUSIVE   (never a proof of reciprocity)
Master invariant stays R = K - S(K) (#055/#056).

## Machine (kernel_comparative_witness_test.py, sha256 19c9d42a)
A  per-sector law SURVIVES on C1: both sectors drift at d(arg)/d(ln x) = +nu,
   |slope - nu| = 2.36e-16 (the #040 identity is intact PER SECTOR).
B  witness W on six kernels:
     K_ow  (one-way, partner absent)  max|W| = 2.311e+00  FIRES
     C1    (reciprocal, both rotate)  max|W| = 0.000e+00  REFUSES  <- the repair
     C_rec (reciprocal dilog, frozen) max|W| = 0.000e+00  REFUSES
     K_rho (size asymmetry, rho=2)    max|W| = 2.311e+00  FIRES (SIZE column)
     K_det (speed asymmetry, 3nu)     max|W| = 6.482e-01  FIRES (SPEED column)
     K_eps (entire antisym, R != 0)   max|W| = 0.000e+00  silent -> THE LIMIT
C  ground truth R: R(C1) = 0.00e+00 exactly; R != 0 on K_ow/K_rho/K_det/K_eps.
D  SIZES LEDGER, exact: max|W| = |1 - rho| * |D|, |diff| = 0.00e+00 at
   rho = 0.5 / 1.0 / 2.0. Amplitude asymmetry is read by W and MISSED by any
   phase-only comparison (K_rho has identical phase and slope in both sectors).
E  numeric control (a=1 dilog, standard branch): rel. err 3.6e-13 / 1.8e-25 /
   6.7e-14 at x = 1.5 / 2.0 / 3.0.

## Judge (judge_witness_056.py, sha256 3e65f4f3, SymPy exact, 8/8)
J1a  C1: W = D_X - D_Y == 0 IDENTICALLY (residue 0, symbolic -- not numeric).
J1b  per-sector rotation x**(I*nu) = exp(I*nu*ln x), residue 0 (drift = +nu).
J2a  K_ow: W == D_X (partner sector absent), residue 0.
J2b  K_ow: W != 0 (x=2, nu=1/10).
J3a  K_eps: the entire antisymmetric part eps*(X-Y) has ZERO discontinuity
     across the cut -- it contributes nothing to W.
J3b  K_eps: R = 2*eps*(X-Y) != 0. Hence W = 0 while R != 0: THE INCONCLUSIVE
     LIMIT, graved before the run, confirmed exactly.
J4a  R(C1) == 0 exactly.  J4b  R(K_rho) == (1-rho)*(F(X)-F(Y)).

## Grand ledger (sizes and speeds)
Both columns are load-bearing: K_rho fires on SIZE alone (same speed, same
phase) and K_det fires on SPEED alone. A phase-only witness reads neither --
this is why the repaired witness must be a COMPLEX difference of jumps.

## Nuance traced (not a debt)
Panel C |R| magnitudes are mpmath-precision-sensitive on complex lerchphi
arguments (sandbox 0.938/0.148 vs machine 1.396/2.109 for K_ow/K_det). No claim
rests on these magnitudes: only the SIGN (R = 0 vs R != 0) is used, identical
in both runs. The a=1 dilog control (Panel E) is the branch-safe check, per the
#040 lesson (mpmath lerchphi is branch-smooth on x>1 -- never probe the cut on
it directly).

## SymPy lesson graved (operational)
A two-variable SWAP must use subs(..., simultaneous=True). Sequential
subs({X: Y, Y: X}) collapses the exchange to 0 and silently fakes reciprocity.
Same family as the .conjugate() trap. Caught in sandbox.

## What this does NOT do
No novelty claim. No physical claim. Does not touch the sealed v3 (Zenodo
10.5281/zenodo.21317960); the repair belongs to the NEXT linked deposit. Does
not touch the size-cone question (ASYM positivity, #052) -- separate chantier,
still open.

Traces: kernel_comparative_witness_test.py, judge_witness_056.py,
IDEAS_REGISTRY.md #057, DETECTOR_RULES_20260703.md section 6 (#056 errata).

## Orthogonal-axis pass ON THIS FINDINGS (post-run, mandatory reflex)
Parameter this harness itself held fixed WITHOUT questioning it: the SEPARABLE
class K(X,Y) = F(X) + G(Y). All six kernels tested live inside it. Consequence:
#057 is [ESTABLISHED] IN THE SEPARABLE CALIBRATED CLASS ONLY. Outside it, a
kernel has no cleanly defined "two sectors" and D_X / D_Y may not exist
separately -- the witness is NOT established there, and no claim is made.
Second axis not broken: the NUMBER of sectors (fixed at two). W = D_X - D_Y is
a binary difference; a K-sector kernel would need a family of differences (or a
matrix of them). Unexplored, traced.
Both are OPEN, and both must be faced before the witness enters any deposit.
