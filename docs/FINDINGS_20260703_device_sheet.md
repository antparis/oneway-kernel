# FINDINGS 2026-07-03 — real-device parameter sheet (visibility of the #027/#028 cusp)

STATUS: [CONJECTURE-grade device numbers] + [DERIVATION formulas]. Machine run of the
sheet certifies the ARITHMETIC, not the device values (literature-typical ranges; must
be re-checked against concrete datasheets before contacting any group). Judge N/A
(no new field claim).

## Main result — VISIBILITY LAW [DERIVATION] (orthogonal-axis catch on our own #028
## platform recommendation)
Probing on a resonant rung, the transcendental (Lerch/cusp) tail weighs, relative to
the resonant peak:  V = (pi^2/12) * (kappa/delta)^2   [verified vs direct sum, 3e-6].
=> The transcendental class needs kappa/delta NOT small. The report's chiral-EP CHIP
microring is the right MECHANISM but the WRONG REGIME: Si3N4 (kappa/delta ~ 1e-3)
gives V ~ 8e-7; SiO2 wedge V ~ 4e-9 — the cusp is BURIED on chip.

## The device that works [CONJECTURE-grade]: FIBER-LOOP ring
L = 20 m (n_g 1.468) -> FSR = 10.21 MHz; loaded finesse 5 -> kappa/2pi = 2.04 MHz;
kappa/delta = 0.20 -> V = 3.3e-2. Loop chain (isolator 0.8 dB + couplers 0.6 dB +
splices 0.4 dB) -> T_loop = 0.66; g0 = (kappa_ext/2)sqrt(T_loop) -> on-rung
converted/direct amplitude ratio 4g0/kappa = 0.81 (order one). Ladder size: GVD-limited
(AUDIT FIX: |beta2|L = 0.42 ps^2 breaks loop-phase linearity at m_disp ~ 6.0e4, NOT
negligible over 4 THz as first written) -> M_max ~ 60287 -> cusp width ~ 6.6e-5 rad.
Time domain: Jordan revivals every 97.9 ns with SECULAR t*exp(-kappa t/2) envelope
(double-pole certificate) — oscilloscope-grade (chip: 10-40 ps, ultrafast only).

## Measurement protocol [DERIVATION]
Kernel depends on (theta1+theta2 - phi), phi = loop phase: sweeping phi with a PIEZO
FIBER STRETCHER at FIXED ports scans the whole cusp lineshape (no movable probes;
required phi resolution ~ cusp width: trivial for sub-nm piezo stretch).
PRIMARY PROTOCOL: fiber ring + isolator feedback loop; pulse the CW port; record the
CCW impulse response; three checks = (i) secular t-envelope, (ii) revival comb at
1/FSR, (iii) phi-sweep cusp. All three together = the measured boundary value of the
machine-judged #027 kernel.

## Command
    python3 device_parameter_sheet.py    (pure numpy, seconds)

## Open before any experimental contact
- Re-check all device values against concrete datasheets (this sheet = typical ranges).
- SOA-compensated loop: model the ASE-noise bound on g0 (flagged, not modeled).
- Machine run of this sheet (arithmetic certification) then engrave #029.

## MACHINE CERTIFIED (2026-07-03) — arithmetic [ESTABLISHED machine]; device values stay [CONJECTURE-grade]
Machine run = sandbox digit-for-digit (device_machine_20260703.txt). Visibility law
V = (pi^2/12)(kappa/delta)^2 verified vs direct sum (3.0e-6). D1 Si3N4: V=7.7e-7
(cusp BURIED); D2 SiO2 wedge: V=4.2e-9; D3 FIBER-LOOP (L=20m, finesse 5): V=3.3e-2,
M_max=60287 (GVD-limited, |beta2|L=0.42 ps^2), conv ratio 0.81, revivals 97.93 ns
(oscilloscope-grade), phi-sweep by piezo stretcher at fixed ports. VERDICT: the report's
chip chiral-EP recommendation = right MECHANISM, wrong REGIME; primary device = fiber
ring + isolator feedback loop; protocol = pulse CW port, CCW impulse response, three
checks (secular t-envelope, revival comb, phi-sweep cusp). Registry #029 engraved.
Before any experimental contact: datasheet re-check + ASE bound (SOA) + mock-modularity
shielding (report's reviewer risk #1).
