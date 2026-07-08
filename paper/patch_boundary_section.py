#!/usr/bin/env python3
"""Boundary-section patch for oneway_kernel_paper_v2.tex (2026-07-05, rev2).

Adds: (1) subsection "Boundary structure of the kernel" (machine result #039)
          at the end of Sec. 2; (2) one pointer sentence in open question 3.
Purely additive. Reads oneway_kernel_paper_v2.tex, writes
oneway_kernel_paper_v2b.tex; source never modified. Aborts without writing
on any anchor problem; on abort, prints the REAL file lines around the
target so the anchor can be fixed from facts, not guesses.
"""
import sys, os, re

SRC = "oneway_kernel_paper_v2.tex"
DST = "oneway_kernel_paper_v2b.tex"

SUBSECTION = r"""\subsection{Boundary structure of the kernel}
\label{sec:boundary}

The closed form of Section~\ref{sec:closedform} converges on the open unit
polydisk $|x| < 1$, $x = \zbone\wbtwo$, and the proposed protocol reads its
boundary values. Three structural facts about this boundary are worth
recording; all are verified numerically in the repository accompanying this
deposit. First, the boundary is intrinsic and dimensionless: it sits at the
pure number $|x| = 1$, fixed by the geometry of the mode sum rather than by
any parameter choice (the physical rates $\kappa$ and $\delta$ enter the
complex offset $c$, not the location of the boundary), and the formalism
contains no dimensional constant from which any other distinguished scale
could be built. Second, the boundary is emergent in the mode ladder: every
truncation of the sum to $N$ rungs is an entire function of $x$ with no
boundary at all, while the radius at which the truncated sum departs from
the closed form approaches $|x| = 1$ monotonically as $N$ grows (at the
one-percent level, the departure radius is $0.904$ at $N = 10$ and $0.991$
at $N = 30$, and lies within $10^{-6}$ of the boundary beyond
$N \simeq 100$). The boundary is therefore a property of the infinite
ladder that no finite sub-ladder carries --- the domain-level analogue of
the fact, used throughout this section, that the one-way structure lives in
the full ladder rather than in any single Jordan pair. Third, the closed
form continues analytically beyond the boundary, where the defining series
diverges: the kernel as a function outlives the kernel as a mode sum, at
the price of a branch structure on $x \in (1, \infty)$ whose leading
discontinuity is inherited from the dilogarithm ($2\pi i \ln x$; we
verified the dilogarithm discontinuity numerically to nine digits, and
state the kernel-specific jump at the level of the Lerch-to-dilogarithm
reduction rather than as an independently certified result). We record
these facts as a structural characterization only: they sharpen, but do
not close, the boundary-limit question of Section~\ref{sec:discussion},
since a rigorous treatment of the $|x| \to 1$ limit in the presence of the
complex offset remains open.

"""

POINTER = (" A structural characterization of this boundary --- its intrinsic,"
           " dimensionless location, its emergence under truncation of the mode"
           " ladder, and the analytic continuation and branch structure beyond"
           " it --- is given in Section~\\ref{sec:boundary}; the rigorous limit"
           " statement remains open.")

ANCHOR_SUBSEC = r"\section{Relation to prior structures}"
RE_OQ3 = re.compile(r"would\s+strengthen\s+Section~\s*\\ref\{sec:platform\}\s*\.")

def main():
    if not os.path.exists(SRC):
        sys.exit(f"ABORT: {SRC} not found. Nothing written.")
    if os.path.exists(DST):
        sys.exit(f"ABORT: {DST} already exists. Remove it first. Nothing written.")
    text = open(SRC, encoding="utf-8").read()

    ok = True
    n = text.count(ANCHOR_SUBSEC)
    print(f"anchor (subsection point): found {n} time(s)")
    if n != 1:
        ok = False
    hits = RE_OQ3.findall(text)
    print(f"anchor (open-q3 regex, wrap-tolerant): found {len(hits)} time(s)")
    if len(hits) != 1:
        ok = False
        print("  DIAGNOSTIC -- real file lines containing 'strengthen' or 'sec:platform':")
        for i, line in enumerate(text.splitlines(), 1):
            if "strengthen" in line or "sec:platform" in line:
                print(f"    L{i}: {line}")
    n = text.count("sec:boundary")
    print(f"new label 'sec:boundary': pre-existing occurrences = {n}")
    if n != 0:
        ok = False
    if not ok:
        sys.exit("ABORT: anchor/label verification failed. Nothing written.")

    before = text.count("\n")
    out = text.replace(ANCHOR_SUBSEC, SUBSECTION + ANCHOR_SUBSEC, 1)
    out = RE_OQ3.sub(lambda mo: mo.group(0) + POINTER, out, count=1)
    open(DST, "w", encoding="utf-8").write(out)
    after = out.count("\n")
    print("--- REPORT ---")
    print(f"lines: {before} -> {after} (+{after - before})")
    print(f"'sec:boundary' occurrences in output (expect 2): {out.count('sec:boundary')}")
    print(f"WROTE {DST}. Source {SRC} untouched.")

if __name__ == "__main__":
    main()
