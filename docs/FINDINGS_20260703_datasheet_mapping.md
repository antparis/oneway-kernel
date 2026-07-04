# FINDINGS 2026-07-03 — datasheet mapping: every #031 knob now carries units

STATUS: [HEURISTIQUE sandbox] — machine re-run pending. Component values are TYPICAL
literature/catalog numbers [CONJECTURE-grade]: the machine run certifies the
ARITHMETIC and the extraction, NOT the component values; re-check against the real
purchased components stays OPEN. Grok's conversion formulas audited: NF->ASE
S=(h*nu/2)(F*G-1) EXACT (includes 1/G shot term); kappa formula kept with C =
THROUGH fraction (definition fixed); mirror ENERGY floor 10^(-iso/10) matches X3.

## Component sheet (typical, 1550 nm)
SMF-28 20 m loop (FSR 10.211 MHz, T_rev 97.93 ns, beta2 -21.7 ps^2/km); isolator
0.8 dB IL / 40 dB isolation; couplers 2x0.3 dB; splices 4x0.1 dB; 70/30 add-drop
(C_through = 0.30, see C4); EDFA NF 5 dB, G = 1.515 (compensates 1.80 dB passive);
detector 1 GHz (n_det = 98 rungs); laser 100 kHz linewidth; piezo/thermal
sigma_phi = 0.02 rad; probe 1 mW / 10 ns.

## Derived knobs (all #031 knobs now with units)
kappa_loaded/2pi = 1.957 MHz -> kappa/delta = 0.192 (the #029 regime, recovered from
components); conv ratio 4g0/kappa = 2.0; S_ASE = 2.43e-19 W/Hz -> P_ASE(1 GHz) =
0.24 nW vs P_sig ~ 200 uW -> single-shot amplitude SNR ~ 900 (ASE not limiting);
c2*M^2/kappa = 1.4e-5 (subcritical); mirror isolation floor = 1e-4.

## The four mapping catches (all machine-checkable)
C1 LASER LINEWIDTH = extra decay rate pi*dnu (ensemble): kappa_hat BIASED by
   2*pi*dnu/dlt (measured 0.0100 vs predicted 0.0098) while the JORDAN EXPONENT p
   stays UNBIASED (1.001 +- 0.005, 185 sigma) — the t-regressor absorbs the rate.
   Lab rule: correct kappa_hat by the independently-measured linewidth; trust p.
C2 ISOLATION FLOOR 1e-4 (40 dB single stage) sits BELOW the realistic noise-floor
   mirror ratio (2.05e-3 at the mapped SNR/averaging): single-stage isolator
   suffices initially; dual-stage is an upgrade path, not a prerequisite.
C3 FIBER DISPERSION subcritical at n_det = 98 rungs (consistent with #029 m_disp~6e4).
C4 DESIGN TENSION (main catch): FULL gain compensation raises finesse and buries the
   frequency-domain cusp (kappa/delta -> 0.017, visibility law #029). RESOLUTION:
   heavy out-coupling (70/30) restores kappa/delta = 0.192 with the EDFA still
   compensating the passive chain. Scope note: the TIME-domain protocol (p-fit,
   revival comb, mirror test) is INSENSITIVE to kappa/delta — the tension concerns
   only the frequency-domain cusp option.

## Command
    python3 protocol_datasheet_mapped.py     (numpy only, ~1 min)

## To confirm on machine (blocking)
1. Re-run; check sheet numbers, X1 p/kappa-bias, X3 vs floor.
2. Engrave #032; update kickoff + MILO.
3. Queue after: judge patch H2 (this session's single judge patch, backup first);
   paper duo (mock-modularity shielding + standard-language translation) next session;
   real purchased-component re-check when hardware is considered.

## MACHINE CERTIFIED (2026-07-03) — [ESTABLISHED machine]; component values stay [CONJECTURE]
Machine run = sandbox digit-for-digit (datasheet_machine_20260703.txt). Scope
(calibrated, external-audit-converged): established = the MAPPING arithmetic and the
extraction under mapped knobs, all component values CATALOGUE-TYPICAL; hardware
validity stays [CONJECTURE] pending re-check on real purchased components.
Numbers: FSR 10.211 MHz, kappa/delta = 0.192 (recovered from components via 70/30
out-coupling), conv 4g0/kappa = 2.00, single-shot SNR ~ 907 (ASE not limiting),
n_det = 98, c2*M^2/kappa = 1.4e-5. C1: laser linewidth = extra rate pi*dnu ->
kappa_hat biased +0.0100 (predicted 0.0098), p UNBIASED (1.001 +- 0.005, 185 sigma);
lab rule: correct kappa_hat by measured linewidth, trust p. C2: 40 dB isolation floor
(1e-4) below realistic noise floor (2.05e-3): single-stage suffices initially.
C3: dispersion subcritical. C4 (main catch): full EDFA compensation buries the
frequency cusp (kappa/delta -> 0.017); 70/30 out-coupling restores 0.192; the
TIME-domain protocol is insensitive to kappa/delta. Registry #032 engraved.
