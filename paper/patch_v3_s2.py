#!/usr/bin/env python3
"""S2 patcher: create oneway_kernel_paper_v3.tex from v2c.
- Promotes the boundary subsection (v2c lines ~256-337) to a full Section 3
  with four subsections (old text absorbed verbatim, registry #042/#043/#045/
  #047 additions, new 3.4 log-periodic calendar #044 with DSI shielding).
- Inserts stub Sections 4 and 5 (labels live, bodies TODO for S3/S4).
- Appends Derrida1984 and Sornette1998 bibitems.
v2c file is never modified. Run from the paper/ directory."""
import sys

SRC, DST = "oneway_kernel_paper_v2c.tex", "oneway_kernel_paper_v3.tex"
src = open(SRC, encoding="utf-8").read()

A_START = r"\subsection{Boundary structure of the kernel}"
A_END = "not as a new class."
A_PRIOR = r"\section{Relation to prior structures}"
A_BIB = r"\end{thebibliography}"
for a, n in [(A_START, 1), (A_END, 1), (A_PRIOR, 1), (A_BIB, 1)]:
    assert src.count(a) == n, f"anchor not unique: {a!r} count={src.count(a)}"

i0 = src.index(A_START)
i1 = src.index(A_END) + len(A_END)
assert i1 > i0

SECTION3 = r"""\section{Boundary structure of the kernel}
\label{sec:boundary}

The closed form of Section~\ref{sec:closedform} converges on the open unit
polydisk $|x| < 1$, $x = \zbone\wbtwo$, and the proposed protocol reads its
boundary values. This section records the machine-verified structure of that
boundary: its intrinsic and emergent character
(Section~\ref{sec:wall}), the chiral law of its crossing
(Section~\ref{sec:chiral}), the interference relief along its tear
(Section~\ref{sec:relief}), and the exact log-scale calendar of the deep
interference minima (Section~\ref{sec:calendar}). All results are
structural characterizations of the kernel, verified in the repository
accompanying this deposit; no physical claim is made.

\subsection{An intrinsic, emergent boundary}
\label{sec:wall}

Three structural facts about the boundary are worth
recording. First, the boundary is intrinsic and dimensionless: it sits at the
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

These characterizations were subsequently audited at the class level.
The location of the boundary is dimensionless across coupling strengths
(departure radius $0.990636$ versus $0.987198$ at $N = 30$ for
$\kappa = 0.2$ and $\kappa = 1.0$), and, across ladder families, the
\emph{existence} of the wall is generic while its \emph{location} is set
by the asymptotics of the mode weights: polynomially decaying weights
place it at $|x| = 1$ for every tested power ($s = 1, 2, 3$, polylogarithm
controls), while geometrically decaying weights of ratio $r$ move it to
$|x| = 1/r$ (machine-checked at $r = 0.5$). The wall is a property of the
class; the choices pick the specimen.

\subsection{The chiral phase law of the cut}
\label{sec:chiral}

The crossing of the boundary is
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
terminology may hide precedents.

The law was subsequently stress-tested across coupling strengths and
ladder families. The ratio identity holds to machine precision
($1.1\times10^{-16}$--$2.2\times10^{-16}$) at $\kappa = 0.05$, $0.2$ and
$1.0$, with the phase drift linear in the coupling,
$\arg x^{-(a-1)} = (\kappa/2\delta)\ln x$
($+0.99^\circ$, $+3.97^\circ$, $+19.86^\circ$ at $x = 2$ respectively);
and the drift law is independent of the weight family (polynomially
weighted ladders of every tested order obey the same law, with
polylogarithm controls agreeing to better than $10^{-9}$). The twist of
the jump belongs to the one-way class; the envelope belongs to the
specimen.

\subsection{Interference relief along the cut}
\label{sec:relief}

When several kernels with
different ladder spacings are summed, their tears stack on the same ray
and the jumps add linearly, but the phase windings differ, and the
resulting interference relief along the cut is governed by a
\emph{detuning} law: at fixed spread of ladder spacings, increasing the
number of summed kernels averages the phases and flattens the relief,
whereas at fixed number, widening the spread of spacings builds it
(contrast growing by an order of magnitude and interior interference
extrema appearing), while the reciprocal control remains flat at
machine precision throughout. Together with the truncation behaviour of
Section~\ref{sec:wall}, this separates two emergence mechanisms living
on the same object: the boundary itself emerges from the \emph{number}
of rungs, while structure \emph{along} its tear emerges from their
\emph{diversity}. The emergence-with-$N$ pattern of an analyticity
boundary has well-known precedents in statistical mechanics --- the
accumulation of partition-function zeros in the thermodynamic limit
\cite{LeeYang1952} and the natural boundary of the 2D Ising
susceptibility built from singularities that become dense as the order
grows \cite{Nickel1999} --- and we present the truncation ladder of
Section~\ref{sec:wall} as an instance of that phenomenon in a
two-point transfer kernel with complex offset, not as a new class.

The relief was further dissected with respect to the weights of the
summed kernels. Purely real weight changes act as a volume knob:
interference minima keep their positions while only the contrast moves.
A common complex phase reweights which minima dominate rather than
translating them (the detailed window-dependence of this effect was
diagnosed and is recorded in the repository). Size disparity alone
writes nothing: disparate weights on a single common winding speed give
contrast at machine zero ($9.6\times10^{-16}$), algebraically forced ---
the sum is a single fixed-length needle --- so winding-speed disparity
is the only source of relief. When sizes correlate with speeds the
response is asymmetric: weighting the slow windings collapses the
residual relief by an order of magnitude (a static-ballast effect:
quasi-static needles drown the relative ripples), while weighting the
fast ones raises it. Finally, as the number of summed kernels grows at
fixed spread, the relief does not vanish: it saturates toward a
distribution-dependent floor (near $0.048$ for log-uniformly spaced
ladders). The mechanism and the exact value of this floor admit a
closed law and an elementary theorem, developed in
Section~\ref{sec:floor}.

\subsection{The log-scale calendar of the deep rendezvous}
\label{sec:calendar}

The interference minima along the cut obey an exact and elementary law.
With the trivial $1/x$ envelope removed, the normalized relief of a sum
of $N$ kernels equals, for all $x > 1$,
\begin{equation}
P(u) \;=\; \Bigl|\,\sum_{k=1}^{N} w_k\, e^{\,i\nu_k u}\Bigr|,
\qquad u = \ln x,\qquad \nu_k = \frac{\kappa}{2\delta_k},
\label{eq:phasors}
\end{equation}
an algebraic identity rather than an asymptotic statement: the relief is
a finite sum of phasors rotating in \emph{logarithmic} scale,
almost-periodic in $u$ by construction. The deep minima are therefore
\emph{log-periodic} rendezvous of the phasors --- a form which is the
classical signature of complex exponents in the literature on discrete
scale invariance \cite{Derrida1984,Sornette1998}. Machine panels: for
$N = 2$ the relief is exactly periodic in $u$ with period
$T = 2\pi/|\nu_1 - \nu_2| = 94.247780$, matched to grid resolution; for
the three-ladder configuration used above, four deep minima occur at
$u = 10.00$, $29.98$, $49.93$, $69.81$ (spacings $\approx 19.9$, near
the extreme-winding beat), and the period law $T = 2\pi/|\Delta\nu|$
holds across four ladder spacings to $1.3\times10^{-3}$. This law also
resolves an earlier provisional reading: interference structures
reported at small $x$ in intermediate work were partial descents toward
the \emph{first} rendezvous (located near $x \approx 2.2\times10^{4}$ in
that configuration), outside every previously examined window; we record
the correction rather than the provisional reading. The calendar is
class-level --- independent of the weight family (an algebraic identity
in the $\nu_k$) and stable under fully randomized choirs of ladders ---
and it is one-way only: the reciprocal control (all $\nu_k = 0$) is flat
to machine zero, with no minima at all.

At the level of form, log-periodic oscillations are the hallmark of
discrete scale invariance, where complex exponents arise from
hierarchical structures or renormalization flows
\cite{Sornette1998,Derrida1984}. Here the imaginary part of the exponent
is produced by one-way (Jordan) coupling alone, with no hierarchy
anywhere in the construction; to our knowledge this route to the motif
is new, and we flag the usual caveat that niche terminology may hide
precedents."""

