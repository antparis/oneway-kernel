# FINDINGS 2026-07-14 — Corrigendum core (#058): repaired theorem certified

Status: [ESTABLISHED machine + judge]. 9/9 SymPy exact clauses. Sandbox and
Anthony's machine identical. Scope: LTI systems, complete kernel, calibrated
bilinear form C. Q1 (size cone) and Q2 (monodromy witness) QUARANTINED --
not part of this battery, per Q3 arbitration.

## What this certifies
J1  The four R/Delta quadrants are symbolically REALIZED, not merely
    conjectured: Q-RH (R=0,Dl=0), Q-C1 (R=0,Dl!=0, dissipative reciprocal),
    Q-DEC (R!=0,Dl=0, historical decoy), Q-OW (R!=0,Dl!=0, one-way).
J2  Operator identity (L^-1)^sharp = (L^sharp)^-1, generic 2x2 symbolic,
    A^sharp = C^-1 A^T C.
J3  L = L^sharp ==> K = K^sharp (kernel-level reciprocity), constructed via
    L = C_sym^-1 * Sigma with Sigma symmetric AND C symmetric (physical
    requirement B(u,v)=B(v,u) -- a non-symmetric C broke this clause in
    sandbox, fixed, see bugs below).
J4  Covariance: R' = U R U^-1 under simultaneous L,K,C transform by U.
J5  PROJECTION BLINDNESS, exact: diag(R) == 0 IDENTICALLY (C=I case) while
    R_offdiag = k12 - k21 generically nonzero. A same-port probe a^T R a
    can NEVER witness non-reciprocity -- proves the "complete kernel"
    requirement is not a caveat, it is structural. Echoes the project's
    two-point law (#026 onward: the living target is two-point).
J6  Onsager-Casimir distinction, exact: K_b^sharp == K_{-b} (device vs
    bias-reversed device) while K_b - K_b^sharp = 2b*antisym != 0 (device
    vs itself). These are two DIFFERENT comparisons; conflating them is a
    literature-adjacent trap the corrigendum must flag explicitly.

## Bugs caught in sandbox before delivery (both fixed, both instructive)
1. First J3 attempt used a generic (non-symmetric) C in L = C^-1*Sigma:
   FAILED. Root cause: the reciprocity bilinear form B(u,v) = u^T C v must
   be symmetric by physical definition (B(u,v)=B(v,u)); a non-symmetric C
   is not a valid reciprocity form to begin with. Fixed by using C_sym.
   Lesson: a judge failure can mean the TEST was physically ill-posed, not
   that the theorem is wrong -- diagnose before rewriting the claim.
2. (Same family as #057's simultaneous=True lesson.) S_swap uses
   subs(..., simultaneous=True) throughout; verified no sequential-subs
   trap reintroduced.

## What this does NOT do
Does not touch the sealed v3 (Zenodo 10.5281/zenodo.21317960). Does not
certify Q1 (size cone, still [DERIVATION]) or Q2 (monodromy witness, still
[DERIVATION], orientation-transport unverified). Does not write the
corrigendum text itself -- this FINDINGS certifies the MATHEMATICAL CORE
the corrigendum will cite.

Traces: judge_repair_058.py (sha256 e39a0d2b...), IDEAS_REGISTRY.md #058.
