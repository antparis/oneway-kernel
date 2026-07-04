#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protocol_realistic_noise.py -- breaking #030's held parameter: "noise is ADDITIVE WHITE".

Four realism layers on the #029/#030 fiber-ring protocol, each with its own kill-knob:
  R1 STRUCTURED ASE: the SOA compensating T_loop injects ASE that RECIRCULATES and gets
     COLORED by the ring resonances -- the noise concentrates exactly where the signal
     lives (worst case, unlike white). Model: white complex noise FFT-filtered by the
     ring response sum_m 1/(i(w - m*dlt) + kap/2), scaled to a target in-band SNR.
  R2 PHOTODETECTOR: finite bandwidth = Gaussian low-pass at n_det rungs; n_det < M
     truncates the effective ladder (comb/cusp broadening ~ 4/n_det instead of 4/M).
  R3 LOOP DISPERSION: quadratic per-rung phase c2*m^2 decoheres LATE revivals
     (broadening grows with revival index k). HONEST NOTE: at the #029 fiber design
     (m_disp ~ 6e4) c2 is SUBCRITICAL for M = 300; an exaggerated c2 is also simulated
     to exhibit the failure signature, labeled as such.
  R4 THERMAL PHI JITTER: phi drifts between averaged shots (sigma_phi per shot);
     averaging then smears the comb (contrast decays ~ exp(-m^2 sigma_phi^2 / 2)).

