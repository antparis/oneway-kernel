#!/usr/bin/env python3
"""S3 patcher: replace the Section 4 stub (sec:floor) in
oneway_kernel_paper_v3.tex with the full Fourier-floor-theorem section
(4.1 law #048, 4.2 elementary theorem #049 with proof sketch, 4.3 fate of
the tides, 4.4 closed-form floors #050), and add the Bohr bibitem.
Run from the paper/ directory. The file is patched in place; a dated
backup is written first."""
import shutil, sys

F = "oneway_kernel_paper_v3.tex"
shutil.copyfile(F, F + ".bak-s3")
src = open(F, encoding="utf-8").read()

A_START = r"\section{The Fourier floor theorem}"
A_END = r"\section{One-way spectroscopy}"
A_BIB = r"\end{thebibliography}"
for a in (A_START, A_END, A_BIB):
    assert src.count(a) == 1, f"anchor not unique: {a!r} count={src.count(a)}"
i0, i1 = src.index(A_START), src.index(A_END)
assert i0 < i1

SECTION4 = r"""\section{The Fourier floor theorem}
\label{sec:floor}

Section~\ref{sec:relief} ended on an empirical fact: as the number of
summed kernels grows at fixed spread, the interference relief along the
cut saturates toward a distribution-dependent floor. This section derives
the exact law of that floor, proves it as an elementary theorem (the full
proof is deposited in the repository accompanying this record), settles
the fate of the log-scale calendar of Section~\ref{sec:calendar} in the
continuum limit, and computes the floors of the canonical ladder families
in closed form. Throughout, results labelled machine-verified were run
against the harnesses in the repository; the theorem's ingredients are
classical, and are labelled as such.

\subsection{The floor law}
\label{sec:floorlaw}

Encode a choir of $N$ summed kernels by its \emph{weighted winding
measure}, the probability measure
$\mu_N = \bigl(\sum_k w_k\bigr)^{-1} \sum_k w_k\, \delta_{\nu_k}$ on the
winding speeds $\nu_k = \kappa/(2\delta_k)$ of
Eq.~\eqref{eq:phasors}. The normalized relief of
Section~\ref{sec:calendar} is then exactly the modulus of its Fourier
transform, $P_N(u)/\sum_k w_k = |\hat{\mu}_N(u)|$ with
$\hat{\mu}_N(u) = \int e^{i\nu u}\, d\mu_N(\nu)$, and the residual floor
obeys:
\emph{as $N \to \infty$ at fixed distribution shape, on a fixed window in
$u$, the relief converges to $|\hat{\mu}(u)|$ and the floor equals the
window-contrast of the Fourier transform of the limiting weighted winding
measure.} On the machine, ladder families already near their limit sit on
the law (measured-to-computed contrast ratios $1.00$--$1.08$ across the
log-uniform, weighted and warped families tested), while families far
from their limit approach it from above --- which retroactively
identifies the apparent ``decay exponents'' of the saturation curves as
transients of this convergence, with no universal meaning. Two natural
first-order candidate laws were refuted en route and are recorded for
completeness: an incoherent (root-sum-square) ballast law fails with
structured deviations up to a factor of ten --- the floor is a
\emph{coherent} phenomenon --- and a binary active/ballast criterion is
degenerate on the roughness window, where no phasor completes a full
turn (maximal sweep $\approx 1.75$ rad): the roughness floor lives
entirely in the partial-rotation regime, while full turns belong to the
calendar of Section~\ref{sec:calendar}.

\subsection{An elementary theorem}
\label{sec:theorem}

\medskip\noindent\textbf{Theorem (Fourier floor law).}
\emph{Fix a window $I = [u_{\min}, u_{\max}] \subset (0,\infty)$ and let
$(\mu_N)$ be probability measures on $[a,b] \subset [0,\infty)$
converging weakly to $\mu$. Then $\hat{\mu}_N \to \hat{\mu}$ uniformly on
$I$, and the window-contrast
$K(f) = (\max_I f - \min_I f)/(\max_I f + \min_I f)$ satisfies
$K(|\hat{\mu}_N|) \to K(|\hat{\mu}|)$, the denominator being protected:
$\max_I |\hat{\mu}| > 0$ always.}

\medskip\noindent
\emph{Proof sketch.} Pointwise convergence follows from weak convergence
of measures against the bounded continuous family
$\nu \mapsto e^{i\nu u}$; the uniform Lipschitz bound
$|\hat{\mu}_N(u) - \hat{\mu}_N(u')| \le b\,|u - u'|$ upgrades it to
uniform convergence on the compact window; $K$ is continuous in the sup
norm wherever its denominator is positive; and the denominator is
protected because $\hat{\mu}$ extends to an entire function of $u$ with
$\hat{\mu}(0) = 1$, so it cannot vanish on any interval. The full proof,
together with a discrepancy lemma, is deposited in the repository. All
ingredients are classical (equicontinuity, Paley--Wiener-type
analyticity, discrepancy bounds); the contribution is the assembly
fitted to the one-way tear. \hfill$\square$

\medskip
The discrepancy lemma bounds the approach at rate $O(1/N)$ for quantile
samplings of the limiting measure --- a bound the machine shows is
\emph{not tight for all samplings}: midpoint quantile choirs converge at
second order (measured log--log slope $-2.00$), endpoint choirs at first
order (slope $-1.02$). The approach speed belongs to \emph{how the choir
samples its measure}, not to the measure alone; the naive first-order
prediction was corrected by the machine before deposit, and the
correction is part of the statement. Three corollaries close earlier
threads. First, the reciprocal control is now a theorem line: all
$\nu_k = 0$ means $\mu = \delta_0$, hence $\hat{\mu} \equiv 1$ and zero
relief on every window --- the machine-flat reciprocal controls of
Sections~\ref{sec:relief} and~\ref{sec:calendar} are instances of this
one line. Second, uniform convergence makes the law
estimator-agnostic: any functional continuous in the sup norm (contrast,
r.m.s.\ ripple over mean, \dots) converges alike, and the machine
confirms both at ratio $1.000$. Third, complex weights are covered
verbatim with $\mu_N$ a finite complex measure --- the phase reweighting
of Section~\ref{sec:relief} is a reweighting of $\mu$.

\subsection{The fate of the tides}
\label{sec:tides}

The theorem's sharpest consequence concerns the long-range destiny of
the calendar of Section~\ref{sec:calendar}, and splits on the nature of
the measure. If $\mu$ is \emph{purely atomic} --- any finite choir ---
then $\hat{\mu}$ is a finite trigonometric sum, hence a Bohr
almost-periodic function \cite{Bohr1947}: every value configuration
recurs within any tolerance infinitely often, and the deep rendezvous
recur forever (machine: for the three-ladder configuration, the maximal
normalized relief equals $1.000$ on the far windows $u \in [1000,1200]$
and $u \in [3000,3200]$ alike). If instead $\mu$ is \emph{absolutely
continuous} --- a true continuum of windings --- the Riemann--Lebesgue
lemma gives $\hat{\mu}(u) \to 0$, at rate $O(1/(ua))$ for a smooth
density on $[a,b]$ with $a > 0$: the whole profile dies on far windows
(machine, with a quantile proxy valid while $u \ll N$: maximal relief
$0.0605 \to 0.0216$ between the two windows above, consistent with
$1/u$). The log-scale calendar is therefore a \emph{discreteness}
phenomenon: a finite ladder keeps it forever, a continuum of windings
forgets it and the tear heals at large scale. No novelty is claimed for
the ingredients, which are textbook; the dichotomy is recorded because
it closes Sections~\ref{sec:calendar} and~\ref{sec:floorlaw} into one
object.

\subsection{Closed-form floors}
\label{sec:closedfloors}

Taking the theorem at its word, the floors of the canonical ladder
families are computed rather than simulated. On the winding interval
$[a,b] = [1/300, 1/3]$ used throughout (with
$\Delta\mathrm{Ci} + i\,\Delta\mathrm{Si}$ denoting
$\mathrm{Ci}(bu)-\mathrm{Ci}(au) + i\,[\mathrm{Si}(bu)-\mathrm{Si}(au)]$):
\begin{equation}
\hat{\mu}_{\log}(u) = \frac{\Delta\mathrm{Ci} + i\,\Delta\mathrm{Si}}
{\ln(b/a)},
\qquad
\hat{\mu}_{1/\nu^2}(u) = \frac{\dfrac{e^{iau}}{a} - \dfrac{e^{ibu}}{b}
+ iu\,(\Delta\mathrm{Ci} + i\,\Delta\mathrm{Si})}{1/a - 1/b},
\label{eq:closedfloors}
\end{equation}
\begin{equation}
\hat{\mu}_{\mathrm{unif}}(u) = \frac{e^{ibu} - e^{iau}}{iu\,(b-a)},
\label{eq:sincfloor}
\end{equation}
for the log-uniform, inverse-square (equivalently: linear-in-$\delta$)
and uniform measures respectively --- the last being the cardinal sine.
Their window-contrasts, $0.04764907$, $0.00565563$ and $0.06533857$,
match $N = 32768$ quantile choirs at relative accuracy
$3.6\times10^{-9}$, $6.0\times10^{-7}$ and $9.0\times10^{-10}$: the
floors of the whole relief phenomenology are values of three formulas
written with two-century-old functions. The derivation also exposed two
identities hidden from the simulations: weighting a log-uniform ladder
by $1/\nu$ (slow windings heavy, the static-ballast direction of
Section~\ref{sec:relief}) produces the effective measure
$d\nu/\nu^2$ --- \emph{exactly} the linear-in-$\delta$ measure, so two
independently measured floors ($0.00568$ and $0.00567$) are one
transform (closed value $0.00566$); and weighting by $\nu$ produces the
uniform measure, so that floor is a contrast of the cardinal sine
($0.06536$ measured, $0.06534$ closed). The compression chain of this
section is then complete: the relief phenomenology of
Section~\ref{sec:relief} reduces to three canonical measures, one law,
one elementary theorem and three formulas --- and the law can be read
backwards, which is the subject of Section~\ref{sec:spectroscopy}.

"""

BIBADD = r"""\bibitem{Bohr1947} H.~Bohr, \emph{Almost Periodic Functions}
(Chelsea, New York, 1947).

"""

out = src[:i0] + SECTION4 + src[i1:]
out = out.replace(A_BIB, BIBADD + A_BIB, 1)
open(F, "w", encoding="utf-8").write(out)
print(f"OK: {F} rewritten ({len(out.splitlines())} lines, from {len(src.splitlines())}); backup {F}.bak-s3")
for k in ["sec:floorlaw", "sec:theorem", "sec:tides", "sec:closedfloors",
          "Bohr1947", "eq:closedfloors", "eq:sincfloor", "TODO S3"]:
    print(f"  {k}: {out.count(k)}")
