#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protocol_effects_modular.py -- MODULAR effects simulator for the active fiber-loop
protocol: 4 master switches + 1 negligible group, each on/off x {typical, stress}.

ORIGIN: Grok's 10-effect list -> deep-research noise budget (RESEARCH_NOTE traced) ->
this build. Held parameter broken: "#031's four layers suffice". All values are
LITERATURE-TYPICAL / catalogue worst-case [CONJECTURE-grade] -- to be replaced by
measured values on the real purchased components (option-1 decision, converged with
our own #032 discipline). The machine run certifies the SIMULATION, not the values.

ARCHITECTURE (from the report; the within-record vs between-shot split is wired in):
  A. LOOP PHASE NOISE (thermal 960 rad/K over 20 m + acoustic 1/f + vibrations)
     -> BETWEEN-SHOT: comb damping exp(-m^2 sig^2/2) + slow drift across the run.
     typical (enclosed): sig_phi = 0.05 rad shot-to-shot, drift 0.5 rad over run
     stress (bare table): sig_phi = 1.0 rad, drift 10 rad over run
  B. INTENSITY NOISE (EDFA RIN -110 dB/Hz over 1 GHz -> ~10% RMS within-record;
     laser RIN -150 dB/Hz -> 0.3%; EDFA gain drift 0.1 dB/min -> shot-to-shot)
     -> WITHIN-RECORD multiplicative + shot-to-shot amplitude jitter.
     typical: rin_rms = 0.10, gain_jit = 0.02 ; stress: rin_rms = 0.30, gain_jit = 0.10
  C. POLARIZATION (SOP drift x PDL ~0.2 dB -> slow T_loop fading; PMD 20 m ~ fs: neg.)
     -> BETWEEN-SHOT multiplicative fading of the whole record.
     typical: fade_rms = 0.05 ; stress: fade_rms = 0.20
  D. REFLECTIONS / RESIDUAL ISOLATION (isolation 40 dB -> mirror ENERGY floor 1e-4
     dominates; Rayleigh 20 m ~ 2e-6 and connectors ~1e-6 below it)
     -> injects a genuine WEAK TWIN COMB at the mirror phase.
     typical: mirror_amp = sqrt(1e-4) = 1e-2 ; stress: isolation 30 dB -> 3.2e-2
  E. NEGLIGIBLE GROUP (Kerr 2.6e-5 rad/turn @ 1 mW; beta3/beta2 ~ 1e-3): switches
     exist, DEFAULT OFF, numbers printed to justify.

OBSERVABLES per scenario: Jordan p (fit t^p e^{-kt/2} on revival peaks), first-peak
amplitude, comb content m_eff (Fourier tones above threshold), mirror energy ratio.
STATUS: [HEURISTIQUE sandbox] until machine.
"""

import numpy as np

# base (mapped #032 regime)
DLT, KAP, PHI = 1.0, 0.192, 2.1
M_R, TMAX, NT = 98, 8 * 2 * np.pi, 32768
t = np.linspace(1e-3, TMAX, NT); DT = t[1] - t[0]
m = np.arange(1, M_R + 1)
LAM = -KAP / 2 - 1j * m * DLT
EX = np.exp(np.outer(t, LAM))
W = np.fft.fftfreq(NT, d=DT) * 2 * np.pi
H = (1.0 / (1j * (W[:, None] - m[None, :] * DLT) + KAP / 2)).sum(axis=1)
SNR_BASE = 30.0        # capped ASE-limited base (from #032), 100 averages
NSHOT = 100
NEGLIGIBLE = {"kerr_rad_per_turn": 2.6e-5, "beta3_over_beta2": 1e-3}

LEVELS = {
    "A_phase":   {"typ": dict(sig=0.05, drift=0.5), "str": dict(sig=1.0, drift=10.0)},
    "B_intens":  {"typ": dict(rin=0.10, gj=0.02),   "str": dict(rin=0.30, gj=0.10)},
    "C_polar":   {"typ": dict(fade=0.05),           "str": dict(fade=0.20)},
    "D_reflect": {"typ": dict(mamp=1.0e-2),         "str": dict(mamp=3.2e-2)},
}


def simulate(A=None, B=None, C=None, D=None, seed=0, nshots=NSHOT):
    """Explicit shot loop (drift/fading break the fixed-signal shortcut; K=nshots
    kept affordable at M=98)."""
    r = np.random.default_rng(seed)
    acc = np.zeros(NT, dtype=complex)
    for s in range(nshots):
        phi_s = PHI
        if A:
            phi_s += r.normal(0, A["sig"]) + A["drift"] * (s / nshots - 0.5)
        ph = np.exp(1j * m * phi_s)
        E = (EX @ ph) * t
        if D:
            E = E + D["mamp"] * (EX @ np.conj(np.exp(1j * m * phi_s))) * t
        amp = 1.0
        if B:
            amp *= (1 + r.normal(0, B["gj"]))
        if C:
            amp *= (1 + r.normal(0, C["fade"]))
        E = E * amp
        if B:
            E = E * (1 + B["rin"] * r.standard_normal(NT))      # within-record
        wn = (r.standard_normal(NT) + 1j * r.standard_normal(NT))
        col = np.fft.ifft(np.fft.fft(wn) * H)
        E = E + col * (np.abs(E).max() / SNR_BASE) / (np.std(col) + 1e-300)
        acc += E
    return acc / nshots


def peaks(E, nrev=6):
    out = []
    for k in range(nrev):
        tk = (PHI + 2 * np.pi * k) / DLT
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
    return b[1], np.sqrt(cov[1, 1])


def m_eff(E):
    """Comb content via first-revival width (the #031 metric): m_eff ~ 0.6*2pi/width.
    (FFT bin counting was noise-polluted -- instrument audit fix.)"""
    tk = PHI / DLT
    wd = (t > tk - np.pi) & (t < tk + np.pi)
    prof = np.abs(E[wd])
    half = prof > prof.max() / 2
    width = DT * np.sum(half)
    return min(int(0.6 * 2 * np.pi / max(width, DT)), M_R)


def validity(E):
    """Comb detected? first-peak amplitude vs RMS of an off-comb window."""
    tk = PHI / DLT
    wd = (t > tk - 0.5) & (t < tk + 0.5)
    off = (t > tk + np.pi - 0.5) & (t < tk + np.pi + 0.5)
    return np.abs(E[wd]).max() / (np.sqrt(np.mean(np.abs(E[off]) ** 2)) + 1e-300)


def mirror(E):
    def en(off):
        s = 0.0
        for k in range(6):
            tk = (off + 2 * np.pi * k) / DLT
            wd = (t > tk - 0.6) & (t < tk + 0.6)
            s += np.sum(np.abs(E[wd]) ** 2)
        return s
    return en(2 * np.pi - PHI) / (en(PHI) + 1e-300)


def run(name, **kw):
    E = simulate(**kw)
    pk = peaks(E)
    p, s = fitp(pk)
    v = validity(E)
    flag = "" if v > 5 else "  [COMB NOT DETECTED: p & mirror INVALID]"
    print(f"  {name:30s} p = {p:6.3f} +- {s:.3f} | amp1 = {pk[0,1]:8.1f} | "
          f"m_eff = {m_eff(E):3d} | mirror = {mirror(E):.2e} | det = {v:5.1f}{flag}")
    return p, s


def main():
    print("=" * 88)
    print("protocol_effects_modular.py -- [HEURISTIQUE sandbox] -- machine arbitrates")
    print(f"base: kap/dlt={KAP}, M={M_R}, SNR={SNR_BASE:.0f}, {NSHOT} shots (explicit loop)")
    print(f"negligible (switch off, justified): Kerr {NEGLIGIBLE['kerr_rad_per_turn']:.1e} "
          f"rad/turn @1mW; beta3/beta2 ~ {NEGLIGIBLE['beta3_over_beta2']:.0e}")
    print("=" * 88)
    T = LEVELS
    print("\n[scenarios] (typical then stress; report hierarchy prediction: A > B ~ C > D)")
    run("baseline (all off)", seed=1)
    run("A phase TYP", A=T["A_phase"]["typ"], seed=2)
    run("A phase STRESS", A=T["A_phase"]["str"], seed=3)
    run("B intensity TYP", B=T["B_intens"]["typ"], seed=4)
    run("B intensity STRESS", B=T["B_intens"]["str"], seed=5)
    run("C polarization TYP", C=T["C_polar"]["typ"], seed=6)
    run("C polarization STRESS", C=T["C_polar"]["str"], seed=7)
    run("D reflections TYP", D=T["D_reflect"]["typ"], seed=8)
    run("D reflections STRESS", D=T["D_reflect"]["str"], seed=9)
    run("ALL TYPICAL", A=T["A_phase"]["typ"], B=T["B_intens"]["typ"],
        C=T["C_polar"]["typ"], D=T["D_reflect"]["typ"], seed=10)
    run("ALL STRESS", A=T["A_phase"]["str"], B=T["B_intens"]["str"],
        C=T["C_polar"]["str"], D=T["D_reflect"]["str"], seed=11)

    print("\n[reading grid]")
    print("  - p column: within-record effects (B rin) are the only ones that can bias")
    print("    p; between-shot effects (A, C, D) should leave p intact even when the")
    print("    comb (m_eff) and amplitude collapse -- #031's jitter-immunity, retested")
    print("    against the full effect set.")
    print("  - m_eff column: the comb killer ranking; report predicts A first.")
    print("  - mirror column: D injects a GENUINE weak twin comb (floor), distinct from")
    print("    noise-floor mirror ratios -- the isolation spec sets the mirror-test floor.")
    print("  - FINDING (grid): phase jitter POLLUTES the mirror test (~10x) well before")
    print("    killing the comb -- A phase noise degrades X3 before X1. p and mirror are")
    print("    flagged INVALID when the comb is not detected (det <= 5): an instrument")
    print("    must refuse to report on a dead signal.")
    print("  - All values literature-typical/catalogue [CONJECTURE-grade]; measured")
    print("    component values replace them when hardware exists (option-1 decision).")
    print("=" * 88)
    print("REMINDER: sandbox only until executed on Anthony's machine.")


if __name__ == "__main__":
    main()
