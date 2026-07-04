# FINDINGS 2026-07-03 — noisy time-domain simulation of the #029 protocol

STATUS: [HEURISTIQUE sandbox] — machine re-run pending. Protocol model [DERIVATION];
no judge claim (no new field formula). Origin: the ONE new valid item of the external
(Grok) audit — the kernel was machine-validated in frequency (#028), the real-time
NOISY measurement chain was not.

## Model [DERIVATION]
At fixed ports, the CCW impulse response of the chiral-feedback-bus ring is
  E(t) = g0 * t * e^{-kap t/2} * D_M(phi - dlt*t)
(Dirichlet revival comb carried by the SECULAR t-envelope — the Jordan certificate).
Diagonalizable control: no t-prefactor (p = 0). Reciprocal control: the mirror partner
appears as a TWIN comb at the mirrored phase — the mirror-deletion law becomes an
oscilloscope observable (single comb vs twin combs).

## Command
    python3 protocol_time_domain_sim.py    (numpy only, ~1 min)

## Sandbox results (protocol_sandbox_20260703.txt)
[0] Noiseless sanity: revivals exactly at t_k = (phi + 2*pi*k)/dlt; Jordan exponent
    p = 1.000 +- 0.000 vs control 0.000 +- 0.000; kappa_hat = 0.200 (true 0.2);
    mirror ratio 4.7e-4 (one-way) vs 1.03 (reciprocal).
[X1] Jordan discrimination under noise (fit p in t^p e^{-kap t/2} over revival peaks):
    single shot: SNR=10 -> p = 0.86 +- 0.09 (10 sigma from p=0); SNR=30 -> 30 sigma.
    100 averages: even SNR=3 -> p = 0.975 +- 0.026 (37 sigma). LAB-TRIVIAL.
    Honest note: low-SNR single-shot biases p LOW (0.37 at SNR=3) — noise biases peak
    picking; averaging removes it; reported as-is.
[X2] phi-sweep (piezo stretcher): slope dt1/dphi = 0.9996 (expect 1/dlt), residual 1.4e-3.
[X3] Mirror test at SNR=10, 100 avg: one-way 1.2e-2 vs reciprocal 1.03 — two orders
    of separation. The #026/#027 mirror-deletion law is directly measurable.

## Reading
All three protocol checks (secular envelope, revival comb + phi-sweep, mirror test)
are EXTRACTABLE at lab-accessible SNR with standard oscilloscope averaging. Combined
with #029 (V = 3.3e-2, conv ratio 0.81 on the fiber ring), the measurement chain is
complete on paper: device + protocol + noise budget.

## To confirm on machine (blocking)
1. Re-run; check [0] exact, X1 sigma table, X2 slope, X3 ratios.
2. Engrave #030; update kickoff + MILO.
3. Remaining before experimental contact (unchanged queue): datasheet re-check,
   ASE bound modeling (SOA), mock-modularity shielding; judge-hardening H2 next session.

## MACHINE CERTIFIED (2026-07-03) — status upgraded to [ESTABLISHED machine]
Machine run = sandbox digit-for-digit (protocol_machine_20260703.txt). Noiseless:
p=1.000+-0.000 (Jordan) vs 0.000+-0.000 (diagonalizable), kappa_hat=0.200, revivals
exact, mirror 4.66e-4 vs 1.03. Under noise: single-shot SNR=10 -> 10.0 sigma Jordan
discrimination; SNR=3 with 100 scope averages -> 37.2 sigma (lab-trivial). Phi-sweep
slope 0.9996 (expect 1). Mirror test at SNR=10/100avg: one-way 1.226e-2 vs reciprocal
1.025 — two orders: the #026/#027 MIRROR-DELETION LAW IS AN OSCILLOSCOPE OBSERVABLE
(single comb vs twin combs). Known bias traced: low-SNR single-shot peak-picking
biases p low; averaging removes it. Registry #030 engraved. Measurement chain now
complete WITH noise budget: #027 math -> #028 mechanism -> #029 device -> #030 protocol.

## MACHINE CERTIFIED (2026-07-03) — status upgraded to [ESTABLISHED machine]
Machine run = sandbox digit-for-digit (protocol_machine_20260703.txt). Noiseless:
p=1.000+-0.000 (Jordan) vs 0.000+-0.000 (diagonalizable), kappa_hat=0.200, revivals
exact, mirror 4.66e-4 vs 1.03. Under noise: single-shot SNR=10 -> 10.0 sigma Jordan
discrimination; SNR=3 with 100 scope averages -> 37.2 sigma (lab-trivial). Phi-sweep
slope 0.9996 (expect 1). Mirror test at SNR=10/100avg: one-way 1.226e-2 vs reciprocal
1.025 — two orders: the #026/#027 MIRROR-DELETION LAW IS AN OSCILLOSCOPE OBSERVABLE
(single comb vs twin combs). Known bias traced: low-SNR single-shot peak-picking
biases p low; averaging removes it. Registry #030 engraved. Measurement chain now
complete WITH noise budget: #027 math -> #028 mechanism -> #029 device -> #030 protocol.

## PRECISION (2026-07-03, post external audit — scope of the #030 claim)
What #030 ESTABLISHES (machine): extractability of the three protocol checks in a
SIMULATION with ADDITIVE WHITE noise on the #029 design model. What it does NOT
establish: behavior on a real device (structured SOA ASE, photodetector response,
time-domain loop dispersion, thermal drifts). Accurate phrasings: "the mirror-deletion
law is PREDICTED to be an oscilloscope observable, demonstrated extractable in
simulation"; "chain complete AT DESIGN/SIMULATION LEVEL". The [ESTABLISHED machine]
tag certifies the executed simulation, per registry convention (#021-#029); the
physical-reality claim remains gated behind the OPEN queue (datasheet, ASE model,
experiment). Next build (merges our ASE queue item + audit option 3): realistic-noise
version (structured ASE spectral density + noise figure, detector bandwidth/response,
loop dispersion in time domain).
