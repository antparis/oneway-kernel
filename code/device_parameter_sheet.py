#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
device_parameter_sheet.py -- real-device parameter sheet for the #028 platform:
which physical resonator makes the #027 Lerch cusp VISIBLE?

STATUS: [CONJECTURE-grade mapping] with [DERIVATION] formulas. Literature-typical
parameter ranges (no new measurement); everything below must be re-checked against a
specific device datasheet before contacting any experimental group. Machine run of
this sheet = arithmetic certification of the formulas, not of the device values.

THE VISIBILITY LAW [DERIVATION] (the sheet's main result, orthogonal-axis catch):
Probing ON a resonant rung m0 (Delta = m0*dlt), the rung amplitude is g0/(kap/2)^2 and
each tail rung m contributes g0/((m-m0)*dlt)^2. Relative weight of the WHOLE
transcendental tail (the Lerch/cusp content) vs the resonant peak:
    V = sum_{m != m0} (kap/2)^2 / ((m-m0)*dlt)^2 = (kap/dlt)^2 * (pi^2/12) * 2/2
      ... exactly: 2 * zeta(2) * (kap/(2*dlt))^2 = (pi^2/12) * (kap/dlt)^2.
=> The transcendental class is VISIBLE only when kap/dlt is not small:
   chip microrings (kap/dlt ~ 1e-4..1e-3) bury the cusp; a FIBER-LOOP resonator
   (kap/dlt ~ 0.1..1, finesse 3..10) exposes it at O(1e-2..1).

MEASUREMENT SIMPLIFICATION [DERIVATION]: the kernel depends on (theta1+theta2 - phi),
phi = loop phase = omega * tau_loop. Sweeping phi with a fiber stretcher (piezo) at
FIXED ports scans the full cusp lineshape -- no movable probes needed.

TIME DOMAIN [DERIVATION]: G21(t) = sum_m g_m t e^{lam_m t} (Jordan double pole =>
SECULAR t-prefactor) = g0 * t * e^{-kap t/2} * comb(t; 1/FSR): revivals every 1/FSR
with the Jordan t-envelope. Fiber ring: revivals every ~100 ns (oscilloscope-grade);
chip: every ~10 ps (ultrafast needed).

DEVICES COMPARED (typical literature values, [CONJECTURE-grade]):
  D1 Si3N4 chip microring: R ~ 230 um, n_g ~ 2.1 -> FSR ~ 100 GHz; loaded Q ~ 2e6
     -> kap/2pi ~ 97 MHz; D2/2pi ~ 100 kHz; isolator bandwidth ~ 4 THz.
  D2 SiO2 wedge/disk: R ~ 1.2 mm -> FSR ~ 27 GHz; loaded Q ~ 1e8 -> kap/2pi ~ 1.9 MHz.
  D3 FIBER-LOOP ring: L = 20 m (n_g = 1.468) -> FSR = c/(n_g L) ~ 10.2 MHz;
     loaded finesse F ~ 5 -> kap/2pi = FSR/F ~ 2.0 MHz; loop chain: isolator insertion
     loss ~ 0.8 dB, 2 couplers ~ 0.6 dB, splices ~ 0.4 dB -> T_loop ~ -1.8 dB ~ 0.66
     (optionally SOA-compensated; ASE noise then bounds g0 -- flagged, not modeled).

LADDER SIZE M_max = min( component bandwidth / FSR , dispersion limit ):
  dispersion limit: ladder linearity holds while |D2| m^2 / 2 < kap  =>
  m_disp ~ sqrt(2 kap / D2). Cusp width ~ 4 / M_max (established #028).

RUN:  python3 device_parameter_sheet.py
"""

import numpy as np

C0 = 299792458.0
PI = np.pi


def device(name, fsr_hz, kap_hz, d2_hz, bw_hz, g0_hz, revival_note=""):
    kd = kap_hz / fsr_hz
    vis = (PI**2 / 12.0) * kd**2
    m_bw = bw_hz / fsr_hz
    m_disp = np.sqrt(2 * kap_hz / d2_hz) if d2_hz > 0 else np.inf
    m_max = min(m_bw, m_disp)
    cusp_w = 4.0 / m_max
    conv = 4 * g0_hz / kap_hz            # on-rung converted/direct amplitude ratio
    t_rev = 1.0 / fsr_hz
    print(f"\n  [{name}]")
    print(f"    FSR (delta)        = {fsr_hz/1e6:10.2f} MHz")
    print(f"    kappa (loaded)     = {kap_hz/1e6:10.3f} MHz    kappa/delta = {kd:.3e}")
    print(f"    ladder M_max       = {m_max:10.0f}   (bandwidth {m_bw:.0f} vs dispersion "
          f"{'inf' if np.isinf(m_disp) else f'{m_disp:.0f}'})")
    print(f"    cusp width ~4/M    = {cusp_w:10.3e} rad  ({np.degrees(cusp_w):.3g} deg)")
    print(f"    VISIBILITY V       = {vis:10.3e}   [(pi^2/12)(kappa/delta)^2]")
    print(f"    on-rung conv ratio = {conv:10.3f}   [4 g0/kappa]")
    print(f"    time-domain revival period = {t_rev*1e9:8.2f} ns  {revival_note}")
    return vis, cusp_w


def main():
    print("=" * 76)
    print("device_parameter_sheet.py -- [CONJECTURE-grade mapping, DERIVATION formulas]")
    print("=" * 76)

    # sanity: the visibility law against a direct numeric tail sum
    kap, dlt = 0.35, 1.0
    m = np.arange(1, 200001)
    tail = np.sum((kap / 2)**2 / (m * dlt)**2) * 2      # both sides of m0
    law = (PI**2 / 12) * (kap / dlt)**2
    print(f"\n[check] visibility law vs direct sum (kap/dlt=0.35): "
          f"law={law:.6f}  sum={tail:.6f}  rel err={(abs(law-tail)/law):.1e}")

    print("\n[devices]")
    # D1 Si3N4 chip: FSR 100 GHz, Q_L=2e6 at 193.4 THz -> kap = f/Q
    f0 = 193.4e12
    device("D1  Si3N4 chip microring (R~230um)",
           fsr_hz=100e9, kap_hz=f0 / 2e6, d2_hz=100e3, bw_hz=4e12,
           g0_hz=10e6, revival_note="(10 ps: ultrafast only)")
    # D2 SiO2 wedge: FSR 27 GHz, Q_L=1e8
    device("D2  SiO2 wedge disk (R~1.2mm)",
           fsr_hz=27e9, kap_hz=f0 / 1e8, d2_hz=20e3, bw_hz=4e12,
           g0_hz=1e6, revival_note="(37 ps: ultrafast only)")
    # D3 fiber loop: L=20m, n_g=1.468, finesse 5; g0 = (kap_ext/2)*sqrt(T_loop),
    # kap_ext ~ kap/2 (critical-ish), T_loop = 10^(-1.8/10)
    fsr3 = C0 / (1.468 * 20.0)
    kap3 = fsr3 / 5.0
    T_loop = 10 ** (-1.8 / 10)
    g03 = (kap3 / 4.0) * np.sqrt(T_loop)
    # AUDIT FIX: fiber GVD is NOT negligible over 4 THz. Loop-phase linearity
    # (phi_m = omega_m * tau(omega_m)) breaks when |beta2| L (2pi m FSR)^2 / 2 ~ pi:
    beta2 = 21e-27          # s^2/m at 1550 nm (std SMF, magnitude)
    L_loop = 20.0
    m_disp3 = np.sqrt(2 * np.pi / (beta2 * L_loop * (2 * np.pi * fsr3)**2))
    # feed as an equivalent d2 so device() computes min() itself:
    d2_equiv = 2 * kap3 / m_disp3**2
    v3, w3 = device("D3  FIBER-LOOP ring (L=20m, finesse 5)",
                    fsr_hz=fsr3, kap_hz=kap3, d2_hz=d2_equiv, bw_hz=4e12,
                    g0_hz=g03, revival_note="(98 ns: oscilloscope-grade)")
    print(f"    GVD bound: |beta2| L = {beta2*L_loop*1e24:.2f} ps^2 -> m_disp ~ "
          f"{m_disp3:.0f} (loop-phase linearity), NOT negligible over 4 THz")
    print(f"    loop chain: isolator 0.8 dB + couplers 0.6 dB + splices 0.4 dB "
          f"-> T_loop = {T_loop:.2f}; g0 = (kap_ext/2)sqrt(T_loop) with kap_ext=kap/2")
    print(f"    NOTE: SOA compensation of T_loop possible; ASE noise then bounds g0 "
          f"(flagged, not modeled). Phi-sweep resolution needed ~ cusp width: trivial "
          f"for a piezo stretcher (sub-nm stretch resolution).")

    print("\n[verdict, CONJECTURE-grade]")
    print("  - Chip platforms (D1, D2): visibility 1e-7..1e-9 -> the Lerch cusp is")
    print("    BURIED. The report's chiral-EP microring is the right MECHANISM but the")
    print("    wrong REGIME for the transcendental class (kappa/delta too small).")
    print("  - D3 fiber-loop ring: kappa/delta ~ 0.2 -> V ~ 3e-2; cusp width ~ 6e-5 rad")
    print("    equivalent in phase sweep; time-domain Jordan revivals every ~100 ns with")
    print("    SECULAR t-envelope (the double-pole certificate) on an oscilloscope;")
    print("    phi-sweep by piezo fiber stretcher at FIXED ports replaces movable probes.")
    print("  - PRIMARY PROTOCOL: fiber ring + isolator feedback loop; pulse the CW port;")
    print("    record the CCW impulse response; check (i) t*exp(-kap t/2) secular")
    print("    envelope, (ii) revival comb at 1/FSR, (iii) phi-sweep cusp; all three =")
    print("    the measured boundary of the machine-judged #027 kernel.")
    print("  - All device numbers are literature-typical [CONJECTURE-grade]: re-check")
    print("    against a concrete datasheet before contacting any group.")
    print("=" * 76)


if __name__ == "__main__":
    main()
