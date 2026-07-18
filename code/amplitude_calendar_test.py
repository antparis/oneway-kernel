#!/usr/bin/env python3
# amplitude_calendar_test.py -- 2026-07-17
# Machine certification for registry entry candidate #061:
# AMPLITUDE vs CALENDAR -- decaying is not forgetting.
#
# Origin: seventh external adversarial audit (GPT-5.6) of paper v10. The
# paper's own uniform-measure closed form (the cardinal sine, Eq. (6))
# refutes the reading "absolutely continuous => the calendar is forgotten"
# stated in Sec. 4.3 and inherited from registry #049's wording: the
# AMPLITUDE tends to zero (Riemann-Lebesgue, which #049 machine-faced),
# but the ZEROS -- the deep rendezvous -- persist forever, and the window
# contrast equals 1 on every far window containing one.
#
# Claims faced (SymPy-exact + numeric far-window panels):
#   J1  Sinc closed form identity:
#       (e^{ibu}-e^{iau})/(iu(b-a)) == e^{i(a+b)u/2} * 2 sin((b-a)u/2)/(u(b-a)).
#   J2  Exact persistent zeros: |mu_unif(u_n)| == 0 at u_n = 2 pi n/(b-a),
#       for every integer n >= 1 -- an eternal calendar of minima.
#   J3  Window contrast C = (max-min)/(max+min) equals 1 exactly on any
#       window containing a zero and a nonzero point (min = 0), however
#       far; numeric face at n = 10^3 and 10^6 on [a,b] = [1/300, 1/3].
#   J4  A finitely supported non-null measure CANNOT decay: for N = 2,
#       |mu_hat| returns exactly to 1 (normalized) at every u_k =
#       2 pi k/Dnu -- limsup = 1, machine-exact.
#   J5  Independence: on the same far windows the sinc's MAXIMAL amplitude
#       decays ~ 1/u while its contrast stays 1 -- amplitude decay,
#       minima persistence and relative contrast are three separate
#       properties; neither "finitely supported" nor "absolutely
#       continuous" alone decides the last two.
#
# Scope: algebraic identities and window functionals of Fourier transforms
# of winding measures. Says nothing about nature.

import sympy as sp
import numpy as np

PASS = 0
FAIL = 0
def verdict(name, ok, detail=""):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok: PASS += 1
    else:  FAIL += 1
    print(f"[{tag}] {name}" + (f" -- {detail}" if detail else ""))

u = sp.Symbol('u', positive=True)
a, b = sp.symbols('a b', positive=True)
n, k = sp.symbols('n k', integer=True, positive=True)

# ---------------------------------------------------------------- J1
mu_unif = (sp.exp(sp.I*b*u) - sp.exp(sp.I*a*u))/(sp.I*u*(b - a))
sinc_form = sp.exp(sp.I*(a + b)*u/2) * 2*sp.sin((b - a)*u/2)/(u*(b - a))
res1 = sp.simplify(sp.expand_complex(mu_unif - sinc_form, deep=True))
res1 = sp.simplify(res1.rewrite(sp.sin))
verdict("J1 sinc closed-form identity", res1 == 0, f"residue = {res1}")

# ---------------------------------------------------------------- J2
u_n = 2*sp.pi*n/(b - a)
val = sp.simplify(sp.sin((b - a)*u_n/2))       # sin(pi n) == 0 exactly
verdict("J2 exact zeros at u_n = 2 pi n/(b-a) for all integer n",
        val == 0, f"sin((b-a)u_n/2) = {val}")

# ---------------------------------------------------------------- J3
# Symbolic core: min = 0 on any window containing a zero => contrast
# (max-0)/(max+0) = 1 whenever max > 0.
M = sp.Symbol('M', positive=True)
contrast = (M - 0)/(M + 0)
verdict("J3a contrast == 1 exactly whenever a window contains a zero",
        sp.simplify(contrast - 1) == 0)
# Numeric far-window face, [a,b] = [1/300, 1/3]
av, bv = 1/300, 1/3
L = bv - av
def relief(uu): return np.abs(2*np.sin(L*uu/2)/(uu*L))
ok3 = True
for nn in (10**3, 10**6):
    un = 2*np.pi*nn/L
    w = np.linspace(un - 30, un + 30, 200001)   # far window containing u_n
    r = relief(w)
    C = (r.max() - r.min())/(r.max() + r.min())
    print(f"      n = {nn:>7}: u_n = {un:.3e}, max relief = {r.max():.3e}, "
          f"min = {r.min():.3e}, contrast = {C:.12f}")
    ok3 = ok3 and abs(C - 1.0) < 1e-9
verdict("J3b far-window contrast == 1 at n = 10^3 and 10^6", ok3)

# ---------------------------------------------------------------- J4
w1, w2, Dnu = sp.symbols('w1 w2 Delta_nu', positive=True)
u_k = 2*sp.pi*k/Dnu
# normalized two-needle transform at the rendezvous u_k (global phase out)
val4 = sp.simplify(sp.Abs(w1 + w2*sp.exp(sp.I*Dnu*u_k))/(w1 + w2))
verdict("J4 finitely supported (N=2) returns to 1 at every u_k = 2 pi k/Dnu",
        val4 == 1, f"|mu_hat(u_k)| = {val4}")

# ---------------------------------------------------------------- J5
# On the same far windows: maximal amplitude decays ~ 1/u, contrast stays 1.
m1 = relief(np.linspace(2*np.pi*10**3/L - 30, 2*np.pi*10**3/L + 30, 200001)).max()
m2 = relief(np.linspace(2*np.pi*10**6/L - 30, 2*np.pi*10**6/L + 30, 200001)).max()
ratio = m1/m2
print(f"      max amplitude n=10^3 / n=10^6 = {ratio:.1f} (1/u predicts ~1000)")
verdict("J5 amplitude decays (~1/u) while contrast stays 1 on the same windows",
        800 < ratio < 1200)

# ---------------------------------------------------------------- summary
print("-" * 64)
print(f"RESULT: {PASS} PASS / {FAIL} FAIL out of {PASS + FAIL} clauses")
print("Reading (only if all PASS): DECAYING IS NOT FORGETTING. Riemann-")
print("Lebesgue kills the AMPLITUDE of an absolutely continuous transform;")
print("it controls neither the persistence of zeros, nor the positions of")
print("minima, nor the relative window contrast (the paper's own uniform")
print("sinc keeps an eternal calendar of exact zeros with contrast 1).")
print("A finitely supported non-null measure cannot decay (Bohr). The")
print("correct dichotomy is an AMPLITUDE dichotomy; calendar persistence")
print("is a separate property, decided by neither class alone.")
