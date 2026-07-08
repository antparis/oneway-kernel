#!/usr/bin/env python3
"""Patch v2 for oneway_kernel_paper.tex (2026-07-05).

Adds: (1) EP-sensing positioning paragraph at end of Sec. 1.3;
      (2) Dietz-2007 prior-work shielding paragraph at end of Sec. 3.5;
      (3) four source-verified bibitems (Langbein2018, Wiersig2020,
          LauClerk2018, Dietz2007) in appearance order.
Changes NOTHING else. Writes oneway_kernel_paper_v2.tex; the original is
never modified. Aborts without writing if any anchor is not found exactly
once.
"""
import sys, os

SRC = "oneway_kernel_paper.tex"
DST = "oneway_kernel_paper_v2.tex"

INSERT1 = r"""Beyond the forcing question itself, the proposed protocol bears on an open
experimental debate in exceptional-point (EP) sensing. The claimed sensitivity
enhancement of EP-based sensors has been challenged on noise
grounds~\cite{Langbein2018,Wiersig2020}, and fundamental-limit analyses have
shown that non-reciprocity --- rather than EP proximity per se --- is the
resource that allows a sensor to exceed the bounds constraining any reciprocal
device~\cite{LauClerk2018}. Both strands of that debate presuppose the ability
to certify, in operation and under realistic noise, (i) that a device is
genuinely defective (a Jordan-block degeneracy rather than a near-degenerate
diagonalizable pair) and (ii) that it is genuinely non-reciprocal. The
time-domain observables proposed here address precisely these two
certification tasks at low cost: the secular exponent of the revival envelope
is a direct witness of Jordan structure which our simulations indicate is
robust to loop-phase jitter and between-shot noise (Section~\ref{sec:noise}),
and the single-versus-twin revival comb is a direct witness of broken
reciprocity. We emphasize that these are certification tools; no
sensitivity-enhancement claim is made or implied.

"""

INSERT2 = r"""Time-domain signatures of defective degeneracies also have an experimental
precedent: Dietz \emph{et al.} observed the algebraic-times-exponential decay
(a $t^{2}$ intensity dependence) predicted at an exceptional point of a
dissipative microwave billiard~\cite{Dietz2007}. Relative to that precedent,
the present proposal differs in the platform (a recirculating fiber loop read
on an oscilloscope rather than a microwave cavity), in the observable set (the
secular envelope is combined with a phase-swept revival comb and a
single-versus-twin-comb reciprocity test, which the billiard setting does not
probe), and in the object being certified (the kernel-level deletion of the
exchange-Hermitian mirror partner by one-way coupling, certified symbolically
upstream). The secular envelope itself is therefore not claimed as new; its
use as a cheap, noise-robust certification channel for one-way kernels is.

"""

BIB_SENSING = r"""\bibitem{Langbein2018}
W. Langbein,
\emph{No exceptional precision of exceptional-point sensors},
Phys. Rev. A \textbf{98}, 023805 (2018).

\bibitem{Wiersig2020}
J. Wiersig,
\emph{Review of exceptional point-based sensors},
Photonics Res. \textbf{8}, 1457--1467 (2020).

\bibitem{LauClerk2018}
H.-K. Lau and A. A. Clerk,
\emph{Fundamental limits and non-reciprocal approaches in non-Hermitian quantum sensing},
Nat. Commun. \textbf{9}, 4320 (2018).

"""

BIB_DIETZ = r"""\bibitem{Dietz2007}
B. Dietz, T. Friedrich, J. Metz, M. Miski-Oglu, A. Richter, F. Sch\"afer,
and C. A. Stafford,
\emph{Rabi oscillations at exceptional points in microwave billiards},
Phys. Rev. E \textbf{75}, 027201 (2007).

"""

# (anchor, text inserted immediately BEFORE the anchor)
PATCHES = [
    (r"\subsection{Outline}", INSERT1),
    (r"\subsection{Cousins of the forcing question}", INSERT2),
    (r"\bibitem{Gardiner1993}", BIB_SENSING),
    (r"\bibitem{BCOV1994}", BIB_DIETZ),
]

def main():
    if not os.path.exists(SRC):
        sys.exit(f"ABORT: {SRC} not found in current directory. Nothing written.")
    if os.path.exists(DST):
        sys.exit(f"ABORT: {DST} already exists. Remove it first. Nothing written.")
    text = open(SRC, encoding="utf-8").read()

    # Verification pass: every anchor exactly once, no new cite keys already present
    ok = True
    for anchor, _ in PATCHES:
        n = text.count(anchor)
        print(f"anchor {anchor!r}: found {n} time(s)")
        if n != 1:
            ok = False
    for key in ("Langbein2018", "Wiersig2020", "LauClerk2018", "Dietz2007"):
        n = text.count(key)
        print(f"new key {key!r}: pre-existing occurrences = {n}")
        if n != 0:
            ok = False
    if not ok:
        sys.exit("ABORT: anchor/key verification failed. Nothing written.")

    before_lines = text.count("\n")
    before_bib = text.count(r"\bibitem{")
    out = text
    for anchor, insert in PATCHES:
        out = out.replace(anchor, insert + anchor, 1)

    open(DST, "w", encoding="utf-8").write(out)
    after_lines = out.count("\n")
    after_bib = out.count(r"\bibitem{")
    print("--- REPORT ---")
    print(f"lines: {before_lines} -> {after_lines} (+{after_lines - before_lines})")
    print(f"bibitems: {before_bib} -> {after_bib} (expected {before_bib} -> {before_bib + 4})")
    for key in ("Langbein2018", "Wiersig2020", "LauClerk2018", "Dietz2007"):
        print(f"key {key}: cite+bibitem occurrences in v2 = {out.count(key)}")
    print(f"WROTE {DST}. Original {SRC} untouched.")

if __name__ == "__main__":
    main()
