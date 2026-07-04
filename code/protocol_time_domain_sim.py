#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protocol_time_domain_sim.py -- full NOISY time-domain simulation of the #029 protocol
(the one new valid item from the external audit: the frequency-domain kernel was
machine-validated (#028), the real-time noisy measurement chain was not).

BROKEN PARAMETER (orthogonal axis): "the #029 protocol is validated" -- it was, but
only in the noiseless frequency domain. Here: pulse the CW port -> CCW impulse
response -> detection noise (white, heterodyne; ASE-like) -> can the three protocol
checks be EXTRACTED under noise, and at which SNR?

MODEL [DERIVATION] (dimensionless: FSR delta = 1, so revival period T = 2*pi):
  Per rung m (Jordan double pole): h_m(t) = g0 e^{i m phi} * t * e^{lam_m t},
  lam_m = -kap/2 - i m delta.  At fixed ports the CCW field is
     E(t) = g0 * t * e^{-kap t/2} * D_M(phi - delta t),   D_M = Dirichlet comb
  => revival comb every T = 2*pi/delta, positions t_k = (phi + 2*pi*k)/delta,
     carried by the SECULAR envelope t * e^{-kap t/2} (the Jordan certificate).
  Diagonalizable control: h_m = g0 e^{i m phi} e^{lam_m t} (no t prefactor, p = 0).
  Reciprocal control: + mirror channel conj-weights e^{+i m(...)} => a TWIN comb at
  t_k' = (2*pi - phi + 2*pi*k)/delta. ONE-WAY = single comb; RECIPROCAL = twin combs:
  the mirror-deletion law, readable on an oscilloscope.

THE THREE EXTRACTIONS UNDER NOISE
  X1 Jordan exponent: fit p in peak_k ~ t_k^p e^{-kap t_k/2} over the revival peaks
     (log-linear regression with regressors log t_k and t_k). Jordan -> p = 1;
     diagonalizable -> p = 0. Report p-hat +- sigma vs SNR; find SNR* for 5-sigma
     separation.
  X2 phi-sweep: revival position t_1 vs phi must be linear with slope 1/delta.
  X3 mirror test: twin-comb detection = energy at the mirror positions relative to
     the main comb (one-way ~ noise floor; reciprocal ~ 1).

NOISE MODEL: additive complex white Gaussian on the record (detection + ASE lump),
SNR defined on the FIRST revival peak amplitude. Single-shot AND N_avg = 100 averages
(standard oscilloscope averaging) both reported.

STATUS: [HEURISTIQUE sandbox] until executed on Anthony's machine. Protocol-level
derivations [DERIVATION]; no judge claim (no new field formula).
"""

import numpy as np

rng = np.random.default_rng(0)

# ---------------- parameters (dimensionless, #029 fiber-ring regime) ----------------
DLT   = 1.0
KAP   = 0.2 * DLT          # kappa/delta = 0.2 (D3 regime)
G0    = 1.0
PHI   = 2.1                # loop phase (revival offset)
M_RUNG = 300               # served rungs in the simulated band
TMAX  = 8 * 2 * np.pi      # 8 revivals
NT    = 32768


def field_oneway(t, jordan=True):
    m = np.arange(1, M_RUNG + 1)
    lam = -KAP / 2 - 1j * m * DLT
    ph = G0 * np.exp(1j * m * PHI)
    # E(t) = sum_m ph * t^p * exp(lam t)
    ex = np.exp(np.outer(t, lam))            # (NT, M)
    pref = t[:, None] if jordan else np.ones_like(t)[:, None]
    return (ex * ph[None, :]).sum(axis=1) * pref[:, 0]


def field_reciprocal(t):
    m = np.arange(1, M_RUNG + 1)
    lam = -KAP / 2 - 1j * m * DLT
    ph = G0 * np.exp(1j * m * PHI)
    ex = np.exp(np.outer(t, lam))
    fwd = (ex * ph[None, :]).sum(axis=1)
    bwd = (ex * np.conj(ph)[None, :]).sum(axis=1)   # mirror partner (conj weights)
    return t * (fwd + bwd)


def add_noise(E, snr_peak, navg=1, seed=1):
    r = np.random.default_rng(seed)
    peak = np.abs(E).max()
    sig = peak / snr_peak
    noise = (r.standard_normal((navg,) + E.shape) +
             1j * r.standard_normal((navg,) + E.shape)) * sig / np.sqrt(2)
    return (E[None, :] + noise).mean(axis=0)


def find_revival_peaks(t, E, nrev=6):
    """Peak time and amplitude in each expected revival window."""
    out = []
    for k in range(nrev):
        tk = (PHI + 2 * np.pi * k) / DLT
        w = (t > tk - 1.5) & (t < tk + 1.5)
        if not np.any(w):
            continue
        i = np.argmax(np.abs(E[w]))
        out.append((t[w][i], np.abs(E[w][i])))
    return np.array(out)


def fit_p(peaks):
    """peak ~ C * t^p * exp(-kap t/2): log(peak) = logC + p log t - (kap/2) t.
    Linear LS in (1, log t, t); returns (p_hat, sigma_p, kap_hat)."""
    t, a = peaks[:, 0], peaks[:, 1]
    X = np.column_stack([np.ones_like(t), np.log(t), t])
    y = np.log(a)
    beta, res, *_ = np.linalg.lstsq(X, y, rcond=None)
    dof = max(len(t) - 3, 1)
    s2 = (res[0] / dof) if len(res) else np.sum((y - X @ beta)**2) / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta[1], np.sqrt(cov[1, 1]), -2 * beta[2]


def mirror_energy_ratio(t, E):
    """Energy near mirror revival positions / energy near main positions."""
    def energy_at(offsets):
        tot = 0.0
        for k in range(6):
            tk = (offsets + 2 * np.pi * k) / DLT
            w = (t > tk - 0.6) & (t < tk + 0.6)
            tot += np.sum(np.abs(E[w])**2)
        return tot
    main = energy_at(PHI)
    mirr = energy_at(2 * np.pi - PHI)
    return mirr / (main + 1e-300)


def main():
    global PHI
    print("=" * 76)
    print("protocol_time_domain_sim.py -- [HEURISTIQUE sandbox] -- machine arbitrates")
    print(f"params: kap/dlt={KAP/DLT}, M={M_RUNG}, phi={PHI}, 8 revivals, NT={NT}")
    print("=" * 76)
    t = np.linspace(1e-3, TMAX, NT)

    E_j = field_oneway(t, jordan=True)
    E_d = field_oneway(t, jordan=False)
    E_r = field_reciprocal(t)

    # ---------------- noiseless sanity ----------------
    pk = find_revival_peaks(t, E_j)
    p_j, s_j, kap_j = fit_p(pk)
    p_d, s_d, _ = fit_p(find_revival_peaks(t, E_d))
    print("\n[0] noiseless sanity")
    print(f"    revivals found at t_k = {np.round(pk[:,0], 3).tolist()} "
          f"(expected {np.round([(PHI+2*np.pi*k) for k in range(6)],3).tolist()})")
    print(f"    Jordan fit: p = {p_j:.3f} +- {s_j:.3f} (expect 1), "
          f"kappa_hat = {kap_j:.3f} (true {KAP})")
    print(f"    diagonalizable control: p = {p_d:.3f} +- {s_d:.3f} (expect 0)")
    print(f"    mirror ratio: one-way = {mirror_energy_ratio(t, E_j):.2e} "
          f"(noise floor), reciprocal = {mirror_energy_ratio(t, E_r):.2f} (~1)")

    # ---------------- X1: Jordan exponent vs SNR ----------------
    print("\n[X1] Jordan exponent p under noise (single shot and 100-average)")
    for navg in (1, 100):
        print(f"    N_avg = {navg}:")
        for snr in (3, 10, 30, 100):
            ps = []
            for trial in range(24):
                En = add_noise(E_j, snr, navg=navg, seed=100 * navg + 7 * trial + snr)
                pkn = find_revival_peaks(t, En)
                if len(pkn) < 4:
                    continue
                p, s, _ = fit_p(pkn)
                ps.append(p)
            ps = np.array(ps)
            sep = abs(ps.mean() - 0.0) / (ps.std() + 1e-12)   # sigmas from p=0
            print(f"      SNR={snr:4d}: p = {ps.mean():.3f} +- {ps.std():.3f}  "
                  f"(separation from diagonalizable p=0: {sep:.1f} sigma)")

    # ---------------- X2: phi-sweep linearity ----------------
    print("\n[X2] phi-sweep: revival position vs loop phase (piezo stretcher)")
    phis = np.linspace(0.5, 5.5, 9)
    t1s = []
    for ph in phis:
        PHI = ph
        En = add_noise(field_oneway(t, True), 10, navg=100, seed=int(ph * 1000))
        pkn = find_revival_peaks(t, En)
        t1s.append(pkn[0, 0] if len(pkn) else np.nan)
    PHI = 2.1
    slope, icpt = np.polyfit(phis, t1s, 1)
    print(f"    slope dt1/dphi = {slope:.4f} (expect 1/delta = {1/DLT}), "
          f"linear fit residual = {np.std(np.array(t1s) - (slope*phis+icpt)):.2e}")

    # ---------------- X3: mirror test under noise ----------------
    print("\n[X3] mirror (twin-comb) test under noise, SNR=10, N_avg=100")
    En_j = add_noise(field_oneway(t, True), 10, navg=100, seed=5)
    En_r = add_noise(field_reciprocal(t), 10, navg=100, seed=6)
    print(f"    one-way   mirror ratio = {mirror_energy_ratio(t, En_j):.3e}")
    print(f"    reciprocal mirror ratio = {mirror_energy_ratio(t, En_r):.3f}")
    print("    (one-way ~ noise floor vs reciprocal ~ 1: the mirror-deletion law on a scope)")

    print("\n[verdict template] the protocol is EXTRACTABLE if: p separates from 0 at")
    print(">=5 sigma at lab-accessible SNR; slope = 1/delta; mirror ratios separated by")
    print(">=2 orders. Machine run fills the actual numbers.")
    print("=" * 76)
    print("REMINDER: sandbox only until executed on Anthony's machine.")


if __name__ == "__main__":
    main()
