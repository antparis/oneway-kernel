# FINDINGS 2026-07-17 -- #060 CALENDAR vs WEIGHTS: positive weights move the deep minima (N >= 3); the only guaranteed volume knob is the COMMON rescaling

Status: [ESTABLISHED machine + judge] -- SymPy-exact harness, 8/8 on
Anthony's machine (ThinkCentre, 2026-07-17). The harness IS the judge
(exact symbolic residues, no hardcoded verdict).

## Origin
External adversarial audit (GPT-5.6) of paper v8 produced a three-needle
counter-example against two related wordings: (i) v7 l.527-529 "positive
real rescalings ... minima keep their positions"; (ii) the v8 3f repair
"calendar independent of the weight family among real positive weights".
Sandbox reproduced the counter-example; this machine run is the arbiter.

## What was tested (calendar_weights_test.py, sha256 bb9371cd19ff2dfe
2631ab8f16dfb52d90af6fce134f80665663c25a8226099e)
- J1  |1 + a e^{iu} + e^{2iu}| == |a + 2 cos u|  (exact identity).
- J2  Interior deep minimum at u* = arccos(-a/2): P(u*) == 0 exactly and
      du*/da == 1/(2 sqrt(1 - a^2/4)) > 0  -- the POSITION of the deep
      minimum strictly MOVES with the positive weight a (N = 3).
- J3  Two-needle law P^2 == w1^2 + w2^2 + 2 w1 w2 cos(Dnu u + Dphi);
      minima exactly at u_n = ((2n+1)pi - Dphi)/Dnu; translation under a
      relative phase = MINUS Dphi/Dnu (sign certified); positions
      independent of positive w1, w2 at N = 2.
- J4  A COMMON positive rescaling w -> c w leaves the normalized relief
      P/sum(w) exactly invariant.

## Exact command
    cd ~/Desktop/oxieml-star && python3 calendar_weights_test.py

## Raw result
    8 PASS / 0 FAIL (all residues exactly 0; u* = 1.823477 / 2.094395 /
    2.418858 at a = 1/2, 1, 3/2).

## Law graved (grand-ledger refinement, now machine-faced)
SPEEDS fix the frequency group of the relief; MODULI AND ANGLES fix
depth, selection AND POSITION of the deep rendezvous for N >= 3. At
N = 2 the positions are weight-independent (positive weights) and a
relative phase translates them by MINUS Dphi/Dnu. The only guaranteed
pure volume knob is the COMMON positive rescaling (J4); relative
positive changes generally move the minima from N >= 3 on (J2).

## Semantic debt traced (append-only; originals untouched)
- #042 wording "positive real rescaling = volume knob, positions frozen"
  holds for the COMMON rescaling only; unscoped readings are superseded
  by this entry.
- Paper v7 l.527-529 and the v8 "3f" repair both carry the unscoped
  claim; both are rewritten in v9 (build_v9.py).

## Credit
Counter-example: external adversarial audit (GPT-5.6, fifth round).
Reproduction: Cowork sandbox. Arbitration: Anthony's machine.

## Scope
Algebraic identities on finite phasor sums along the one-way cut.
Says nothing about nature. Shared FORM, never identity.