EXTRACTIONS re-run under each layer (same as #030): X1 Jordan exponent p; X3 mirror
(twin-comb) ratio; plus the layer-specific failure signatures (comb width vs n_det,
revival broadening vs k, contrast vs sigma_phi).

STATUS: [HEURISTIQUE sandbox] until machine. Model-level [DERIVATION]; all "realistic"
magnitudes are dimensionless knobs, not device datasheet values ([CONJECTURE-grade]).
"""

import numpy as np

# ---------------- base (identical to #030) ----------------
DLT, KAP, G0, PHI = 1.0, 0.2, 1.0, 2.1
M_RUNG, TMAX, NT = 300, 8 * 2 * np.pi, 32768
t = np.linspace(1e-3, TMAX, NT)
DT = t[1] - t[0]


# ---------------- precomputed kernels (cost audit: single build) ----------------
_M = np.arange(1, M_RUNG + 1)
_LAM = -KAP / 2 - 1j * _M * DLT
_EX = np.exp(np.outer(t, _LAM))                       # (NT, M) once
_W = np.fft.fftfreq(NT, d=DT) * 2 * np.pi
_H = (1.0 / (1j * (_W[:, None] - _M[None, :] * DLT) + KAP / 2)).sum(axis=1)  # once


def field(jordan=True, c2=0.0, phi=PHI, mirror=False, sigma_phi=0.0):
    """Averaged-over-jitter field: phi ~ N(phi, sigma^2) gives EXACT per-rung
    Gaussian damping exp(-m^2 sigma^2/2). MODEL FIX (self-audit): loop DISPERSION
    accumulates PER ROUND TRIP => it belongs in the FREQUENCIES,
    lam_m = -kap/2 - i(m*dlt + c2*m^2), so revival k sees phase k*2pi*c2*m^2/dlt
    and LATE revivals broaden (the static-weight-phase version could not show it)."""
    damp = np.exp(-0.5 * (_M * sigma_phi)**2)
    ph = G0 * np.exp(1j * _M * phi) * damp
    pref = t if jordan else np.ones_like(t)
    if c2 == 0.0:
        E = (_EX @ ph) * pref
    else:
        lam = -KAP / 2 - 1j * (_M * DLT + c2 * _M**2)
        E = (np.exp(np.outer(t, lam)) @ ph) * pref
    if mirror:
        E = E + (_EX @ np.conj(ph)) * pref
    return E


def colored_ase(seed, target_snr, E_ref):
    """One draw of ring-colored ASE at the given in-record SNR (filter precomputed)."""
    r = np.random.default_rng(seed)
    white = (r.standard_normal(NT) + 1j * r.standard_normal(NT))
    col = np.fft.ifft(np.fft.fft(white) * _H)
    col *= (np.abs(E_ref).max() / target_snr) / (np.std(col) + 1e-300)
    return col


def detector_lowpass(E, n_det):
    """Gaussian low-pass with cutoff at n_det rungs (detector bandwidth)."""
    G = np.exp(-0.5 * (_W / (n_det * DLT))**2)
    return np.fft.ifft(np.fft.fft(E) * G)


def noisy_avg(E, snr, nshots, n_det, seed):
    """EXACT shortcut: mean of N fixed-signal shots = E + colored/sqrt(N)."""
    En = E + colored_ase(seed, snr * np.sqrt(nshots), E)
    return detector_lowpass(En, n_det)


def find_peaks(E, phi=PHI, nrev=6):
    out = []
    for k in range(nrev):
        tk = (phi + 2 * np.pi * k) / DLT
        wdw = (t > tk - 1.5) & (t < tk + 1.5)
        i = np.argmax(np.abs(E[wdw]))
        out.append((t[wdw][i], np.abs(E[wdw][i])))
    return np.array(out)


def fit_p(peaks):
    tt, a = peaks[:, 0], peaks[:, 1]
    X = np.column_stack([np.ones_like(tt), np.log(tt), tt])
    beta, res, *_ = np.linalg.lstsq(X, np.log(a), rcond=None)
    dof = max(len(tt) - 3, 1)
    s2 = (res[0] / dof) if len(res) else np.sum((np.log(a) - X @ beta)**2) / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta[1], np.sqrt(cov[1, 1])


def mirror_ratio(E, phi=PHI):
    def en(off):
        s = 0.0
        for k in range(6):
            tk = (off + 2 * np.pi * k) / DLT
            wdw = (t > tk - 0.6) & (t < tk + 0.6)
            s += np.sum(np.abs(E[wdw])**2)
        return s
    return en(2 * np.pi - phi) / (en(phi) + 1e-300)


def main():
    print("=" * 76)
    print("protocol_realistic_noise.py -- [HEURISTIQUE sandbox] -- machine arbitrates")
    print(f"base: kap/dlt={KAP}, M={M_RUNG}; layers: colored ASE, detector LPF, "
          f"dispersion c2, phi jitter")
    print("=" * 76)
    E_j = field(True); E_r = field(True, mirror=True)

    print("\n[R1] STRUCTURED (ring-colored) ASE, detector wide open (n_det=1000), 100 avg")
    for snr in (3, 10, 30):
        ps = []
        for trial in range(12):
            E = noisy_avg(E_j, snr, 100, 1000, 40 + trial + 100 * snr)
            p, s = fit_p(find_peaks(E))
            ps.append(p)
        ps = np.array(ps)
        print(f"    SNR={snr:3d}: p = {ps.mean():.3f} +- {ps.std():.3f}  "
              f"({abs(ps.mean())/(ps.std()+1e-12):.0f} sigma from p=0)")
    Ejn = noisy_avg(E_j, 10, 100, 1000, 7)
    Ern = noisy_avg(E_r, 10, 100, 1000, 8)
    print(f"    mirror @SNR=10/100avg: one-way {mirror_ratio(Ejn):.3e} vs "
          f"reciprocal {mirror_ratio(Ern):.3f}")

    print("\n[R2] DETECTOR bandwidth (rungs passed n_det), SNR=10, 100 avg")
    for nd in (400, 150, 50, 15):
        E = noisy_avg(E_j, 10, 100, nd, 21 + nd)
        pk = find_peaks(E)
        p, s = fit_p(pk)
        tk = pk[0, 0]
        wdw = (t > tk - 2.0) & (t < tk + 2.0)
        prof = np.abs(E[wdw]); half = prof > prof.max() / 2
        width = DT * np.sum(half)
        print(f"    n_det={nd:4d}: p = {p:.3f} +- {s:.3f}; first-revival width = "
              f"{width:.3f} (Dirichlet half-width ~ 0.6*2pi/min(n_det,M) = "
              f"{0.6*2*np.pi/min(nd, M_RUNG):.3f}; scaling 1/M_eff is the claim)")

    print("\n[R3] DISPERSION c2*m^2 (design value SUBCRITICAL at M=300; exaggerated shown)")
    for c2, tag in ((0.0, "design-scale (subcritical, #029 m_disp~6e4)"),
                    (1e-6, "moderate (c2*M^2/kap = 0.45)"),
                    (1e-5, "EXAGGERATED (c2*M^2/kap = 4.5, failure signature)")):
        E = noisy_avg(field(True, c2), 10, 100, 1000, 90)
        pk = find_peaks(E)
        widths = []
        for k in range(0, 6, 2):
            tk = pk[k, 0]
            wdw = (t > tk - 2.0) & (t < tk + 2.0)
            prof = np.abs(E[wdw]); half = prof > prof.max() / 2
            widths.append(DT * np.sum(half))
        p, s = fit_p(pk)
        print(f"    c2={c2:.0e} [{tag}]: p={p:.3f}; revival widths k=0,2,4 -> "
              f"{[round(w,3) for w in widths]}")

    print("\n[R4] THERMAL phi jitter across 100 averaged shots, SNR=10 "
          "(exact Gaussian rung damping exp(-m^2 sig^2/2))")
    for sig in (0.0, 0.02, 0.05, 0.15):
        E = noisy_avg(field(True, sigma_phi=sig), 10, 100, 1000, 63 + int(sig * 1000))
        pk = find_peaks(E)
        p, s = fit_p(pk)
        print(f"    sigma_phi={sig:5.2f} rad: p = {p:.3f} +- {s:.3f}, first-peak "
              f"amplitude = {pk[0,1]:.3f} (kills high-m rungs first: effective ladder "
              f"m_eff ~ 1/sigma = {('inf' if sig==0 else f'{1/sig:.0f}')})")

    print("\n[reading, DERIVATION -> machine]")
    print("  - Exact shortcuts used (cost audit): N-shot average of a fixed signal =")
    print("    one draw at SNR*sqrt(N); jitter average = per-rung exp(-m^2 sig^2/2).")
    print("  - Kill hierarchy read from the tables; machine freezes the numbers.")
    print("  - All magnitudes are dimensionless knobs [CONJECTURE-grade]; datasheet")
    print("    mapping stays the next queue item.")
    print("=" * 76)
    print("REMINDER: sandbox only until executed on Anthony's machine.")


if __name__ == "__main__":
    main()
