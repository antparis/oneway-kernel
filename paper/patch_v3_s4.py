#!/usr/bin/env python3
"""S4 patcher: (1) replace the Section 5 stub (sec:spectroscopy) with the
full one-way-spectroscopy section (#051: instrument, proven limits,
outlook); (2) insert two positioning subsections into 'Relation to prior
structures' (NH point-gap topology [SHIELD-3]; discrete scale invariance);
(3) add Wanjura2020 and Zirnstein2021 bibitems (web-pinned 2026-07-10).
Run from paper/. In-place with dated backup."""
import shutil

F = "oneway_kernel_paper_v3.tex"
shutil.copyfile(F, F + ".bak-s4")
src = open(F, encoding="utf-8").read()

A_SPEC = r"\section{One-way spectroscopy}"
A_PRIOR = r"\section{Relation to prior structures}"
A_COUSINS = r"\subsection{Cousins of the forcing question}"
A_BIB = r"\end{thebibliography}"
for a in (A_SPEC, A_PRIOR, A_COUSINS, A_BIB):
    assert src.count(a) == 1, f"anchor not unique: {a!r} count={src.count(a)}"
i0, i1 = src.index(A_SPEC), src.index(A_PRIOR)
assert i0 < i1

SECTION5 = r"""\section{One-way spectroscopy}
\label{sec:spectroscopy}

The floor law of Section~\ref{sec:floor} maps the composition of a choir
to its relief. This section reads the map backwards: given only the
measured relief along the cut, identify the family of the winding
measure and recover its parameters. The result is an instrument that
works --- and that ships with its limits proven on the day of its
construction, which we regard as part of the result.

\subsection{The instrument}
\label{sec:instrument}

The inverter fits the closed-form dictionary of
Eqs.~\eqref{eq:closedfloors}--\eqref{eq:sincfloor} to a measured relief
by least squares over the winding interval $[a, b]$, once per candidate
family, and selects the family with the smallest residual. Blind tests
against hidden finite choirs ($N = 64$, clean data) identify the
log-uniform family correctly with $a$ recovered to $1.34\%$ and $b$ to
$0.11\%$, and the uniform family correctly with $b$ to $0.21\%$; the
inverse-square case, however, exposes a degeneracy of the short
observation window: a log-uniform fit driven to its $a \to 0$ edge
impersonates the $1/\nu^2$ family (residual $3.5\times10^{-9}$ against
$6.9\times10^{-8}$ for the true family), and wins the selection. We
record the failure verbatim; its diagnosis, and resolution, are the
subject of the next subsection.

\subsection{Proven limits}
\label{sec:limits}

Three limits of the spectroscopy are established alongside it. First,
the instrument is \emph{exactly mirror-blind}: the reflected measure
$\nu \mapsto a + b - \nu$ has transform
$\hat{\mu}_{\mathrm{mir}}(u) = e^{i(a+b)u}\,\overline{\hat{\mu}(u)}$,
of identical modulus, so modulus-only data cannot distinguish a choir
from its mirror (machine: maximal relief difference $5.7\times10^{-15}$).
This is a hard bound of any modulus-only inversion, recorded rather than
hidden. Second, \emph{the window is the aperture}: information about a
winding speed $\nu$ lives at $u \sim 1/\nu$. On the short window the
slow windings sweep only $\approx 0.02$ rad and write essentially
nothing --- which at once explains the family degeneracy above (the
candidate measures differ mainly at their slow edge) and makes the slow
parameter fragile under noise ($29\%$ error on $a$ at $1\%$ relative
noise, against $1.4\%$ on $b$). Extending the window toward
$u \sim 1/a$ (here $[0.05, 300]$, with $N = 1024$ so that the finite
choir remains a valid proxy, $u \ll N$) dissolves both failures at once:
the inverse-square family is then correctly identified with a
thirty-fold residual separation and $a$ recovered to $0.10\%$, and the
noise-induced error on $a$ collapses from $29.4\%$ to $0.02\%$. Third,
the instrument is \emph{mute on the reciprocal by design}: a flat relief
falls below the protocol contrast floor and the inversion is refused
rather than hallucinated --- the reciprocal kernel is unreadable, as
Corollary~1 of Section~\ref{sec:theorem} demands.

\subsection{Outlook for the measurement protocol}
\label{sec:specoutlook}

The spectroscopy upgrades the role of the boundary observables: a
measurement of the relief along the cut, of the kind the
recirculating-loop platform proposed below is designed to approach,
would allow one not only to certify one-wayness (the jump-phase witness
of Section~\ref{sec:chiral}) but to \emph{read} the composition of the
couplings that produce it --- which modes, at which winding speeds, with
which weights, within the proven limits above. We state this as an
outlook on the mathematics of the kernel, not as an experimental claim.

"""

