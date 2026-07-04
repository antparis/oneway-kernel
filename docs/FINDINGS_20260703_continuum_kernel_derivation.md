# FINDINGS 2026-07-03 — continuum one-way kernel DERIVED (the #026 remaining lock)

STATUS: [HEURISTIQUE sandbox] — machine (real judge_v2 certify_2field) arbitrates the
classification. The derivation itself is [DERIVATION], verified coefficient-wise by
partial sums (40 terms, 2 points, geometric tail bound). Forcing of the weights is
inherited from #021 (Lindbladian one-way, Jordan double pole); the ring/edge mode
family is a stated modeling choice; the x = zbar*wbar pairing follows from the
contra-winding bookkeeping itself (downstream -n at observation, conj of +n at source),
not from an adjustable choice.

## What was derived (not inherited)
Spatial contra-winding ring/edge families (outer chiral +n, inner counter-chiral -n),
one-way Metelmann-Clerk coupling per n (awake — consistent with #020 passive dilemma
vs #021 escape), Jordan ladder lam_n = -kappa/2 - i n delta, G21 = k/lam_n^2, G12 = 0.
One-way cross kernel K = sum_{n>=1} g_n x^n with x = zbar*wbar:
 (a) flat weights      -> k x/(1-x)                       [algebraic corner control]
 (b) 1/n toy weights   -> -k log(1-x)                     [log class]
 (c) PHYSICAL Jordan   -> -(k/delta^2)[lerchphi(x,2,c) - 1/c^2], c = kappa/(2 i delta)
                          [LERCH transcendent, leading Li_2 — BEYOND log]
Series checks: ALL MATCH (a,b,c). Convergence: |x| < 1 (inside the ring), stated.

## Battery upgraded twice during the build (audit catches)
1. cross-disc now covers ALL FOUR pairings (z,w),(z,wbar),(zbar,w),(zbar,wbar) by
   numeric central FD on log K (symbolic diff of undefined lerchphi cannot lambdify —
   pitfall). #026's single-pairing test was incomplete.
2. NEW LEG — exchange-Hermiticity, BRANCH-SAFE: K Hermitian iff K = fc2f(swap(K)) up to
   a constant, tested via constancy of exp(Delta) (a +-i*pi log-branch constant flips
   sign pointwise, raw spread ~ pi; exp(Delta) = -1 exposes it). mpmath.taylor on
   lerchphi unstable (pitfall) -> partial-sum verification instead.

## Sandbox results (continuum_sandbox_20260703.txt)
ONE-WAY kernels: (b) log and (c) Lerch PASS the kernel gate v2 (entangled on
(zbar,wbar) ONLY, non-paired, exchange-NON-Hermitian). (a) algebraic PASSES the gate
too — correct: the gate tests one-wayness+entanglement; TRANSCENDENCE is a separate
cube leg supplied by the physical ladder (c).
DECOYS: D1 Bergman -k log(1 - z*wbar) (reciprocal single-sector diagonal): HERMITIAN
exact -> FAIL (this decoy PASSED the #026 formula gate — the new leg was necessary).
D2 Hermitian paired sum: paired residual 0, HERMITIAN exact -> FAIL.
D3 inherited DRUM representative log(z - wbar): HERMITIAN up to BRANCH constant
(exp(Delta) = -1 constant) -> reciprocal-compatible -> FAIL.

## Consequence — #026 continuum representative CORRECTED (refinement of the OPEN lock,
## no contradiction of #026's established parts)
The true one-way continuum kernel lives on x = zbar*wbar (anti-anti pairing), NOT on
(z - wbar). The inherited DRUM form is reciprocal-compatible and was the WRONG
representative for one-wayness. The one-wayness signature at kernel level is
exchange-NON-Hermiticity (K12 = 0 has no mirror partner). The physical Jordan ladder
forces a LERCH/Li_2 transcendent: master-law legs for the derived (c) kernel:
NON-PAIRED (yes) + TRANSCENDENTAL (Lerch, yes) + NON-FACTORIZABLE (cross-disc != 0,
yes) — the 2-field target-corner candidate now carries a DERIVED form.
Measurability note stays [CONJECTURE].

## To confirm on machine (blocking)
1. Run continuum_kernel_derivation.py in the repo (real judge_v2): series checks ALL
   MATCH; three one-way PASS; three decoys FAIL with the exact Hermiticity labels.
2. Then engrave #027 (derived continuum kernel + corrected representative + new
   exchange-Hermiticity leg + Bergman decoy) and update the kickoff.
3. Judge-hardening queue grows: (a) narrow annuli grid; (b) 4-pairing cross-disc;
   (c) exchange-Hermiticity leg — one patch per session, next session.

## MACHINE CERTIFIED (2026-07-03) — status upgraded to [ESTABLISHED machine]
Machine run = sandbox digit-for-digit (continuum_machine_20260703.txt), real judge_v2.
Series checks ALL MATCH (a flat, b 1/n->log, c Jordan->Lerch). Three one-way kernels
PASS kernel gate v2 (entangled on (zbar,wbar) ONLY, non-paired, exchange-NON-Hermitian).
Three decoys FAIL: D1 Bergman HERMITIAN exact (this decoy passed the old #026 formula
gate — the exchange-Hermiticity leg was necessary); D2 paired sum residual 0, HERMITIAN;
D3 inherited DRUM rep log(z-wbar) HERMITIAN up to BRANCH constant (exp(Delta)=-1) =>
reciprocal-compatible => WRONG one-way representative, #026 continuum rep CORRECTED.
Derived physical form: K = -(k/delta^2)[lerchphi(zbar*wbar, 2, c) - 1/c^2],
c = kappa/(2 i delta) — LERCH/Li_2 transcendent, master-law legs all pass.
OPEN [CONJECTURE]: concrete physical platform (ring-edge family = stated modeling
choice) and measurability protocol. One-point target cell stays empty (#025);
the living target is TWO-POINT. Registry #027 engraved.
