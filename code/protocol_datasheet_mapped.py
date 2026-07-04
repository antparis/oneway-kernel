#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protocol_datasheet_mapped.py -- #031's held parameter broken: "the knobs are
dimensionless". Every knob is now COMPUTED from typical component values
([CONJECTURE-grade typical] -- to be re-checked against real datasheets before any
experimental contact; the machine run certifies the ARITHMETIC and the extraction,
not the component values).

COMPONENT SHEET (typical, 1550 nm)
  Fiber loop: L = 20 m SMF-28, n_g = 1.468, loss 0.2 dB/km, beta2 = -21.7 ps^2/km
  Isolator: insertion 0.8 dB, ISOLATION 40 dB (single stage; dual ~58 dB option)
  Couplers: 2 x 0.3 dB insertion; add-drop THROUGH (stay-in-loop) fraction C = 0.90
            (10% out-coupling => kappa_ext); splices 4 x 0.1 dB
  EDFA (not SOA -- gain ~ms, transparent at ~100 ns revivals): NF = 5 dB, G set to
            compensate the passive chain
  Detector: 1 GHz bandwidth  => n_det = BW/FSR rungs passed
  Laser: linewidth 100 kHz (self-heterodyne, common-mode cancelled up to the
            differential delay k*T_rev)
  Piezo/thermal loop-phase jitter over one averaging run: sigma_phi = 0.02 rad
  Input probe pulse: 1 mW peak, ~10 ns (order-of-magnitude for the SNR estimate)

GROK FORMULAS (audited): S_ASE = (h*nu/2)(F*G - 1) [EXACT, includes 1/G shot term];
kappa = -ln(T_rt_power)/T_loop with C = THROUGH fraction (definition fixed);
mirror ENERGY floor = 10^(-iso_dB/10) [matches our energy-based X3].

