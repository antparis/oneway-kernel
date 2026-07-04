# FINDINGS 2026-07-03 — realistic-noise protocol simulation (#030's held parameter broken)

STATUS: [HEURISTIQUE sandbox] — machine re-run pending. Model-level [DERIVATION];
all magnitudes are dimensionless knobs [CONJECTURE-grade] (datasheet mapping = next
queue item, unchanged). Merges our ASE queue item + the external audit's option 1/3.

## Broken parameter
#030 assumed ADDITIVE WHITE noise. Four realism layers, each with its kill-knob:
R1 ring-COLORED ASE (SOA noise recirculating on the resonances — worst case: noise
   where the signal lives); R2 photodetector low-pass (n_det rungs passed);
R3 loop dispersion; R4 thermal phi jitter across averaged shots.
Exact shortcuts (cost audit): N-shot average of fixed signal = one draw at
SNR*sqrt(N); jitter average = per-rung damping exp(-m^2 sigma^2/2) (analytic).

## Sandbox results (realistic_sandbox_20260703.txt)
R1 COLORED ASE: p = 0.969+-0.041 at SNR=3/100avg (24 sigma; white gave 37) —
   mild degradation, extraction robust; mirror 1.14e-2 vs 1.026 (survives).
R2 DETECTOR: p robust down to n_det=15 (0.978+-0.046); first-revival width scales
   as 1/min(n_det, M): 0.025 -> 0.321 from n_det=400 to 15.
R3 DISPERSION (MODEL FIX, self-audit catch #1: dispersion accumulates PER ROUND TRIP
   => belongs in the FREQUENCIES lam_m = -kap/2 - i(m dlt + c2 m^2), not in a static
   weight phase — the static version could not show late-revival broadening):
   design-scale: subcritical, flat widths; c2 M^2/kap = 4.5 (exaggerated): late
   revivals broaden 0.025 -> 0.069 -> 0.146 (k=0,2,4) and p degrades to 0.874 —
   the failure signature exists and appears only supercritical.
R4 JITTER: the JORDAN CERTIFICATE IS JITTER-IMMUNE (p = 0.994 even at sigma=0.15 rad:
   the secular t-envelope of revival peaks does not depend on ladder size) — what
   jitter kills is the TRANSCENDENCE EVIDENCE: amplitude collapses (529 -> 13.6) and
   the effective ladder shrinks to m_eff ~ 1/sigma (50/20/7). Nuance to carry into
   any experimental design: p-fit tolerant, comb/cusp (the Lerch content) fragile.

## Kill hierarchy (design guidance, [DERIVATION])
For the transcendental-class evidence (many-rung comb): phi stability first
(m_eff ~ 1/sigma_phi), detector bandwidth second (m_eff ~ n_det), colored ASE third
(mild), dispersion last (subcritical at the #029 fiber design). For the Jordan
certificate alone (p-fit): robust to ALL four layers at the tested scales.

## Self-audit catches this build
1. Dispersion model placement (static weight phase -> frequencies): fixed, signature
   now exhibited. 2. R2 width expectation prefactor (cusp heuristic 4/M misapplied;
   Dirichlet half-width ~ 0.6*2pi/M_eff; the 1/M_eff SCALING is the claim): corrected.
   (Plus 3 patcher/escaping bugs during the build, process-level, fixed.)

## To confirm on machine (blocking)
1. Re-run; check R1 24 sigma, R2 scaling, R3 0.025/0.069/0.146 + p=0.874, R4 p-immunity.
2. Engrave #031; update kickoff + MILO.
3. Queue unchanged: datasheet mapping, mock-modularity shielding, judge H2 next session.

## MACHINE CERTIFIED (2026-07-03) — status upgraded to [ESTABLISHED machine]
Scope (calibrated per #030 PRECISION): established = extractability IN SIMULATION with
four realistic-noise layers, all magnitudes dimensionless knobs; the hardware bridge
stays gated behind the datasheet mapping. Machine run = sandbox digit-for-digit
(realistic_machine_20260703.txt): R1 colored ASE 24/76/335 sigma at SNR=3/10/30
(100 avg), mirror 1.144e-2 vs 1.026; R2 p robust to n_det=15, first-revival width
0.025->0.321 (1/M_eff scaling holds, Dirichlet prefactor shown); R3 design-scale flat,
EXAGGERATED c2*M^2/kap=4.5 gives late-revival broadening 0.025/0.069/0.146 (k=0,2,4)
and p=0.874 — failure signature exists, appears only supercritical; R4 JORDAN
CERTIFICATE JITTER-IMMUNE (p=0.994 at sigma=0.15) while amplitude collapses 529->13.6
and m_eff ~ 1/sigma (50/20/7): jitter kills the TRANSCENDENCE EVIDENCE, not p.
KILL HIERARCHY (design guidance): phi stability > detector bandwidth > colored ASE >
dispersion (subcritical at #029 design). Registry #031 engraved.

## PRECISION 2 (2026-07-03, post external audit — hierarchy status split)
[ESTABLISHED machine]: the kill MECHANISMS and their m-scalings (jitter: Gaussian
exp(-m^2 sigma^2/2) kills high-m first; detector: truncation m_eff ~ n_det; colored
ASE: SNR degradation only; dispersion: requires supercriticality c2 M^2/kap > ~1),
AND the observed ordering WITHIN THE EXPLORED WINDOW of knob values.
[CONJECTURE until datasheet]: the ordering for any REAL device — it depends on the
relative magnitudes of the knobs (e.g. tiny jitter + poor detector reorders it).
"Protect the loop phase first" is design guidance conditional on the explored window,
prescriptive only after the datasheet mapping.
