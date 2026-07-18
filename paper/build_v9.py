#!/usr/bin/env python3
# build_v9.py -- 2026-07-17
# Builds oneway_kernel_paper_v9.tex from oneway_kernel_paper_v8.tex
# (chain: v3 sealed -> build_v5..v7 -> v7 (H1-H3 folded) -> build_v8.py -> v8
#  -> this). Fix basis: FIFTH external adversarial audit (GPT-5.6) of v8,
# each catch verified on the tex or machine-certified; registry #060
# (calendar-vs-weights law, 8/8 SymPy on Anthony's machine) is the graved
# base for the weight-sentence rewrites; decision D1 = the phase-referenced
# branch is specified as a requirement with an explicit not-simulated
# perimeter (no modulus-only simulation is inherited by it).
#
# Take-by-take map (audit -> edit tags):
#  K third life (classification + contrast functional) -> W1a-e
#  R_{G,C} defined + propagated (operator, protocol)   -> W2a-c
#  S_C transport sector-preserving (v8 debt)           -> W3
#  Calendar/weights on #060 (positions move, N>=3)     -> W4a-c
#  rho angle = component of size                        -> W5
#  Riemann-Lebesgue rate de-surclaimed                  -> W6
#  winding causality (ladder offset vs one-way) x3      -> W7a-c
#  'none states' deflated                               -> W8
#  phase-referenced perimeter (abstract/7.3/8/concl/5.3)-> W9a-e
#  Fig. 2 caption strengthened (matrix reciprocal)      -> W10
#  version metadata v9, drafts window v4--v8            -> W0a-d

import hashlib, sys

SRC = "oneway_kernel_paper_v8.tex"
DST = "oneway_kernel_paper_v9.tex"
SRC_SHA256 = "372271b4174c437fe86d2951cf28a0757a2f4e96ee63817fe2e5e67dc417255e"

with open(SRC, "rb") as f:
    raw = f.read()
h = hashlib.sha256(raw).hexdigest()
assert h == SRC_SHA256, f"[input] v8.tex sha256 mismatch: {h}"
t = raw.decode("utf-8")

edits = []

def rep(old, new, tag):
    global t
    n = t.count(old)
    assert n == 1, f"[{tag}] anchor count = {n} (need 1)"
    t = t.replace(old, new)
    edits.append(tag)

# ---------------------------------------------------------------- metadata
rep(r"\date{July 17, 2026 (v8)}", r"\date{July 17, 2026 (v9)}", "W0a-date")
rep("transfer kernel (v8)}, pdfauthor={Anthony Monnerot}}",
    "transfer kernel (v9)}, pdfauthor={Anthony Monnerot}}", "W0b-pdftitle")
rep(r"\paragraph{Version note (v8).}", r"\paragraph{Version note (v9).}",
    "W0c-note-title")
rep("Intermediate drafts v4--v7 existed only",
    "Intermediate drafts v4--v8 existed only", "W0d-note-window")

# ------------------------------------------ W1: kill K's third life for good
rep(r"$\partial_a \partial_b \log K$ across the two points, evaluated on all four",
    r"$\partial_a \partial_b \log G_{21}$ across the two points, evaluated on all four",
    "W1a-classification-logK")

rep("non-pairing: $K$ is not invariant under the mirror map, and no mirror partner",
    "non-pairing: $G_{21}$ is not invariant under the mirror map, and no mirror partner",
    "W1b-classification-K")

rep(r"""$K(f) = (\max_I f - \min_I f)/(\max_I f + \min_I f)$ satisfies""",
    r"""$\mathcal{C}(f) = (\max_I f - \min_I f)/(\max_I f + \min_I f)$ satisfies""",
    "W1c-contrast-def")

rep(r"""$K(|\hat{\mu}_N|) \to K(|\hat{\mu}|)$, the denominator being protected:""",
    r"""$\mathcal{C}(|\hat{\mu}_N|) \to \mathcal{C}(|\hat{\mu}|)$, the denominator being protected:""",
    "W1d-contrast-statement")

rep(r"""uniform convergence on the compact window; $K$ is continuous in the sup""",
    r"""uniform convergence on the compact window; $\mathcal{C}$ is continuous in the sup""",
    "W1e-contrast-proof")

