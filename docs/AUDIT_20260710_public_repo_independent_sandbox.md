# AUDIT 2026-07-10 — Independent-sandbox audit of the public oneway-kernel repository (pre-v3-deposit)

Auditor: Claude (cloud sandbox, Cowork session), read-only clone of
github.com/antparis/oneway-kernel at HEAD 9eddb97 (2026-07-10 20:43 +0200).
No file in the repository was modified (one-hand rule). All checks below were
EXECUTED in the sandbox, not reasoned. Status of every item: [ESTABLISHED
sandbox] — executed on an independent machine, NOT the author's machine and
NOT the SymPy judge pipeline; it certifies repository state and public
reproducibility, never physics.

## A. Kickoff claims verified on pieces (all PASS)

1. HEAD = 9eddb97, previous commit 5f445ad, history matches the five-session
   v3 plan (97abd73 -> ec11c80 -> 274a1a3 -> ddce800 -> 5c6e91a -> 5f445ad -> 9eddb97).
2. paper/oneway_kernel_paper_v3.pdf: 507,741 bytes, md5
   d3eea5fe94c8a7de5b7909404555dbc0, 18 pages (pdfinfo). Exact match.
3. Supplement present: docs/PROOF_20260710_fourier_floor_theorem.md = 127
   lines exactly; 4 FINDINGS (#048 floor law, #049 theorem, #050 closed
   floors, #051 inverse); 4 harnesses in code/ (ballast_law, theorem_companion,
   closed_floors, inverse).
4. Independent recompilation of oneway_kernel_paper_v3.tex (pdflatex
   1.40.25, two passes, figures present): 0 errors, 0 LaTeX warnings,
   18 pages, zero '??' in pdftotext. Compile-clean CONFIRMED on a second
   machine.
5. Citation closure: 28 \cite keys vs 28 \bibitem keys, sets identical in
   both directions — zero orphan refs/cites CONFIRMED independently.
6. Zenodo API: record 21286458 = version 2.0, publication_date 2026-07-10,
   conceptdoi 10.5281/zenodo.21195310, related_identifier isDerivedFrom
   10.5281/zenodo.20272784. Record 21195311 = version 1.0, 2026-07-04,
   intact, same concept and same isDerivedFrom. All as claimed.

## B. New result: the four public harnesses REPRODUCE on an independent machine

All four #048–#051 harnesses were run in the sandbox (python3, numpy/scipy/
sympy/mpmath installed from PyPI; every run exit=0, no timeout at 300 s):

- kernel_theorem_companion_test.py: MIDPOINT slope -2.00, ENDPOINT slope
  -1.02; Bohr atomic max = 1.000 on both windows; continuum proxy
  0.0605 -> 0.0216. Matches paper Section 4.2/4.3 digits exactly.
- kernel_inverse_test.py: mirror-blindness max |relief - mirrored| =
  5.66e-15 (paper says 5.7e-15 — rounding of the same number); short-window
  slow-needle error 29.42% -> long-window 0.02%. Matches Section 5.2.
- kernel_closed_floors_test.py: uniform/sinc floor 0.06533857 vs closed form,
  rel.diff 9.0e-10; identities (big-slow == linear-in-delta, big-fast ==
  sinc) reproduced. Matches Section 4.4.
- kernel_ballast_law_test.py: full battery runs, two-needle anchor exact,
  reciprocal X=0 confirmed.

Reading: an external reviewer cloning the public repo can reproduce every
Section 4–5 machine number from scratch on a fresh machine. This was not
previously verified outside the author's machine.

## C. Gap found (orthogonal-axis pass on commit 9eddb97's own claim)

Broken parameter: "the supplement backs every number in Sections 3–5"
(commit message of 9eddb97). Checked on pieces: FALSE for Section 3.

- Section 3.4 machine panels (period T = 94.247780; deep minima u = 10.00,
  29.98, 49.93, 69.81; spacing ~19.9; period law to 1.3e-3; first rendezvous
  x ~ 2.2e4) appear NOWHERE in code/ or docs/ — grep over the whole repo
  returns nothing. They are backed only by the #044 harness in the PRIVATE
  oxieml-star repository.
- Section 3.2 chiral-phase-law checks (1.1e-16–2.2e-16 at kappa = 0.05,
  0.2, 1.0; linear drift; family independence) likewise have no public
  FINDINGS or harness (boundary arc #039–#045 is private-only; docs/ jumps
  from the 2026-07-03 protocol era to the 2026-07-10 floor era).
- The paper itself promises (Outline, last sentence): "The certification
  details, the full proof of the floor theorem, the closed-form derivations,
  and the simulation parameters are provided as supplementary material in
  the repository accompanying this deposit." For Section 3 the simulation
  backing is not there. Same class of gap as the one already caught and
  fixed for the theorem proof before 9eddb97.

Severity: does not invalidate the paper (numbers were audited against the
registry on the author's machine); it weakens the public reproducibility
claim for Section 3 only. RECOMMENDATION: before or together with the v3
Zenodo deposit, add the boundary-arc harnesses + FINDINGS (#039–#041, #044,
#045) to code/ and docs/, or weaken the commit-message-level claim to
"Sections 4–5".

## D. Minor findings (author's call, none blocking)

1. \date{July 4, 2026} in oneway_kernel_paper_v3.tex is inherited from v1;
   a v3 deposited on 2026-07-10+ may want its own date (re-seal md5 if
   changed — this is exactly the re-read window, so now is the moment).
2. Section count bookkeeping: the kickoff says "9 sections"; the tex has 10
   numbered \section (Introduction ... Conclusion) plus 2 starred. No
   consequence; just keep future traces consistent.
3. code/ has no requirements.txt; the sandbox needed pip installs of sympy,
   mpmath, scipy (numpy preinstalled). A 4-line requirements.txt plus one
   README sentence ("each harness is standalone, python3 harness.py,
   < 5 min each") would lower the reviewer's cost to zero.
4. Post-deposit TODO (already implied by the v2 pattern, listed so it is not
   lost): bump README "How to cite" current-version block and consider a
   version field in CITATION.cff once the v3 DOI exists.
5. Paper 5.7e-15 vs harness 5.66e-15: same number, rounded; consistent with
   the text's wording. No action.

## E. What this audit does NOT cover

- The private oxieml-star registry (#001–#051) — unreachable from this
  sandbox; the 42-number registry audit of 5f445ad is taken as recorded,
  not re-verified.
- The author's re-read of abstract / contributions (i)–(vii) / Discussion
  opening / Section 3.4 — still the one pending gate before deposit.
- Any physical claim. Sandbox execution certifies repository state and
  reproducibility only.
