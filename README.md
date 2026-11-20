# One-way transfer kernels: exchange non-Hermiticity and a proposed fiber-loop test

> **Status.** This repository accompanies a theoretical/numerical manuscript.
> All claims are at the level of **symbolically certified formula structure**
> (exact Wirtinger-derivative computation) and **numerical simulation** with
> literature-typical component values. **No experimental measurement has been
> performed.** "Certified" here means the symbolic structure was verified by the
> SymPy judge, never that any physical or cosmological statement is established.

## What this is

A study of when the anti-holomorphic (conjugate-variable) dependence of a
two-point transfer kernel is *forced* by the underlying open-system dynamics,
rather than removable by gauge, basis, or preparation. For two counter-winding
mode ladders coupled unidirectionally (reservoir-engineered, Lindblad-type,
per-pair Jordan structure), the transfer kernel sums to a closed form involving
the Lerch transcendent in the product of conjugated coordinates.
Exchange-Hermiticity and physical reciprocity are independent invariants.
Reciprocity is carried by `R = K - S(K)` evaluated on the complete matrix
transfer kernel; the scalar surviving element can be exchange-symmetric even
when the reverse matrix element vanishes. One-way coupling deletes the mirror
partner and independently makes `R != 0` on the complete kernel. A
recirculating-fiber-loop implementation and a time-domain measurement protocol
are proposed, with a noise/imperfection analysis and explicit falsifiability
criteria.

## Origin

This work extends the author's **eml★** program on the detection of
anti-holomorphic dynamics via symbolic regression. It is a **linked, separate
deposit** — not a merge into the eml★ record.

- eml★ paper (Zenodo): https://doi.org/10.5281/zenodo.20272784
- eml★ software (Zenodo): https://doi.org/10.5281/zenodo.20273262

## How to cite

Paper (all versions, always resolves to the latest):
https://doi.org/10.5281/zenodo.21195310

Current version: **v11** (2026-07-18), DOI: https://doi.org/10.5281/zenodo.21431359
(v3: 2026-07-12, DOI: https://doi.org/10.5281/zenodo.21317960; v1: 2026-07-04, DOI: https://doi.org/10.5281/zenodo.21195311)

> MONNEROT, A. (2026). *When is anti-holomorphic dependence forced? Exchange
> non-Hermiticity of one-way transfer kernels and a proposed time-domain test
> in a recirculating fiber loop* (Version 4.0, paper v11). Zenodo.
> https://doi.org/10.5281/zenodo.21431359

## Layout

- `paper/` — the manuscript (PDF + LaTeX source)
- `code/` — the SymPy certification judge and the simulation scripts underlying
  the certified claims (kernel derivation, platform identity check, time-domain
  protocol, realistic-noise and effects simulators)
- `docs/` — the dated FINDINGS files and detector rules that back each claim

## Certification discipline

A discoverer may propose; only the symbolic judge certifies. Every symbolic
statement in the paper is checked by exact Wirtinger-derivative computation
(`code/judge_v2.py` and the specialized pairing judge). Numerical evidence
supports but never replaces the symbolic certificates.

## AI assistance

The author, an independent researcher, used AI assistants as coding, auditing,
and drafting tools under a strict verification discipline: every symbolic claim
was certified by exact computation executed on the author's machine, and no
numerical result was produced or accepted without such execution. Responsibility
for the content rests with the author.

## License

MIT — see `LICENSE`.