# ------------------------- W2: R_{G,C} defined and propagated (general C)
rep(r"""and the invariant is then written
$R_{\mathbf{G},C}$),""",
    r"""and the invariant is then written
$R_{\mathbf{G},C} = \mathbf{G} - S_C(\mathbf{G})$),""",
    "W2a-RGC-defined")

rep(r"""$\mathbf{G} = L^{-1}$, i.e.\ to $R_{\mathbf{G}} = 0$; the identity""",
    r"""$\mathbf{G} = L^{-1}$, i.e.\ to $R_{\mathbf{G},C} = 0$ (reducing to
$R_{\mathbf{G}} = 0$ in the port basis $C = I$); the identity""",
    "W2b-operator-RGC")

rep("""(heterodyne or quadrature demodulation against a common reference, the
calibration $C$ fixed once)""",
    """(heterodyne or quadrature demodulation against a common reference, the
calibration fixed once in the port basis, $C = I$)""",
    "W2c-protocol-portbasis")

# --------------------- W3: S_C transport scoped to sector-preserving C
rep("""the same orientation, fixed once by the common parametrization of $x$ and
transported unchanged under $S_C$ (the exchange maps each sector cut onto
the other without reversing the ray); physically,""",
    """the same orientation, fixed once by the common parametrization of $x$ and
transported unchanged under $S_C$ for sector-preserving calibrations
(block-diagonal in the channel basis, the exchange then mapping each sector
cut onto the other without reversing the ray; a channel-mixing $C$ falls
outside the separable-class scope of this witness); physically,""",
    "W3-SC-sector-preserving")

# ------------- W4: calendar vs weights, rewritten on the graved #060 law
rep(r"""summed kernels. Positive real rescalings of the weights act as a volume
knob: interference minima keep their positions while only the contrast moves
(a negative real weight carries an angle $\pi$ and is not a pure volume
change). Relative complex phases""",
    r"""summed kernels. A \emph{common} positive rescaling of all the weights is a
pure volume knob: the normalized relief is exactly invariant. Relative
changes of the positive moduli, by contrast, generally move the
interference minima from $N \geq 3$ on --- three needles with weights
$(1, \alpha, 1)$ on windings $(0, 1, 2)$ have relief $|\alpha + 2\cos u|$,
whose deep minimum sits at $u = \arccos(-\alpha/2)$ and moves with
$\alpha$; at $N = 2$ the minima positions are weight-independent for
positive weights (and a negative real weight carries an angle $\pi$, not a
volume change at all). Relative complex phases""",
    "W4a-volume-knob-060")

rep(r"""translates the
interference minima by $\Delta\varphi/\Delta\nu$ in logarithmic scale
($u = \ln x$, Section~\ref{sec:calendar}),""",
    r"""translates the
interference minima by $-\Delta\varphi/\Delta\nu$ in logarithmic scale
($u = \ln x$; minima exactly at
$u_n = ((2n+1)\pi - \Delta\varphi)/\Delta\nu$, Section~\ref{sec:calendar}),""",
    "W4b-translation-sign")

rep(r"""class-level --- independent of the weight family among real positive
weights (an algebraic identity in the $\nu_k$; relative complex phases
translate and deform the calendar, Section~\ref{sec:relief}) and stable
under fully randomized choirs of ladders ---""",
    r"""class-level in its \emph{frequency content} --- the period law is an
algebraic identity in the $\nu_k$, independent of the weight family ---
while the depth, selection and position of its deep minima are set by the
weight moduli and angles from $N \geq 3$ on (Section~\ref{sec:relief}); it
is stable under fully randomized choirs of ladders ---""",
    "W4c-calendar-scope-060")

# ------------------------------ W5: the angle is a component of the size
rep("""unimodular complex $\\rho$ would instead shift the weight angle, not the
size) leaves phase and slope identical""",
    """unimodular complex $\\rho$ would instead shift the angle component of the
weight, not its modulus) leaves phase and slope identical""",
    "W5-rho-angle")

# --------------------------------- W6: Riemann-Lebesgue rate de-surclaimed
rep(r"""lemma gives $\hat{\mu}(u) \to 0$, at rate $O(1/(ua))$ for a smooth
density on $[a,b]$ with $a > 0$:""",
    r"""lemma gives $\hat{\mu}(u) \to 0$, with no universal rate in general;
under mild regularity (a density of bounded variation on $[a,b]$, $a > 0$)
the decay is $O(1/u)$, with constants set by the boundary values of the
density --- for the log-uniform family the boundary term scales as
$1/(ua)$:""",
    "W6-RL-rate")