STUBS = r"""

\section{The Fourier floor theorem}
\label{sec:floor}

% TODO S3: the floor law (#048), the theorem and its machine-faced
% clauses (#049), the fate of the tides, the closed-form floors (#050).
[Section to be completed at the next revision stage: the residual-floor
law and its elementary theorem.]

\section{One-way spectroscopy}
\label{sec:spectroscopy}

% TODO S4: the inverse problem (#051): reading the winding measure from
% the relief; proven limits (mirror blindness, window aperture,
% reciprocal refusal); outlook tie to the loop protocol.
[Section to be completed at the next revision stage: the inverse reading
of the winding measure from the measured relief.]

"""

BIBADD = r"""\bibitem{Derrida1984} B.~Derrida, C.~Itzykson, and J.~M.~Luck,
Oscillatory critical amplitudes in hierarchical models,
Commun. Math. Phys. \textbf{94}, 115--132 (1984).

\bibitem{Sornette1998} D.~Sornette, Discrete-scale invariance and
complex dimensions, Phys. Rep. \textbf{297}, 239--270 (1998).

"""

out = src[:i0] + SECTION3 + src[i1:]
out = out.replace(A_PRIOR, STUBS + A_PRIOR, 1)
out = out.replace(A_BIB, BIBADD + A_BIB, 1)
open(DST, "w", encoding="utf-8").write(out)
print(f"OK: {DST} written ({len(out.splitlines())} lines, from {len(src.splitlines())})")
for k in ["sec:wall", "sec:chiral", "sec:relief", "sec:calendar",
          "sec:floor", "sec:spectroscopy", "Derrida1984", "Sornette1998"]:
    print(f"  {k}: {out.count(k)}")
