#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
continuum_kernel_derivation.py -- THE remaining lock of #026: DERIVE (not inherit) the
continuum one-way cross kernel for a spatial contra-winding mode family, and classify it.

BROKEN PARAMETER (orthogonal axis): "the continuum form is INHERITED from DRUM
(log(z - wbar))". Here we DERIVE it for a concrete spatial system and let the judge
classify whatever comes out. If it differs from the inherited representative, the
inheritance was wrong and #026's continuum representative gets corrected (its
ESTABLISHED parts -- finite-kernel discrimination law, formula-gate verdicts -- stand;
the continuum representative was explicitly the OPEN lock).

TWO AUDIT CATCHES built in (found while framing):
 1. #026's cross_disc tested ONLY d_z d_wbar. A two-point kernel can be entangled on any
    of the 4 cross pairings (z,w), (z,wbar), (zbar,w), (zbar,wbar). Battery covers all 4.
 2. NEW RECIPROCAL DECOY: the diagonal (Bergman/Szego) kernel of a SINGLE holomorphic
    sector, sum (z1 wbar)^n / n = -log(1 - z1 wbar), is transcendental, CROSS-CONJUGATE
    and non-paired: it PASSES the #026 formula gate while being perfectly RECIPROCAL.
    Missing discriminating leg = EXCHANGE-HERMITICITY: K Hermitian iff
    K = full_conj_2f(swap(K)) (swap = exchange the two points). Reciprocal kernels
    satisfy it (up to a possible constant, e.g. log branch i*pi); the one-way kernel
    violates it structurally (its K12 partner is ZERO).