# --------------- W7: winding causality -- ladder offset vs one-way deletion
rep(r"""$a = 1 + \kappa/(2i\delta)$ produced by one-way coupling makes the""",
    r"""$a = 1 + \kappa/(2i\delta)$ of the physical double-pole ladder --- carried
alone by the one-way kernel, whose partner sector is deleted --- makes the""",
    "W7a-chiral-431")

rep("""arises with no hierarchy anywhere in the construction --- in this model it
is produced by the one-way (Jordan) coupling, though complex winding is not""",
    """arises with no hierarchy anywhere in the construction --- it is set by the
complex offset of the damped double-pole ladder ($\\kappa/2\\delta$ per
rung), the one-way coupling deleting the partner sector, though complex
winding is not""",
    "W7b-calendar-593")

rep("""contains no hierarchy: in this model the imaginary part of the exponent is
produced by the one-way (Jordan) coupling --- a route realized here, not the
unique origin of complex winding.""",
    """contains no hierarchy: the imaginary part of the exponent is set by the
complex offset of the damped ladder, the one-way (Jordan) coupling deleting
the partner sector --- a route realized here, not the unique origin of
complex winding.""",
    "W7c-dsi-1020")

# --------------------------------------------- W8: 'none states' deflated
rep("""; none states a position-dependent jump
phase along the cut, and we flag""",
    """; a position-dependent jump
phase along the cut appears unreported in the literature we searched, and
we flag""",
    "W8-none-states")

# ---------------- W9: phase-referenced branch -- honest perimeter (D1 = i)
rep("""single-versus-twin-comb conditional reciprocity witness. Numerical simulations with""",
    """single-versus-twin-comb conditional reciprocity witness; a direct
measurement of the reciprocity invariant additionally requires reverse
injection with phase-referenced detection, specified but not simulated
here. Numerical simulations with""",
    "W9a-abstract")

rep(r"""modulus-only records are mirror-blind (Section~\ref{sec:limits}).""",
    r"""modulus-only records are mirror-blind (Section~\ref{sec:limits}). The
phase-referenced branch is specified here as a requirement: its hardware
realization (reference arm or local oscillator, I/Q or phase-stepped
detection, relative calibration of the two directions) and its noise
budget are beyond the simulated scope of this deposit and are flagged as
future work.""",
    "W9b-protocol-perimeter")

rep("""demands a phase-quiet loop even more than the comb itself does.""",
    """demands a phase-quiet loop even more than the comb itself does. The
analysis above covers the modulus observables; the phase-referenced
acquisition required for a direct measurement of $R_{\\mathbf{G}}$ carries
its own error terms (reference drift, I/Q imbalance, calibration error)
which are not simulated here.""",
    "W9c-noise-perimeter")

rep("""of its realistic imperfections and explicit criteria under which the proposal""",
    """of the realistic imperfections of its modulus observables (the
phase-referenced branch required for $R_{\\mathbf{G}}$ is specified but not
simulated) and explicit criteria under which the proposal""",
    "W9d-conclusion-perimeter")

rep(r"""reference beat recovers the complex transform from modulus-only records
(quadrature pair), lifting the mirror ambiguity of
Section~\ref{sec:limits}; the scheme and its exact demodulation law are
certified in the repository accompanying this deposit, for the weight class
certified there.""",
    r"""reference beat, read at two reference phases in quadrature, recovers the
complex transform --- a phase-referenced augmentation of the intensity
data, not a modulus-only inversion --- lifting the mirror ambiguity of
Section~\ref{sec:limits}; the scheme, with a known injected reference
needle $r\,e^{i(\nu_r u + \varphi_r)}$, and its exact demodulation law are
certified in the repository accompanying this deposit across eight weight
families, including size-disparate and size--speed-correlated choirs.""",
    "W9e-outlook-052-hypotheses")

# ------------------------------- W10: Fig. 2 caption, matrix-level explicit
rep("""Bottom: reciprocal control --- the twin comb appears at the mirrored""",
    """Bottom: matrix reciprocal control ($G_{12}$ restored) --- the twin comb
appears at the mirrored""",
    "W10-fig2-caption")

