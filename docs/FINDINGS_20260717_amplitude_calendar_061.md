# FINDINGS 2026-07-17 -- #061 AMPLITUDE vs CALENDAR: decaying is not forgetting -- the paper's own sinc keeps an eternal calendar of exact zeros

Status: [ESTABLISHED machine + judge] -- SymPy-exact + far-window numeric
harness, 6/6 on Anthony's machine (ThinkCentre, 2026-07-17). The harness
IS the judge (exact residues, no hardcoded verdict).

## Origin
Seventh external adversarial audit (GPT-5.6) of paper v10: the reading
"absolutely continuous => the calendar is forgotten / the tear heals"
(paper Sec. 4.3, abstract, intro; inherited from the WORDING of registry
#049 Theorem 3) is refuted by the paper's own Eq. (6): the uniform
measure's transform is the cardinal sine, absolutely continuous, whose
AMPLITUDE dies (Riemann-Lebesgue, which #049 machine-faced) while its
ZEROS -- the deep rendezvous -- persist forever.

## What was tested (amplitude_calendar_test.py, sha256 1130c24dd71bfcac
7c734afd7b95efbd3db4896dfff5ec364b2bf2329466af87)
- J1  Sinc closed form: (e^{ibu}-e^{iau})/(iu(b-a)) ==
      e^{i(a+b)u/2} 2 sin((b-a)u/2)/(u(b-a)), residue 0.
- J2  Exact zeros at u_n = 2 pi n/(b-a) for every integer n (sin(pi n)=0).
- J3  Window contrast == 1 exactly on any window containing a zero;
      numeric face on [1/300, 1/3]: contrast 0.999999999999 at n = 10^3
      (u ~ 1.9e4) and 0.999999999554 at n = 10^6 (u ~ 1.9e7).
- J4  Finitely supported non-null cannot decay: N = 2 normalized
      transform returns EXACTLY to 1 at every u_k = 2 pi k/Dnu.
- J5  Independence on the same far windows: maximal amplitude falls by
      1001.5 (1/u predicts ~1000) while the contrast stays 1.

## Exact command
    cd ~/Desktop/oxieml-star && python3 amplitude_calendar_test.py

## Raw result
    6 PASS / 0 FAIL.

## Law graved
DECAYING IS NOT FORGETTING. Riemann-Lebesgue kills the AMPLITUDE of an
absolutely continuous transform; it decides neither the persistence of
zeros, nor the positions of minima, nor the relative window contrast.
A finitely supported non-null measure cannot decay (Bohr almost
periodicity). The correct dichotomy is an AMPLITUDE dichotomy:
finitely supported => almost periodic, no decay (except null);
absolutely continuous => amplitude tends to zero;
calendar persistence is a SEPARATE property, decided by neither class
alone (the uniform sinc: absolutely continuous AND eternal calendar).

## Semantic debt traced (append-only; originals untouched)
- #049 Theorem 3 WORDING "the continuum forgets the calendar and the
  tear heals at large scale": the theorem's mathematical content
  (mu_hat -> 0) is intact and machine-faced; the calendar-oblivion
  reading is superseded by this entry. The Bohr side of #049 is
  unaffected.
- Paper v10 carries the reading at four sites (abstract l.53, intro
  l.146, Sec. 4 opening l.639, Sec. 4.3 l.728-750); all rewritten as an
  amplitude dichotomy in v11 (build_v11.py).

## Credit
Counter-example: external adversarial audit (GPT-5.6, seventh round),
using the paper's own closed form. Reproduction: Cowork sandbox.
Arbitration: Anthony's machine.

## Scope
Window functionals of Fourier transforms of winding measures. Says
nothing about nature. Shared FORM, never identity.
