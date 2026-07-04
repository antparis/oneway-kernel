#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spatial_kernel_test.py -- the identified object of #025: the TWO-POINT transfer kernel
of the Jordan M1 one-way coupling, on SPATIAL LG carriers.

WHY THIS OBJECT (from #025 [ESTABLISHED machine]): the driven FIELD is preparation-posed
(a licit drive erases the anti). A transfer KERNEL depends on NO drive -- it IS the
structure of M (one-wayness G12=0 + double pole G21 ~ k/lambda^2, non-erasable per #021
GATE A). The #025 erasure axis does not exist for a kernel. The DRUM session had already
certified the continuum cross-kernel class log(z1 - zbar2) as target-type; DRUM died ONLY
on spatial_carrier (temporal exponent). Here the carriers are spatial LG modes: the 7th
condition is satisfied by construction.

BROKEN PARAMETER (orthogonal axis): "the object is a ONE-point field". Broken: two-point
kernel K(z, zbar; w, wbar), field 1 = observation point, field 2 = source point.
TOOLING GAP CAUGHT: judge_v2.mixed_discriminant tests d2/dz dzbar (INTRA-field 1);
the decisive entanglement for a two-point kernel is CROSS-FIELD: d_z d_wbar log K.
Implemented locally here (no judge patch this session -- #024 consumed it).

CUBE POSITION (2-field): target corner = non-paired x transcendental x non-factorizable
(cross-disc != 0), with spatial carrier. Candidate: continuum class log(z - wbar).

STAGES
  1. FINITE 2-mode kernel  K2 = -(1/lam)[m1 m1* + m2 m2*] + (k/lam^2) m2 m1*
     (m1 = LG(+1,0), m2 = LG(-1,1); Jordan numbers from awake_defective_pair M_target).
     Sum of separable terms: is the SUM cross-entangled (law #004, two-field side)?
     Controls: single product term (must be cross-separable = wall);
               reciprocal/Hermitian kernel (both cross terms) -- comparison;
               pairing test full_conj_2f (z<->zbar AND w<->wbar AND I->-I).
  2. CONTINUUM class representative [DERIVATION, from the DRUM derivation]:
     K = log(z - wbar)  (and the primitive (z-wbar)*(log(z-wbar)-1)).
     Tests: certify_2field class; cross-disc; rephasing_test; pairing.
     Historical-trap controls: log(z-w) (holo-holo wall); the PAIRED sum
     log(z-wbar)+log(zbar-w) (the "transcendant apparie" trap -> must be real-trapped
     under full_conj_2f); product log(z)*log(wbar) (cross-separable wall).

TIMEOUT DISCIPLINE: no sp.simplify on large log expressions (lived 9h freeze case);
nonzero checks are done NUMERICALLY on random sample points; symbolic diff only.

STATUS: [HEURISTIQUE sandbox] until executed on Anthony's machine with the real judge_v2.
SPARC note (to verify, not assume): the kernel is drive-independent; the one-wayness is
Lindbladian (#021, non-erasable by licit gauge diag(s,1/s)); remaining SPARC axis =
mode-basis choice, covariant per #021 GATE A. spatial_carrier: LG plane = spatial.
"""

import numpy as np
import sympy as sp

np.random.seed(0)

import judge_v2 as JJ
from judge_v2 import certify_2field, rephasing_test
z, zbar, w, wbar = JJ.z, JJ.zbar, JJ.w, JJ.wbar

from awake_defective_pair import M_metelmann_clerk

# ---------------------------------------------------------------------------
# Jordan numbers (same M_target as #021/#025)
# ---------------------------------------------------------------------------
G_, ETA, THETA = 1.0, 0.8, 0.3
J_ = G_ * ETA / 2.0
PHI = -THETA + np.pi / 2
K2_ = 0.5
K1_ = K2_ + G_ * (ETA**2 - 1)
M = M_metelmann_clerk(0.0, 0.0, K1_, K2_, G_, ETA, J_, PHI, THETA)
lam = complex(M[0, 0])                    # equal diagonal
kJ = complex(M[1, 0])                     # one-way entry (a1 -> a2)
print(f"[setup] lambda = {lam:.4f}   k(one-way) = {kJ:.4f}   G12 = {complex(M[0,1]):.2e}")

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def full_conj_2f(expr):
    """Two-field mirror: z<->zbar, w<->wbar, I->-I. Invariant <=> paired/real wall."""
    t1, t2 = sp.Symbol('__t1__'), sp.Symbol('__t2__')
    e = expr.subs({z: t1, w: t2}, simultaneous=True)
    e = e.subs({zbar: z, wbar: w}, simultaneous=True)
    e = e.subs({t1: zbar, t2: wbar}, simultaneous=True)
    return e.subs(sp.I, -sp.I)


def num_nonzero(expr, npts=24, scale=1.5, tol=1e-10):
    """Numeric nonzero check on random complex sample points (avoids simplify freezes).
    Returns (nonzero_bool, median_abs). Points where expr blows up are skipped."""
    f = sp.lambdify((z, zbar, w, wbar), expr, "numpy")
    rng = np.random.default_rng(2)
    vals = []
    tries = 0
    while len(vals) < npts and tries < 40 * npts:
        tries += 1
        Z = scale * (rng.standard_normal() + 1j * rng.standard_normal())
        W = scale * (rng.standard_normal() + 1j * rng.standard_normal())
        try:
            v = complex(f(Z, np.conj(Z), W, np.conj(W)))
        except Exception:
            continue
        if np.isfinite(v):
            vals.append(abs(v))
    if not vals:
        return False, 0.0
    med = float(np.median(vals))
    return med > tol, med


def cross_disc(K):
    """CROSS-field entanglement: d_z d_wbar log K  (nonzero => non-factorizable across
    the two points; zero => K = A(z,zbar)*B(w,wbar) locally => product wall)."""
    return sp.diff(sp.log(K), z, wbar)


def pairing_verdict(K):
    d = sp.expand(full_conj_2f(K) - K)
    nz, med = num_nonzero(d)
    return (not nz), med           # True => paired/mirror wall


def battery(name, K, expect_note=""):
    print(f"\n  [{name}] {expect_note}")
    cls, ders = certify_2field(K)
    print(f"    certify_2field       : {cls}")
    cd = cross_disc(K)
    nz, med = num_nonzero(cd)
    print(f"    cross-disc dz dwbar logK != 0 : {nz}   (median |.| = {med:.3e})")
    paired, pmed = pairing_verdict(K)
    print(f"    paired (full_conj_2f invariant) : {paired}   (residual {pmed:.3e})")
    rp, inv = rephasing_test(K)
    print(f"    rephasing            : {rp}")
    target = (nz and not paired)
    print(f"    => two-field gate (cross-entangled AND non-paired): "
          f"{'PASS' if target else 'FAIL'}")
    return target


# ---------------------------------------------------------------------------
# modes (spatial LG carriers, w0=1)
# ---------------------------------------------------------------------------
m1_z = z * sp.exp(-z * zbar)                          # LG(+1, p=0) at obs point
m2_z = zbar * (2 - 2 * z * zbar) * sp.exp(-z * zbar)  # LG(-1, p=1) at obs point
m1c_w = wbar * sp.exp(-w * wbar)                      # conj(m1) at source point
m2c_w = w * (2 - 2 * w * wbar) * sp.exp(-w * wbar)    # conj(m2) at source point


def main():
    print("=" * 74)
    print("spatial_kernel_test.py -- [HEURISTIQUE sandbox] -- machine + judge arbitrate")
    print("=" * 74)

    lam_s = sp.Float(lam.real) + sp.I * sp.Float(lam.imag)
    k_s = sp.Float(kJ.real) + sp.I * sp.Float(kJ.imag)

    # ---------------- STAGE 1: finite 2-mode kernel ----------------
    print("\n[STAGE 1] finite 2-mode Jordan kernel (sum of separable terms)")
    Kdiag = -(1 / lam_s) * (m1_z * m1c_w + m2_z * m2c_w)
    Kcross = (k_s / lam_s**2) * m2_z * m1c_w
    K2 = sp.expand(Kdiag + Kcross)
    battery("K2 Jordan (diag + one-way cross, double-pole weight k/lam^2)", K2,
            "(sum of 3 separable terms -- law #004 two-field side)")

    battery("CONTROL: single cross term m2(r1)*conj(m1)(r2)",
            sp.expand(Kcross),
            "(pure product: cross-disc must be ~0 -> wall)")

    # TRUNCATION ARTIFACT CAUGHT (self-audit): a 2-mode set {+1p0, -1p1} is NOT
    # conjugation-closed (full_conj maps it to {-1p0, +1p1}, outside the space), so a
    # Hermitian kernel built on it shows a spurious nonzero pairing residual. Clean
    # controls below use the CONJUGATION-CLOSED construction: K_herm = one-way half
    # + its full_conj_2f image (Hermitian by construction, exactly paired); the Jordan
    # keeps only the one-way half (non-paired).
    g = sp.Float(0.37) + sp.I * sp.Float(0.21)
    half = g * m2_z * m1c_w
    K_herm_closed = sp.expand(half + full_conj_2f(half))
    battery("CONTROL (conjugation-closed): Hermitian kernel = half + mirror(half)",
            K_herm_closed, "(reciprocal -> must be PAIRED -> FAIL)")
    battery("CONTROL (conjugation-closed): Jordan one-way half only",
            sp.expand(Kdiag + half),
            "(one-way -> non-paired; cross-entangled by sum law -> PASS expected)")

    # ---------------- STAGE 2: continuum class [DERIVATION from DRUM] --------
    print("\n[STAGE 2] continuum class representative (DRUM cross-kernel, spatial carrier)")
    Klog = sp.log(z - wbar)
    battery("K = log(z - wbar)  (canonical class rep)", Klog,
            "(target corner candidate: transcendental + cross + non-paired)")

    Kprim = (z - wbar) * (sp.log(z - wbar) - 1)
    battery("K = (z-wbar)(log(z-wbar)-1)  (primitive of the class)", Kprim, "")

    # historical-trap controls
    battery("TRAP CONTROL: log(z - w)  (holo-holo)", sp.log(z - w),
            "(no anti anywhere -> must FAIL as target)")
    battery("TRAP CONTROL: PAIRED sum log(z-wbar) + log(zbar-w)",
            sp.log(z - wbar) + sp.log(zbar - w),
            "(the 'transcendant apparie' trap -> must be PAIRED -> FAIL)")
    battery("TRAP CONTROL: product log(z)*log(wbar)", sp.log(z) * sp.log(wbar),
            "(cross-separable -> must FAIL)")

    # ---------------- SPARC / sieve notes ----------------
    print("\n[SPARC / sieve notes -- DERIVATION, to engrave with the FINDINGS]")
    print("  - Kernel is drive-independent: the #025 preparation-erasure axis does not")
    print("    exist for a transfer kernel; the forced content = G12=0 + double pole,")
    print("    non-erasable by licit gauge diag(s,1/s) [#021 GATE A, machine].")
    print("  - spatial_carrier (7th condition): z, w are LG-plane spatial coordinates")
    print("    by construction -- the condition that killed DRUM is satisfied here.")
    print("  - Rephasing covariance of log(z-wbar) is the winding content itself;")
    print("    physical invariant combinations pair it with mode weights (report only).")

    print("\n" + "=" * 74)
    print("REMINDER: sandbox only. Machine (real judge_v2) arbitrates.")


if __name__ == "__main__":
    main()