SUBS_PRIOR = r"""\subsection{Non-Hermitian point-gap topology and directional amplification}
\label{sec:nhtopo}

The certification role proposed in Section~\ref{sec:chiral} for the
cut-discontinuity phase should be positioned against the standard
witnesses of directionality in non-Hermitian lattice physics. There,
non-reciprocity is diagnosed through the point-gap winding number of the
determinant of the dynamic matrix as momentum traverses the Brillouin
zone, in one-to-one correspondence with directional amplification and
exponential end-to-end gain \cite{Wanjura2020}, and through the spatial
growth of the bulk Green function, which the one-dimensional
non-Hermitian winding number implies \cite{Zirnstein2021}; see
also \cite{HuWang2023} for Green's-function winding as a unifying
invariant. These witnesses and ours share a family trait --- an argument
winding as the signature of one-wayness --- but the objects differ:
theirs wind in momentum space or grow in real space on lattice models,
whereas ours is the position-dependent phase of the branch-cut
discontinuity of a closed-form two-point kernel in the product of
conjugated coordinates. We are not aware of an overlap of objects, and
flag once more that niche terminology may hide precedents.

\subsection{Discrete scale invariance and log-periodicity}
\label{sec:dsi}

The log-scale calendar of Section~\ref{sec:calendar} places this work in
contact with the literature on discrete scale invariance, where
log-periodic corrections arise from complex critical exponents
\cite{Derrida1984,Sornette1998} in systems with built-in hierarchies ---
hierarchical lattices, renormalization flows, and the broad range of
applications surveyed in \cite{Sornette1998}. The present construction
contains no hierarchy: the imaginary part of the exponent is produced by
the one-way (Jordan) coupling alone. We therefore read the kernel as a
hierarchy-free route to a classical motif, rather than as an instance of
the classical mechanism --- a positioning claim we keep hedged, as
elsewhere in this paper.

"""

BIBADD = r"""\bibitem{Wanjura2020} C.~C.~Wanjura, M.~Brunelli, and A.~Nunnenkamp,
Topological framework for directional amplification in driven-dissipative
cavity arrays, Nat. Commun. \textbf{11}, 3149 (2020).

\bibitem{Zirnstein2021} H.-G.~Zirnstein, G.~Refael, and B.~Rosenow,
Bulk-boundary correspondence for non-Hermitian Hamiltonians via Green
functions, Phys. Rev. Lett. \textbf{126}, 216407 (2021).

"""

out = src[:i0] + SECTION5 + src[i1:]
out = out.replace(A_COUSINS, SUBS_PRIOR + A_COUSINS, 1)
out = out.replace(A_BIB, BIBADD + A_BIB, 1)
open(F, "w", encoding="utf-8").write(out)
print(f"OK: {F} rewritten ({len(out.splitlines())} lines, from {len(src.splitlines())}); backup {F}.bak-s4")
for k in ["sec:instrument", "sec:limits", "sec:specoutlook", "sec:nhtopo",
          "sec:dsi", "Wanjura2020", "Zirnstein2021", "TODO S4"]:
    print(f"  {k}: {out.count(k)}")
