#!/usr/bin/env python3
# calendar_weights_test.py -- 2026-07-17
# Machine certification for registry entry candidate #060:
# CALENDAR vs WEIGHTS refinement (grand-ledger law made exact).
#
# Claims faced (all SymPy-exact, no hardcoded verdict):
#   J1  Three-needle identity: |1 + a e^{iu} + e^{2iu}| = |a + 2 cos u|.
#   J2  For 0 < a < 2 the interior deep minimum sits at u* = arccos(-a/2):
#       P(u*) = 0 exactly, and du*/da > 0 -- THE POSITIONS OF THE DEEP
#       MINIMA DEPEND ON THE POSITIVE WEIGHTS for N >= 3.
#       (Refutes any unscoped "positive weights freeze the positions".)
#   J3  Two-needle law: P^2 = w1^2 + w2^2 + 2 w1 w2 cos(Dnu*u + Dphi);
#       minima exactly at u_n = ((2n+1)pi - Dphi)/Dnu, so a relative
#       phase TRANSLATES the minima by MINUS Dphi/Dnu, and for positive
#       w1, w2 the POSITIONS are weight-independent at N = 2 (only the
#       depth |w1 - w2| moves).
#   J4  A COMMON positive rescaling w -> c*w leaves the normalized
#       relief P/sum(w) exactly invariant (the true scope of the old
#       "volume knob / frozen positions" wording: common, not relative).
#
# Context: external audit (GPT-5.6) of paper v8 produced the three-needle
# counter-example; sandbox reproduced it; this harness is the machine
# arbiter. Scope: algebraic identities on finite phasor sums; says
# nothing about nature.

import sympy as sp

PASS = 0
FAIL = 0
def verdict(name, ok, detail=""):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok: PASS += 1
    else:  FAIL += 1
    print(f"[{tag}] {name}" + (f" -- {detail}" if detail else ""))

u = sp.Symbol('u', real=True)
a = sp.Symbol('a', positive=True)

# ---------------------------------------------------------------- J1
P2 = sp.expand_trig(sp.expand(
    (1 + a*sp.cos(u) + sp.cos(2*u))**2 + (a*sp.sin(u) + sp.sin(2*u))**2))
Q2 = sp.expand_trig(sp.expand((a + 2*sp.cos(u))**2))
res1 = sp.simplify(P2 - Q2)
verdict("J1 three-needle identity |1+a e^iu+e^2iu|^2 == (a+2cos u)^2",
        res1 == 0, f"residue = {res1}")

# ---------------------------------------------------------------- J2
ustar = sp.acos(-a/2)                      # interior zero for 0 < a < 2
Pmin = sp.simplify((a + 2*sp.cos(ustar)))
dustar_da = sp.simplify(sp.diff(ustar, a))
# du*/da = 1/(2 sqrt(1 - a^2/4)) > 0 on 0 < a < 2
pos = sp.simplify(dustar_da - 1/(2*sp.sqrt(1 - a**2/4)))
verdict("J2a interior minimum value P(u*) == 0 exactly",
        Pmin == 0, f"P(u*) = {Pmin}")
verdict("J2b du*/da == 1/(2 sqrt(1-a^2/4)) > 0 (position MOVES with a)",
        pos == 0, f"closed form residue = {pos}")
# numeric face, three alphas
import math
for aval in (sp.Rational(1,2), 1, sp.Rational(3,2)):
    print(f"      a = {aval}:  u* = arccos(-a/2) = {float(sp.acos(-aval/2)):.6f}")

# ---------------------------------------------------------------- J3
w1, w2, Dphi, Dnu = sp.symbols('w1 w2 Delta_phi Delta_nu', positive=True)
n = sp.Symbol('n', integer=True)
P2two = sp.expand_trig(sp.expand(
    (w1 + w2*sp.cos(Dnu*u + Dphi))**2 + (w2*sp.sin(Dnu*u + Dphi))**2))
target = w1**2 + w2**2 + 2*w1*w2*sp.cos(Dnu*u + Dphi)
res3 = sp.simplify(P2two - target)
verdict("J3a two-needle modulus law P^2 == w1^2+w2^2+2w1w2 cos(Dnu u+Dphi)",
        res3 == 0, f"residue = {res3}")
u_n = ((2*n + 1)*sp.pi - Dphi)/Dnu
at_min = sp.simplify(sp.cos(Dnu*u_n + Dphi))     # must be -1 exactly
verdict("J3b minima exactly at u_n = ((2n+1)pi - Dphi)/Dnu (cos == -1)",
        at_min == -1, f"cos at u_n = {at_min}")
# shift w.r.t. Dphi: du_n/dDphi = -1/Dnu  (MINUS sign of the translation law)
shift = sp.simplify(sp.diff(u_n, Dphi) + 1/Dnu)
verdict("J3c translation sign: du_n/dDphi == -1/Dnu (shift = MINUS Dphi/Dnu)",
        shift == 0, f"residue = {shift}")
# positions independent of positive w1, w2 at N = 2
indep = (sp.diff(u_n, w1) == 0) and (sp.diff(u_n, w2) == 0)
verdict("J3d N=2 minima positions independent of positive weights", indep)

# ---------------------------------------------------------------- J4
c = sp.Symbol('c', positive=True)
w3 = sp.Symbol('w3', positive=True)
nu1, nu2, nu3 = sp.symbols('nu1 nu2 nu3', real=True)
S  = w1*sp.exp(sp.I*nu1*u) + w2*sp.exp(sp.I*nu2*u) + w3*sp.exp(sp.I*nu3*u)
norm_orig = sp.Abs(S)/(w1 + w2 + w3)
norm_resc = sp.Abs(c*S)/(c*(w1 + w2 + w3))
res4 = sp.simplify(norm_resc - norm_orig)
verdict("J4 common positive rescaling leaves normalized relief invariant",
        res4 == 0, f"residue = {res4}")

# ---------------------------------------------------------------- summary
print("-" * 64)
print(f"RESULT: {PASS} PASS / {FAIL} FAIL out of {PASS + FAIL} clauses")
print("Reading (only if all PASS): speeds fix the frequency group;")
print("moduli AND angles fix depth, selection and POSITION of the deep")
print("rendezvous for N >= 3; at N = 2 positions are weight-independent")
print("and translate by MINUS Dphi/Dnu under a relative phase; a COMMON")
print("positive rescaling is the only guaranteed pure volume knob.")
