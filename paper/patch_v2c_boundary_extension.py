#!/usr/bin/env python3
"""v2c patch for oneway_kernel_paper_v2b.tex (2026-07-08).

Adds, purely additively:
 (1) TWO paragraphs extending the "Boundary structure of the kernel"
     subsection with the #040 (chiral tear) and #041 (localization-from-
     detuning) machine results, each with honest statuses and the
     prior-art shielding references identified by the anteriority report;
 (2) FOUR bibliography entries (LeeYang1952, Nickel1999, Colom2023,
     HuWang2023) inserted before \end{thebibliography};
 (3) ONE sentence updating open question 3's pointer.

Reads oneway_kernel_paper_v2b.tex, writes oneway_kernel_paper_v2c.tex;
the source is never modified. Aborts without writing if any anchor is not
found exactly once; on abort prints the real file lines near the targets.
"""
import sys, os, re

SRC = "oneway_kernel_paper_v2b.tex"
DST = "oneway_kernel_paper_v2c.tex"

EXTENSION = r"""
Two further structural facts about this boundary were established
numerically after the characterization above, and are recorded here with
the same status discipline (machine-verified simulation of the kernel;
no physical claim). First, the crossing of the boundary is
\emph{oriented}: writing the leading discontinuity of the closed form
across the cut $x \in (1,\infty)$ as
$\mathrm{disc}\,\Phi(x,2,a) = 2\pi i\, x^{-a} \ln x$, the complex offset
$a = 1 + \kappa/(2i\delta)$ produced by one-way coupling makes the
\emph{phase} of the jump rotate along the cut (by
$\arg x^{-(a-1)}$, about $9.2^\circ$ from $x=1$ to $x=5$ at
$\kappa/\delta = 0.2$), whereas the reciprocal (Bergman-type,
dilogarithm) control, whose offset is real, has a frozen jump phase at
every point of the cut. The ratio law
$\mathrm{disc}_{\text{one-way}}/\mathrm{disc}_{\text{reciprocal}}
= x^{-(a-1)}$ was verified digit-for-digit against the dilogarithm
control (itself machine-exact to $10^{-9}$); the monodromy stacking
across repeated crossings is arithmetic (equal sheet steps, ratios equal
to unity to $10^{-21}$). We are not aware of a published use of the
cut-discontinuity phase law as a reciprocity witness; the closest works
we found diagnose directionality through spectral winding numbers or
end-to-end Green's-function growth \cite{HuWang2023}, through the phase
of the drive \cite{McDonald2018}, or through a frequency-dependent
$2\pi$ phase gradient at a branch-cut crossing in non-Hermitian
metasurfaces \cite{Colom2023}; none states a position-dependent jump
phase along the cut, and we flag the usual caveat that niche
terminology may hide precedents. Second, when several kernels with
different ladder spacings are summed, their tears stack on the same ray
and the jumps add linearly, but the phase windings differ, and the
resulting interference relief along the cut is governed by a
\emph{detuning} law: at fixed spread of ladder spacings, increasing the
number of summed kernels averages the phases and flattens the relief,
whereas at fixed number, widening the spread of spacings builds it
(contrast growing by an order of magnitude and interior interference
extrema appearing), while the reciprocal control remains flat at
machine precision throughout. Together with the truncation behaviour
above, this separates two emergence mechanisms living on the same
object: the boundary itself emerges from the \emph{number} of rungs,
while structure \emph{along} its tear emerges from their
\emph{diversity}. The emergence-with-$N$ pattern of an analyticity
boundary has well-known precedents in statistical mechanics --- the
accumulation of partition-function zeros in the thermodynamic limit
\cite{LeeYang1952} and the natural boundary of the 2D Ising
susceptibility built from singularities that become dense as the order
grows \cite{Nickel1999} --- and we present the truncation ladder of
Section~\ref{sec:boundary} as an instance of that phenomenon in a
two-point transfer kernel with complex offset, not as a new class.
"""

BIB = r"""\bibitem{LeeYang1952} C.~N. Yang and T.~D. Lee, Statistical theory of equations of state and phase transitions. I. Theory of condensation, Phys. Rev. \textbf{87}, 404 (1952); T.~D. Lee and C.~N. Yang, II. Lattice gas and Ising model, Phys. Rev. \textbf{87}, 410 (1952).
\bibitem{Nickel1999} B.~Nickel, On the singularity structure of the 2D Ising model susceptibility, J. Phys. A: Math. Gen. \textbf{32}, 3889 (1999); addendum, J. Phys. A: Math. Gen. \textbf{33}, 1693 (2000).
\bibitem{Colom2023} R.~Colom et al., Crossing of the branch cut: the topological origin of a universal $2\pi$-phase retardation in non-Hermitian metasurfaces, Laser Photonics Rev. \textbf{17}, 2200976 (2023).
\bibitem{HuWang2023} Y.-M. Hu and Z.~Wang, Green's functions of multiband non-Hermitian systems, Phys. Rev. Research \textbf{5}, 043073 (2023).
"""

POINTER_OLD = "the rigorous limit"
POINTER_NEW = ("the oriented (chiral) crossing law and the detuning-governed "
               "interference relief along the cut are characterized there as "
               "well; the rigorous limit")

ANCHOR_EXT = None   # set below: end of the boundary subsection = before \section{Relation
ANCHOR_SECTION = r"\section{Relation to prior structures}"
ANCHOR_BIBEND = r"\end{thebibliography}"

def main():
    if not os.path.exists(SRC):
        sys.exit(f"ABORT: {SRC} not found. Nothing written.")
    if os.path.exists(DST):
        sys.exit(f"ABORT: {DST} already exists. Remove it first. Nothing written.")
    text = open(SRC, encoding="utf-8").read()

    ok = True
    for name, anchor in [("section point", ANCHOR_SECTION),
                         ("bibliography end", ANCHOR_BIBEND),
                         ("pointer phrase", POINTER_OLD)]:
        n = text.count(anchor)
        print(f"anchor ({name}): found {n} time(s)")
        if n != 1:
            ok = False
            print(f"  DIAGNOSTIC -- lines containing a fragment of the anchor:")
            frag = anchor[:20]
            for i, line in enumerate(text.splitlines(), 1):
                if frag in line:
                    print(f"    L{i}: {line[:100]}")
    for key in ["LeeYang1952", "Nickel1999", "Colom2023", "HuWang2023"]:
        n = text.count(key)
        if n != 0:
            ok = False
            print(f"new bib key '{key}': pre-existing occurrences = {n} (must be 0)")
    if not ok:
        sys.exit("ABORT: anchor/key verification failed. Nothing written.")

    before = text.count("\n")
    out = text.replace(ANCHOR_SECTION, EXTENSION + "\n" + ANCHOR_SECTION, 1)
    out = out.replace(ANCHOR_BIBEND, BIB + ANCHOR_BIBEND, 1)
    out = out.replace(POINTER_OLD, POINTER_NEW, 1)
    open(DST, "w", encoding="utf-8").write(out)
    after = out.count("\n")
    print("--- REPORT ---")
    print(f"lines: {before} -> {after} (+{after - before})")
    for key in ["LeeYang1952", "Nickel1999", "Colom2023", "HuWang2023", "McDonald2018"]:
        print(f"  '{key}' occurrences in output: {out.count(key)}")
    print(f"WROTE {DST}. Source {SRC} untouched.")

if __name__ == "__main__":
    main()