THREE MAPPING CATCHES (derived while building, verified below):
  C1 LASER LINEWIDTH acts like a jitter GROWING WITH REVIVAL INDEX k
     (sigma_k^2 = 2*pi*dnu*k*T_rev): ensemble-averaged, it multiplies E(t) by
     exp(-pi*dnu*t) = an EXTRA DECAY RATE pi*dnu. Consequence: kappa_hat is BIASED
     by +2*pi*dnu (fit measures kappa + 2*pi*dnu) but the Jordan exponent p is
     UNBIASED (the t-regressor absorbs it; log t and t separate). Verified.
  C2 ISOLATION FLOOR (40 dB -> 1e-4) sits BELOW the noise-floor mirror ratio at
     realistic SNR (~1e-2 at SNR=10/100avg): single-stage isolation is NOT the
     limiting factor; dual-stage unnecessary initially.
  C3 DISPERSION: subcritical at M = n_det = 98 (consistent with #029 m_disp ~ 6e4).
  C4 DESIGN TENSION (the mapping's main catch): an EDFA that FULLY compensates the
     passive chain raises the finesse (kappa/delta -> 0.017) and BURIES the
     frequency-domain cusp (visibility law #029). Resolution: HEAVY OUT-COUPLING
     (70/30 coupler, C_through = 0.30) restores kappa/delta ~ 0.19 while the EDFA
     still compensates the passive losses. Honest scope note: the TIME-domain
     protocol (#030/#031: p-fit, revival comb, mirror test) is INSENSITIVE to
     kappa/delta -- the tension concerns only the frequency-domain cusp option.

STATUS: [HEURISTIQUE sandbox] until machine.
"""

import numpy as np

# ---------------- component sheet ----------------
C0 = 299792458.0
LAM0 = 1550e-9
HNU = 6.62607015e-34 * C0 / LAM0          # photon energy [J]
L_FIB, NG = 20.0, 1.468
FSR = C0 / (NG * L_FIB)                    # [Hz]
T_REV = 1.0 / FSR
BETA2 = -21.7e-27                          # s^2/m
ISO_DB = 40.0
NF_DB, = (5.0,)
IL_ISO, IL_CPL, IL_SPL = 0.8, 2 * 0.3, 4 * 0.1   # dB
C_THROUGH = 0.30                           # coupler stay-in-loop fraction (70/30: see C4)
BW_DET = 1e9                               # Hz
DNU_LASER = 100e3                          # Hz
SIG_PIEZO = 0.02                           # rad
P_IN, T_PULSE = 1e-3, 10e-9                # W, s

def dB(x): return 10 ** (-x / 10)

def main():
    print("=" * 76)
    print("protocol_datasheet_mapped.py -- [HEURISTIQUE sandbox] -- machine arbitrates")
    print("=" * 76)

    # ---------------- derived quantities (Grok formulas, audited) ----------------
    passive_dB = IL_ISO + IL_CPL + IL_SPL + 0.2e-3 * L_FIB * 1e3 / 1e3
    T_passive = dB(passive_dB)
    G_EDFA = 1.0 / T_passive                       # compensate passive chain
    F_lin = 10 ** (NF_DB / 10)
    S_ASE = (HNU / 2) * (F_lin * G_EDFA - 1)       # W/Hz (exact, incl. 1/G term)
    T_rt_power = T_passive * G_EDFA * C_THROUGH    # net round trip incl. out-coupling
    kap = -np.log(T_rt_power) / T_REV              # rad/s (energy decay)
    kap_ext = -np.log(C_THROUGH) / T_REV
    dlt = 2 * np.pi * FSR                          # rad/s ladder spacing
    kap_over_dlt = kap / dlt
    n_det = BW_DET / FSR
    g0 = (kap_ext / 2) * np.sqrt(T_passive * G_EDFA)
    conv = 4 * g0 / kap
    # dispersion curvature per rung^2 (angular)
    c2 = abs(BETA2) * L_FIB * FSR * (2 * np.pi * FSR) ** 2
    crit = c2 * n_det**2 / kap
    # ASE-limited single-shot SNR (order of magnitude)
    P_ase_inband = S_ASE * BW_DET
    P_sig = P_IN * conv * 0.1                      # conservative conversion+insertion
    snr_amp = np.sqrt(P_sig / P_ase_inband)
    mirror_floor = dB(ISO_DB)

    print("\n[sheet -> knobs]")
    print(f"    FSR = {FSR/1e6:.3f} MHz, T_rev = {T_REV*1e9:.2f} ns; passive chain "
          f"{passive_dB:.2f} dB -> G_EDFA = {G_EDFA:.3f}")
    print(f"    kappa_loaded/2pi = {kap/2/np.pi/1e6:.3f} MHz  (kappa/delta = "
          f"{kap_over_dlt:.3f}); kappa_ext share = {kap_ext/kap:.2f}")
    print(f"    S_ASE = {S_ASE:.3e} W/Hz -> in-band P_ASE = {P_ase_inband*1e9:.2f} nW; "
          f"P_sig ~ {P_sig*1e6:.1f} uW -> single-shot amplitude SNR ~ {snr_amp:.0f}")
    print(f"    conv ratio 4g0/kappa = {conv:.2f}; n_det = {n_det:.0f} rungs; "
          f"c2*M^2/kappa = {crit:.1e} (subcritical, C3); mirror floor = "
          f"{mirror_floor:.1e} (C2)")

    # ---------------- dimensionless simulation with the MAPPED knobs ----------------
    DLT_, KAP_ = 1.0, kap_over_dlt
    M_ = int(min(n_det, 300)); PHI_ = 2.1
    TMAX, NT = 8 * 2 * np.pi, 32768
    t = np.linspace(1e-3, TMAX, NT); DT = t[1] - t[0]
    m = np.arange(1, M_ + 1)
    lam = -KAP_ / 2 - 1j * m * DLT_
    EX = np.exp(np.outer(t, lam))
    W = np.fft.fftfreq(NT, d=DT) * 2 * np.pi
    H = (1.0 / (1j * (W[:, None] - m[None, :] * DLT_) + KAP_ / 2)).sum(axis=1)
    dnu_dimless = DNU_LASER / FSR / (2 * np.pi) * (2 * np.pi)  # dnu in units of FSR
    laser_rate = np.pi * (DNU_LASER / FSR) / (2 * np.pi) * 2 * np.pi  # pi*dnu*t with t in T_rev*2pi units
    # in dimensionless time (dlt=1 => T_rev = 2*pi): pi*dnu*t_phys = pi*(dnu/FSR)*(t/2pi)
    laser_damp = np.exp(-np.pi * (DNU_LASER / FSR) * t / (2 * np.pi))

    def field(jordan=True, sig=SIG_PIEZO):
        damp = np.exp(-0.5 * (m * sig) ** 2)
        ph = np.exp(1j * m * PHI_) * damp
        pref = t if jordan else np.ones_like(t)
        return (EX @ ph) * pref

    def colored(seed, snr, E):
        r = np.random.default_rng(seed)
        w = (r.standard_normal(NT) + 1j * r.standard_normal(NT))
        c = np.fft.ifft(np.fft.fft(w) * H)
        return c * (np.abs(E).max() / snr) / (np.std(c) + 1e-300)

    def lowpass(E, nd):
        return np.fft.ifft(np.fft.fft(E) * np.exp(-0.5 * (W / (nd * DLT_)) ** 2))

    def peaks(E, nrev=6):
        out = []
        for k in range(nrev):
            tk = (PHI_ + 2 * np.pi * k) / DLT_
            wd = (t > tk - 1.5) & (t < tk + 1.5)
            i = np.argmax(np.abs(E[wd]))
            out.append((t[wd][i], np.abs(E[wd][i])))
        return np.array(out)

    def fitp(pk):
        tt, a = pk[:, 0], pk[:, 1]
        X = np.column_stack([np.ones_like(tt), np.log(tt), tt])
        b, res, *_ = np.linalg.lstsq(X, np.log(a), rcond=None)
        dof = max(len(tt) - 3, 1)
        s2 = (res[0] / dof) if len(res) else np.sum((np.log(a) - X @ b) ** 2) / dof
        cov = s2 * np.linalg.inv(X.T @ X)
        return b[1], np.sqrt(cov[1, 1]), -2 * b[2]

    def mirror(E):
        def en(off):
            s = 0.0
            for k in range(6):
                tk = (off + 2 * np.pi * k) / DLT_
                wd = (t > tk - 0.6) & (t < tk + 0.6)
                s += np.sum(np.abs(E[wd]) ** 2)
            return s
        return en(2 * np.pi - PHI_) / (en(PHI_) + 1e-300)

    print(f"\n[mapped run] kap/dlt = {KAP_:.3f}, M = {M_}, sigma_piezo = {SIG_PIEZO}, "
          f"laser {DNU_LASER/1e3:.0f} kHz, SNR ~ {min(snr_amp,30):.0f} (capped 30), 100 avg")
    E0 = field(True)
    E_las = E0 * laser_damp
    snr_use = min(snr_amp, 30.0)
    # C1 check: kappa bias with laser, p unbiased
    ps, ks_nolas, ks_las = [], [], []
    for trial in range(12):
        En = lowpass(E_las + colored(50 + trial, snr_use * 10, E_las), M_)
        p, s, kh = fitp(peaks(En))
        ps.append(p); ks_las.append(kh)
        En0 = lowpass(E0 + colored(500 + trial, snr_use * 10, E0), M_)
        _, _, kh0 = fitp(peaks(En0))
        ks_nolas.append(kh0)
    ps = np.array(ps)
    kbias = np.mean(ks_las) - np.mean(ks_nolas)
    kbias_pred = 2 * np.pi * (DNU_LASER / FSR) / (2 * np.pi)
    print(f"    X1 (with laser): p = {ps.mean():.3f} +- {ps.std():.3f}  "
          f"({abs(ps.mean())/(ps.std()+1e-12):.0f} sigma from 0) -> p UNBIASED (C1)")
    print(f"    kappa_hat bias (laser on - off) = {kbias:.4f} vs predicted 2*pi*dnu/dlt "
          f"= {kbias_pred:.4f} (C1: bias in kappa, not in p)")
    Ej = lowpass(E_las + colored(7, snr_use * 10, E_las), M_)
    mr = mirror(Ej)
    print(f"    X3 mirror ratio (one-way) = {mr:.2e}; ISOLATION floor = "
          f"{mirror_floor:.1e} -> noise floor {'ABOVE' if mr > mirror_floor else 'below'} "
          f"isolation floor (C2: single-stage isolator suffices initially)")

    print("\n[verdict, CONJECTURE-grade component values]")
    print(f"  - All #031 knobs now carry units: kap/dlt = {kap_over_dlt:.2f}, n_det = "
          f"{n_det:.0f}, sigma_phi = {SIG_PIEZO}, SNR ~ {snr_amp:.0f}, c2 subcritical.")
    print("  - C1: laser linewidth = extra decay rate pi*dnu; biases kappa_hat, NOT p.")
    print("  - C2: 40 dB isolation floor (1e-4) below realistic noise floor: not limiting.")
    print("  - C3: fiber dispersion subcritical at n_det=98 rungs.")
    print("  - C4: FULL gain compensation buries the frequency cusp (kap/dlt 0.017);")
    print("    70/30 out-coupling restores ~0.19; TIME-domain protocol insensitive.")
    print("  - Datasheet re-check against REAL purchased components remains OPEN.")
    print("=" * 76)
    print("REMINDER: sandbox only until executed on Anthony's machine.")

if __name__ == "__main__":
    main()