# ============================== SWEEPS =====================================
flat = " ".join(t.split())
fails = []

def forbid(s, tag):
    if s in flat:
        fails.append(f"NEGATIVE [{tag}]: forbidden phrase present: {s!r}")

def require(s, tag, n=1):
    c = flat.count(s)
    if c < n:
        fails.append(f"POSITIVE [{tag}]: {s!r} count {c} < {n}")

def exact(s, tag, n):
    c = flat.count(s)
    if c != n:
        fails.append(f"COUNT [{tag}]: {s!r} count {c} != {n}")

# --- negative: fifth-audit catches must be gone; earlier fixes must survive
forbid("(v8)", "meta")
forbid("v4--v7", "meta")
forbid(r"\log K$", "W1")
forbid("$K$ is not invariant", "W1")
forbid("$K(f)", "W1")
forbid(r"$K(|\hat", "W1")
forbid("$K$ is continuous", "W1")
forbid("produced by one-way coupling makes the", "W7")
forbid("none states", "W8")
forbid("O(1/(ua))", "W6")
forbid("not the size)", "W5")
forbid("minima keep their positions", "W4")
forbid("independent of the weight family among real positive", "W4")
forbid("from modulus-only records (quadrature pair)", "W9e")
forbid("for the weight class certified there", "W9e")
forbid("purely atomic", "v8-regression")
forbid("potentially new", "v8-regression")
forbid("figure, or protocol changed", "v8-regression")
forbid("what we believe has no direct precedent", "v8-regression")
forbid(r"K \equiv G_{21}", "v7-regression")
forbid("jointly characterize", "v7-regression")
exact("reciprocal control", "two-kept", 2)

# --- positive: new clauses + regression guards
exact("(v9)", "meta", 3)
require("v4--v8", "meta", 1)
require(r"\mathcal{C}(f)", "W1", 1)
require(r"\mathcal{C}(|\hat{\mu}_N|)", "W1", 1)
require(r"$\mathcal{C}$ is continuous", "W1", 1)
require(r"\partial_a \partial_b \log G_{21}$", "W1", 1)
require(r"R_{\mathbf{G},C} = \mathbf{G} - S_C(\mathbf{G})", "W2", 1)
require(r"R_{\mathbf{G},C} = 0$ (reducing to", "W2", 1)
require("port basis, $C = I$", "W2", 1)
require("sector-preserving calibrations", "W3", 1)
require(r"\arccos(-\alpha/2)", "W4", 1)
require(r"$|\alpha + 2\cos u|$", "W4", 1)
require(r"-\Delta\varphi/\Delta\nu", "W4", 1)
require(r"u_n = ((2n+1)\pi - \Delta\varphi)/\Delta\nu", "W4", 1)
require("frequency content", "W4", 1)
require("angle component of the", "W5", 1)
require("bounded variation", "W6", 1)
require("double-pole ladder", "W7", 2)
require("appears unreported in the literature we searched", "W8", 1)
require("specified but not simulated", "W9", 2)
require("not simulated here", "W9", 2)
require("reference arm or local oscillator", "W9", 1)
require(r"e^{i(\nu_r u + \varphi_r)}", "W9e", 1)
require("eight weight families", "W9e", 1)
require("matrix reciprocal control ($G_{12}$ restored)", "W10", 1)
require("real-offset (scalar) control", "v8-regression", 4)
require("conditional reciprocity witness", "v8-regression", 1)
require("of the surviving element", "v8-regression", 3)
require("apparently new", "v8-regression", 2)
require("finitely supported", "v8-regression", 1)
require(r"X = \zbone \wbtwo", "v8-regression", 1)
require(r"R_{\mathbf{G}} = \mathbf{G} - S(\mathbf{G})", "v8-regression", 2)

if fails:
    print(f"SWEEP FAILED ({len(fails)}):")
    for f_ in fails:
        print("  ", f_)
    sys.exit(1)

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print(f"OK: {len(edits)} edits applied -> {DST}")
for e in edits:
    print("  ", e)
print("SWEEPS: negative + positive + v7/v8-regression all PASS (normalized text)")
print("sha256:", hashlib.sha256(t.encode("utf-8")).hexdigest())
