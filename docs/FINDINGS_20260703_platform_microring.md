# FINDINGS 2026-07-03 — platform mapping: the #027 kernel on a photonic microring

STATUS: [HEURISTIQUE sandbox] — machine re-run pending. The closed form is the
ALREADY machine-judged #027 Lerch kernel; the new content is the platform mapping,
the theta1+theta2 law, the chiral-feedback-bus mechanism, and the lab observables.
No new judge claim. Physical-units mapping stays [CONJECTURE] until a real device
parameter set is put in.

## Mechanism [DERIVATION] — answers the OPEN selection-rule question of the
## RESEARCH_NOTE (single-L modulation serves one pair only)
CHIRAL FEEDBACK BUS: microring + add-drop bus + isolator loop re-injecting the CW
output onto the CCW input. (i) every azimuthal pair (+m,-m) is degenerate and couples
to the SAME bus => equal diagonals per m AUTOMATIC => per-m Jordan WITHOUT fine-tuning;
(ii) the isolator kills the reverse path => G12 = 0 structurally; (iii) the loop delay
gives g_m = g0 e^{i m phi} (phi = FSR*tau) => the #027 ladder, all rungs served by ONE
loop. Tabletop-compatible (ring + fiber loop + isolator).

## Command
    python3 platform_microring_kernel.py     (fast, pure numpy+mpmath)

## Sandbox results (platform_sandbox_20260703.txt)
[1] per-m: reverse entry exactly 0; phase rigidity 0.00 (Jordan by construction).
[2a] SIGNATURE LAW: the one-way conversion kernel is a function of theta1+theta2 ONLY
     (rel spread 1.4e-16 varying the difference at fixed sum). Reciprocal channels
     live on theta1-theta2. Fourier-separating the two sectors of the measured
     two-point map IS the experiment.
[2b] QUANTITATIVE IDENTITY: the platform ladder sum equals the #027 lerchphi closed
     form at |x|=1 to 1.4e-7 (after fixing a sign error in Im(c) — audit catch #1:
     lam_m = -i*dlt*(m+c) gives c = -Delta/dlt - i*kappa/(2*dlt)).
[2c] M-convergence 200->400: 1.5e-5.
[3i] Exchange-Hermiticity: one-way residual 2.05 (NON-Hermitian); reciprocal control
     exactly 0 (Hermitian). The #027 K3 leg is measurable on the platform.
[3ii] Ladder vs single-pair EP: 21 Fourier tones vs 1 — the transcendental class
     REQUIRES the ladder; a single chiral EP (Yang/Wiersig-type alone) cannot give it.
[4] LINESHAPE: boundary value of Li_2/Lerch = Clausen-family CUSP at
     theta1+theta2 = phi. Audit catch #2 (own expectation broken): kappa enters as a
     COMPLEX OFFSET, not an exponential cutoff — the cusp is mathematically SHARP;
     its measured width COUNTS the served rungs: width ~ 4/M_max (verified: 0.0252 /
     0.0096 / 0.0032 rad at M = 150/400/1200). Off-resonance kappa has weak effect;
     the strong knobs are M_max (width, set by bus bandwidth/dispersion) and Delta
     (which rung resonates). FWHM was the wrong descriptor (audit trail kept).

## Lab-facing summary [DERIVATION]
Measure the two-point angular response (two ports / two near-field probes; add-drop
heterodyne as the report recommends). Fourier-split into (theta1-theta2) [reciprocal]
and (theta1+theta2) [one-way] sectors. In the sum-sector: a sharp Clausen cusp at the
loop phase, width ~ 4/(number of served rungs), exchange-non-Hermitian. That lineshape
IS the boundary value of the machine-judged #027 Lerch kernel.

## To confirm on machine (blocking)
1. Re-run platform_microring_kernel.py; check [2a] 1e-16, [2b] MATCH 1e-7, controls.
2. Then engrave #028 (platform mapping + chiral-feedback-bus mechanism + theta1+theta2
   law + cusp-counts-rungs law) and update kickoff + MILO.
3. Next [CONJECTURE step]: real-device parameter sheet (Si3N4 or SiO2 microring FSR,
   loaded kappa, isolator loop loss) -> visibility estimate; only then any contact
   with an experimental group.

## MACHINE CERTIFIED (2026-07-03) — status upgraded to [ESTABLISHED machine]
Machine run = sandbox digit-for-digit (platform_machine_20260703.txt): per-m Jordan by
construction (rigidity 0.00, reverse entry exactly 0); theta1+theta2 law rel spread
1.4e-16; QUANTITATIVE IDENTITY ladder = #027 lerchphi boundary to 1.37e-7; exchange-
Hermiticity 2.047 (one-way) vs 0.000 (reciprocal); 21 Fourier tones (ladder) vs 1
(single chiral EP — insufficient for the transcendental class); cusp width ~4/M
(0.0252/0.0096/0.0032 at M=150/400/1200), kappa = complex offset, no width effect
off-resonance. HYGIENE: one stale print line ("width kappa/FSR") in the [reading]
block contradicted the established finding — fixed post-run (see script); the FINDINGS
body above was already correct. Registry #028 engraved. NEXT [CONJECTURE step]:
real-device parameter sheet (FSR, loaded kappa, isolator loop loss) -> visibility.
