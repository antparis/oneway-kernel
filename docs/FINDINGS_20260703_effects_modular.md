# FINDINGS 2026-07-03 — modular effects simulator (4 master switches, typ/stress)

STATUS: [HEURISTIQUE sandbox] — machine re-run pending. All effect magnitudes are
literature-typical/catalogue [CONJECTURE-grade] (RESEARCH_NOTE_20260703_noise_budget.md);
the machine run certifies the SIMULATION and the instrument behavior, not the values.

## Architecture (report-derived, within-record vs between-shot wired in)
A LOOP PHASE (thermal+acoustic+vibration, between-shot: jitter sigma + slow drift):
  typ sig=0.05/drift=0.5 rad; stress sig=1.0/drift=10 rad.
B INTENSITY (EDFA RIN within-record + gain jitter shot-to-shot): typ rin=0.10/gj=0.02;
  stress 0.30/0.10.
C POLARIZATION (SOP x PDL slow fading): typ 0.05; stress 0.20.
D REFLECTIONS (finite isolation => GENUINE weak twin comb injected): typ amp 1e-2
  (40 dB); stress 3.2e-2 (30 dB).
E NEGLIGIBLE (Kerr 2.6e-5 rad/turn; beta3/beta2 1e-3): switches off, justified.
Explicit 100-shot loop (drift/fading break the fixed-signal shortcut).
Observables per scenario: p, first-peak amplitude, m_eff (first-revival width metric),
mirror energy ratio, DETECTION flag (p & mirror marked INVALID when comb undetected).

## Sandbox results (effects_sandbox_20260703.txt)
Baseline: p=0.992+-0.005, m_eff=49, mirror=2.0e-3 (noise floor), det=69.
A TYP: comb damaged (m_eff 17, amp /8) and MIRROR POLLUTED x10 (2.1e-2) — p INTACT
  (0.982). A STRESS: comb dead, det=1.0 -> INVALID flagged (instrument refuses).
B/C/D typ AND stress: p, comb, amplitude intact; D STRESS mirror 2.6e-3 barely above
  the 2e-3 noise floor (the injected 1e-3 floor is masked unless the loop is
  phase-quiet). ALL TYPICAL: A dominates (m_eff 11, det 10, p 1.033 valid).
ALL STRESS: INVALID (comb dead).

## Findings of the grid
1. SIMULATED HIERARCHY CONFIRMS THE REPORT: A (loop phase) >> B ~ C ~ D. Protect the
   loop phase first — now grounded across the full 10-effect set, not just #031's R4.
2. NEW: phase jitter POLLUTES the mirror test (~10x) well BEFORE killing the comb —
   X3 degrades before X1; resolving the isolation floor (D) requires a phase-quiet loop.
3. p remains immune to every between-shot effect at every tested level (jitter, drift,
   fading, gain jitter, reflections); within-record RIN at stress (30%) leaves p at
   0.989+-0.015. The Jordan certificate is the robust observable of the protocol.
4. Instrument honesty: two audit fixes during the build — m_eff by revival width (FFT
   bin counting was noise-polluted) and a detection-validity flag (p & mirror INVALID
   on a dead comb; an instrument must refuse to report on a dead signal).

## Commands
    python3 protocol_effects_modular.py     (numpy, ~2-3 min, explicit 100-shot loops)

## To confirm on machine (blocking)
1. Re-run; check grid digit-for-digit (seeds fixed).
2. Engrave #034; update kickoff + MILO.
3. Queue: paper duo (mock shielding + standard translation) = next session main build;
   H1/H3 judge patches (one per session); measured component values when hardware.

## MACHINE CERTIFIED (2026-07-04 00h, dated 20260703 per session) — [ESTABLISHED machine]
Machine run = sandbox digit-for-digit (effects_machine_20260703.txt), fixed seeds,
11 scenarios. Scope: SIMULATION + instrument behavior established; effect magnitudes
literature-typical [CONJECTURE-grade] (RESEARCH_NOTE_20260703_noise_budget.md),
replaced by measured values when hardware exists (option-1 decision).
GRID: baseline p=0.992+-0.005/m_eff=49/det=69; A phase TYP: comb damaged (m_eff 17,
amp /8), MIRROR POLLUTED x10 (2.07e-2), p INTACT 0.982; A STRESS + ALL STRESS:
comb dead, det~1, p & mirror flagged INVALID (instrument refuses); B/C/D typ AND
stress: everything intact (RIN 30% leaves p at 0.989+-0.015); ALL TYPICAL: A
dominates (m_eff 11, det 10, p 1.033 valid).
THREE GRID FINDINGS: (1) simulated hierarchy CONFIRMS the report: A (loop phase) >>
B ~ C ~ D — "protect the loop phase first" now grounded on the full 10-effect set;
(2) NEW: phase jitter pollutes the MIRROR test ~10x BEFORE killing the comb — X3
degrades before X1; resolving the isolation floor requires a phase-quiet loop;
(3) p is the ROBUST observable: immune to every between-shot effect at every level.
Registry #034 engraved.