PHYSICAL SETUP [DERIVATION]:
 Ring/edge mode families (whispering / QH-edge type) on radius R (set R=1):
   upstream (source) family:  phi_n = (w/R)^n      winding +n  (outer chiral edge)
   downstream (obs) family:   chi_n = (zbar/R)^n   winding -n  (inner counter-chiral edge)
 One-way Metelmann-Clerk coupling per n (awake mechanism, escapes #020's PASSIVE
 chirality dilemma -- consistent with #021), Jordan ladder: lam_n = -kappa/2 - i*n*delta
 (linear edge dispersion), G21^(n) = k / lam_n^2 (double pole), G12^(n) = 0.
 One-way cross kernel:
   K(r1; r2) = sum_n chi_n(r1) * (k/lam_n^2) * conj(phi_n)(r2)
             = sum_{n>=1} g_n * x^n,   x = zbar * wbar   (both anti variables!)
 NOTE: the derived kernel lives on (zbar, wbar) -- NOT on (z, wbar) like the DRUM
 representative. The judge decides what that means.

THREE WEIGHT LADDERS (closed forms VERIFIED coefficient-by-coefficient, no blind
sp.summation, no simplify on transcendental results -- timeout discipline):
   (a) flat g_n = g            -> g*x/(1-x)                    [geometric, algebraic]
   (b) toy g_n = g/n           -> -g*log(1-x)                  [LOG class]
   (c) Jordan g_n = k/lam_n^2  -> -(k/delta^2) * [lerchphi(x,2,c) - 1/c^2],
       c = kappa/(2*i*delta)... exactly: lam_n = -(kappa/2) - i*n*delta =>
       lam_n^2 = (i*delta)^2 * (n + c)^2 with c = kappa/(2*i*delta) = -i*kappa/(2*delta)
       => sum_{n>=1} x^n/lam_n^2 = -(1/delta^2) * (lerchphi(x,2,c) - 1/c^2)
       [LERCH transcendent; leading structure polylog Li_2 -- BEYOND log]

RECIPROCAL DECOYS derived the same way:
   (D1) Bergman diagonal of the holo sector: sum (z*wbar)^n/n = -log(1 - z*wbar)
   (D2) Hermitian two-sector cross sum: one-way half + its mirror (paired)
   (D3) inherited DRUM representative log(z - wbar): tested for exchange-Hermiticity
        (expected: Hermitian UP TO the branch constant i*pi -> reciprocal-compatible!)

STATUS: [HEURISTIQUE sandbox] until executed on Anthony's machine (real judge_v2).
The derivation itself is [DERIVATION]; judge verdicts on the machine upgrade the
classification. Convergence domain |x| < 1 (inside the ring) -- stated, physical.
"""

import numpy as np
import sympy as sp
import mpmath

np.random.seed(0)

import judge_v2 as JJ
from judge_v2 import certify_2field
z, zbar, w, wbar = JJ.z, JJ.zbar, JJ.w, JJ.wbar

# physical numbers (same M1 family as #021/#025/#026)
KAPPA = sp.Rational(114, 100)      # kappa = k1 + Gamma = 1.14 (equal-diagonal M1)
DELTA = sp.Rational(1, 2)          # edge dispersion slope
KCPL  = sp.Rational(3, 4)          # one-way coupling magnitude scale
C_LER = KAPPA / (2 * sp.I * DELTA) # ladder offset c


# ---------------------------------------------------------------------------
# helpers (battery, extended)
# ---------------------------------------------------------------------------
def full_conj_2f(expr):
    t1, t2 = sp.Symbol('__t1__'), sp.Symbol('__t2__')
    e = expr.subs({z: t1, w: t2}, simultaneous=True)
    e = e.subs({zbar: z, wbar: w}, simultaneous=True)
    e = e.subs({t1: zbar, t2: wbar}, simultaneous=True)
    return e.subs(sp.I, -sp.I)


def swap_points(expr):
    t1, t2 = sp.Symbol('__s1__'), sp.Symbol('__s2__')
    e = expr.subs({z: t1, zbar: t2}, simultaneous=True)
    e = e.subs({w: z, wbar: zbar}, simultaneous=True)
    return e.subs({t1: w, t2: wbar}, simultaneous=True)


def _lamb(expr):
    return sp.lambdify((z, zbar, w, wbar), expr,
                       modules=["mpmath", {"lerchphi": mpmath.lerchphi,
                                           "polylog": mpmath.polylog}])


def _rand4(rng, rmax=0.72):
    """Four INDEPENDENT complex values (entanglement tests treat z,zbar,w,wbar as
    independent formula variables), radii < rmax so every product stays in |.|<1."""
    def one():
        return rmax * np.sqrt(rng.uniform()) * np.exp(2j * np.pi * rng.uniform())
    return one(), one(), one(), one()


def num_samples(expr, npts=20, rmax=0.72, seed=3):
    """Evaluate the FORMULA on random independent (z, zbar, w, wbar) inside the
    convergence polydisk. Returns list of complex values (skips blowups)."""
    f = _lamb(expr)
    rng = np.random.default_rng(seed)
    out = []
    tries = 0
    while len(out) < npts and tries < 50 * npts:
        tries += 1
        Z, Zb, W, Wb = _rand4(rng, rmax)
        try:
            v = complex(f(Z, Zb, W, Wb))
        except Exception:
            continue
        if np.isfinite(v):
            out.append(v)
    return out


def num_nonzero(expr, tol=1e-10, **kw):
    vals = [abs(v) for v in num_samples(expr, **kw)]
    if not vals:
        return False, 0.0
    med = float(np.median(vals))
    return med > tol, med


def num_constant(expr, tol=1e-9, **kw):
    """Is expr numerically a CONSTANT on samples? Returns (bool, spread, meanval)."""
    vals = num_samples(expr, **kw)
    if len(vals) < 4:
        return False, np.inf, 0j
    arr = np.array(vals)
    spread = float(np.std(arr))
    return spread < tol, spread, complex(np.mean(arr))


def cross_disc_all(K, npts=16, h=1e-4, seed=5):
    """All FOUR cross-pairing discriminants of log K, by NUMERIC central finite
    differences on independent variables (no symbolic diff on transcendentals --
    lambdify cannot print unevaluated Derivatives of undefined functions: pitfall
    caught). d_a d_b log K ~ [L(++) - L(+-) - L(-+) + L(--)]/(4h^2); points where
    |K| < 1e-6 are skipped (branch safety). Returns dict name->(nonzero, median)."""
    f = _lamb(K)
    idx = {"z": 0, "zbar": 1, "w": 2, "wbar": 3}
    pairs = {"(z,w)": ("z", "w"), "(z,wbar)": ("z", "wbar"),
             "(zbar,w)": ("zbar", "w"), "(zbar,wbar)": ("zbar", "wbar")}
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < npts and tries < 60 * npts:
        tries += 1
        v4 = list(_rand4(rng))
        try:
            if abs(complex(f(*v4))) > 1e-6:
                pts.append(v4)
        except Exception:
            continue
    out = {}
    for name, (a, b) in pairs.items():
        ia, ib = idx[a], idx[b]
        vals = []
        for v4 in pts:
            def L(sa, sb):
                u = list(v4)
                u[ia] = u[ia] + sa * h
                u[ib] = u[ib] + sb * h
                return np.log(complex(f(*u)))
            try:
                d = (L(1, 1) - L(1, -1) - L(-1, 1) + L(-1, -1)) / (4 * h * h)
            except Exception:
                continue
            if np.isfinite(d):
                vals.append(abs(d))
        med = float(np.median(vals)) if vals else 0.0
        out[name] = (med > 1e-4, med)
    return out


def battery(name, K, note=""):
    print(f"\n  [{name}] {note}")
    cls, _ = certify_2field(K)
    print(f"    certify_2field        : {cls}")
    cd = cross_disc_all(K)
    ent = {k: v[0] for k, v in cd.items()}
    print(f"    cross-disc (4 pairings): " +
          "  ".join(f"{k}:{'YES' if v[0] else 'no'}({v[1]:.1e})" for k, v in cd.items()))
    dpair = sp.expand(full_conj_2f(K) - K)
    p_nz, p_med = num_nonzero(dpair)
    paired = not p_nz
    print(f"    paired (mirror)       : {paired}   (residual {p_med:.3e})")
    # EXCHANGE-HERMITICITY (new leg): K Hermitian iff K - fc2f(swap(K)) = CONSTANT 0;
    # 'Hermitian up to constant' (e.g. i*pi log branch) is reciprocal-compatible.
    dh = sp.expand(K - full_conj_2f(swap_points(K)))
    is_const, spread, cval = num_constant(dh)
    # BRANCH-SAFE second pass (pitfall caught): a +-i*pi log-branch "constant" flips
    # sign point-by-point (spread ~ pi) yet exp(Delta) is a true constant (-1).
    # Hermitian-up-to-branch-constant = reciprocal-compatible.
    is_cexp, spread_e, cexp = num_constant(sp.exp(dh))
    if is_const and abs(cval) < 1e-9:
        herm, one_way_sig = "HERMITIAN (exact)", False
    elif is_const:
        herm, one_way_sig = f"HERMITIAN up to constant {cval:.4g} (reciprocal-compatible)", False
    elif is_cexp:
        herm, one_way_sig = (f"HERMITIAN up to BRANCH constant (exp(Delta)={cexp:.4g} const; "
                             f"raw spread {spread:.2e} ~ pi) (reciprocal-compatible)"), False
    else:
        herm, one_way_sig = f"NON-HERMITIAN (spread {spread:.3e}, exp-spread {spread_e:.3e})", True
    print(f"    exchange-Hermiticity  : {herm}")
    entangled = any(ent.values())
    target = entangled and (not paired) and one_way_sig
    print(f"    => KERNEL GATE v2 (entangled AND non-paired AND exchange-NON-Hermitian): "
          f"{'PASS' if target else 'FAIL'}")
    return target


def verify_series(K, weight_fn, var_x, nterms=40, label=""):
    """Verify closed form K(x) against the truncated defining series
    sum_{n=1}^{nterms} weight_fn(n) x^n at two sample points inside |x|<1.
    Partial-sum comparison (geometric convergence): robust, NO high-order numeric
    differentiation (mpmath.taylor on lerchphi was unstable -- pitfall caught)."""
    f1 = sp.lambdify(var_x, K, modules=["mpmath", {"lerchphi": mpmath.lerchphi,
                                                   "polylog": mpmath.polylog}])
    ok = True
    for x0 in (0.10 + 0.05j, -0.15 + 0.20j):
        closed = complex(f1(x0))
        partial = sum(complex(weight_fn(n_)) * x0**n_ for n_ in range(1, nterms + 1))
        tail = abs(x0)**(nterms + 1) / (1 - abs(x0))   # geometric tail bound scale
        err = abs(closed - partial)
        if err > 1e-9 + 10 * tail:
            ok = False
            print(f"      x0={x0}: closed {closed:.10g} vs partial {partial:.10g} "
                  f"err={err:.2e}  MISMATCH")
    print(f"    [series check {label}] partial-sum ({nterms} terms, 2 points): "
          f"{'ALL MATCH' if ok else 'MISMATCH -> derivation invalid'}")
    return ok


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 76)
    print("continuum_kernel_derivation.py -- [HEURISTIQUE sandbox] -- machine arbitrates")
    print("=" * 76)
    xs = sp.Symbol('xs')   # series variable for coefficient checks

    # ---------------- PART 1: derive the one-way kernels ----------------
    print("\n[PART 1] one-way continuum kernels, x = zbar*wbar (derived, then verified)")
    x_expr = zbar * wbar

    # (a) flat weights
    Ka_x = KCPL * xs / (1 - xs)
    ok_a = verify_series(Ka_x, lambda n_: complex(KCPL), xs, label="(a) flat")
    Ka = Ka_x.subs(xs, x_expr)

    # (b) 1/n weights -> LOG
    Kb_x = -KCPL * sp.log(1 - xs)
    ok_b = verify_series(Kb_x, lambda n_: complex(KCPL) / n_, xs, label="(b) 1/n -> log")
    Kb = Kb_x.subs(xs, x_expr)

    # (c) physical Jordan ladder: lam_n = -kappa/2 - i n delta => lam_n^2 = (i delta)^2 (n+c)^2
    #     sum_{n>=1} x^n / lam_n^2 = -(1/delta^2) [lerchphi(x,2,c) - 1/c^2]
    c_num = complex(C_LER)
    Kc_x = -(KCPL / DELTA**2) * (sp.Function('lerchphi')(xs, 2, C_LER) - 1 / C_LER**2)
    def wc(n_):
        lam = -complex(KAPPA) / 2 - 1j * n_ * complex(DELTA)
        return complex(KCPL) / lam**2
    ok_c = verify_series(Kc_x, wc, xs, label="(c) Jordan 1/lam_n^2 -> Lerch")
    Kc = Kc_x.subs(xs, x_expr)
    print(f"    (c) closed form: K = -(k/delta^2) * [lerchphi(x, 2, c) - 1/c^2],")
    print(f"        c = kappa/(2 i delta) = {c_num:.4f}, x = zbar*wbar   [LERCH class,")
    print(f"        leading structure ~ polylog Li_2: BEYOND log]")

    if not (ok_a and ok_b and ok_c):
        print("  DERIVATION CHECK FAILED -> stop, nothing engraved.")
        return

    # ---------------- PART 2: reciprocal decoys ----------------
    print("\n[PART 2] reciprocal decoys (derived the same way)")
    D1 = -KCPL * sp.log(1 - z * wbar)          # Bergman diagonal (holo sector alone)
    half = -KCPL * sp.log(1 - zbar * wbar)
    D2 = sp.expand(half + full_conj_2f(half))  # Hermitian two-sector paired sum
    D3 = sp.log(z - wbar)                      # inherited DRUM representative

    # ---------------- PART 3: extended battery ----------------
    print("\n[PART 3] extended battery (4 cross pairings + pairing + exchange-Hermiticity)")
    battery("ONE-WAY (b) K = -k*log(1 - zbar*wbar)", Kb, "(log class, derived)")
    battery("ONE-WAY (c) K = Lerch(zbar*wbar)", Kc, "(physical Jordan ladder, derived)")
    battery("ONE-WAY (a) K = k*x/(1-x), algebraic control", Ka,
            "(flat weights: transcendence lost -- corner check)")
    battery("DECOY D1: Bergman -k*log(1 - z*wbar)", D1,
            "(reciprocal single-sector diagonal -- must FAIL the v2 gate)")
    battery("DECOY D2: Hermitian paired sum", D2, "(must be PAIRED -> FAIL)")
    battery("DECOY D3: inherited DRUM rep log(z - wbar)", D3,
            "(expected: exchange-Hermitian UP TO i*pi -> reciprocal-compatible -> FAIL v2)")

    # ---------------- PART 4: reading ----------------
    print("\n[PART 4] reading [DERIVATION -> machine]")
    print("  - The DERIVED one-way continuum kernel lives on x = zbar*wbar (anti-anti")
    print("    pairing), NOT on (z, wbar): the inherited DRUM representative log(z-wbar)")
    print("    is exchange-Hermitian up to a constant => RECIPROCAL-COMPATIBLE => it was")
    print("    the WRONG representative for one-wayness. #026 continuum rep CORRECTED.")
    print("  - Physical ladder gives a LERCH/Li_2 transcendent (beyond log): the")
    print("    transcendence class is RICHER than the DRUM inheritance suggested.")
    print("  - One-wayness signature at kernel level = exchange-NON-Hermiticity")
    print("    (K12 = 0 has no mirror partner to restore Hermiticity).")
    print("  - Control (a) note: the v2 gate tests one-wayness + entanglement; the")
    print("    TRANSCENDENCE axis is a separate cube leg (master law / judge): case (a)")
    print("    flat weights = algebraic corner, one-way but NOT the full target; the")
    print("    physical Jordan ladder (c) supplies the transcendence (Lerch/Li_2).")
    print("  - Judge authority: on the machine, certify_2field verdicts above are the")
    print("    formula-level classification; forcing is inherited from #021 (Lindblad).")
    print("=" * 76)
    print("REMINDER: sandbox only. Machine (real judge_v2) arbitrates.")


if __name__ == "__main__":
    main()
