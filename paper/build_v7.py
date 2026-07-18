#!/usr/bin/env python3
# build_v7.py -- 2026-07-16
# Builds oneway_kernel_paper_v7.tex from oneway_kernel_paper_v6.tex
# (chain: v3 sealed -> build_v5.py -> v5 -> build_v6.py -> v6 -> this).
# Fix basis: external adversarial audit of v6 (GPT-5.6), each catch verified
# on the tex. Core fixes: K/G notation collision, patch-broken fragment,
# stale version-note title, complex-weight normalization, conclusion
# de-surclaim, winding-causality exclusivity, protocol conditionality.

SRC = "oneway_kernel_paper_v6.tex"
DST = "oneway_kernel_paper_v7.tex"

with open(SRC, encoding="utf-8") as f:
    t = f.read()

edits = []

def rep(old, new, tag):
    global t
    n = t.count(old)
    assert n == 1, f"[{tag}] anchor count = {n} (need 1)"
    t = t.replace(old, new)
    edits.append(tag)

# G0 -- date ------------------------------------------------------------------
rep(r"\date{July 16, 2026 (v6)}", r"\date{July 16, 2026 (v7)}", "G0-date")

# G1a -- kill the K-collision at its source: no global "K == G21" --------------
rep(
"""Throughout, $K$ denotes this surviving transfer element, $K \\equiv G_{21}$;
the complete two-channel kernel is the matrix with $G_{12} = 0$, and for
matrix-valued kernels the exchange $S$ also transposes the channel indices,
$(S G)_{ij}(\\mathbf{r}_1, \\mathbf{r}_2) = G_{ji}(\\mathbf{r}_2, \\mathbf{r}_1)$
(or its $C$-covariant version): with this definition the scalar element, a
function of the commuting product $\\zb\\wb$, is exchange-symmetric on its own,
while the matrix kernel has $R \\neq 0$ --- reciprocity statements always
refer to the matrix (Section~\\ref{sec:mirror}). The""",
"""We write $G_{21}$ for this surviving transfer element; the complete
two-channel kernel is the matrix $\\mathbf{G} = (G_{ij})$ with $G_{12} = 0$,
and for matrix-valued kernels the exchange $S$ also transposes the channel
indices,
$(S \\mathbf{G})_{ij}(\\mathbf{r}_1, \\mathbf{r}_2) = G_{ji}(\\mathbf{r}_2,
\\mathbf{r}_1)$, or explicitly in its $C$-covariant form
$(S_C \\mathbf{G})(\\mathbf{r}_1, \\mathbf{r}_2) = C^{-1}\\,
\\mathbf{G}(\\mathbf{r}_2, \\mathbf{r}_1)^{T}\\, C$: with this definition the
scalar element, a function of the commuting product $\\zb\\wb$, is
exchange-symmetric on its own, while the matrix kernel has
$R_{\\mathbf{G}} = \\mathbf{G} - S(\\mathbf{G}) \\neq 0$. In the general
statements of this paper $K$ denotes a generic two-point kernel --- scalar or
matrix, with $S$ acting accordingly --- and we write $G_{21}$ or $\\mathbf{G}$
whenever the distinction matters; reciprocity statements always refer to the
matrix (Section~\\ref{sec:mirror}). The""",
"G1a-K-collision")

# G1b -- operator paragraph: the matrix is G, not K -----------------------------
rep(
"""$L = L^{\\sharp}$ for the generator is equivalent to $K = K^{\\sharp}$ for the
kernel $K = L^{-1}$, i.e.\\ to $R = 0$; the identity""",
"""$L = L^{\\sharp}$ for the generator is equivalent to
$\\mathbf{G} = \\mathbf{G}^{\\sharp}$ for the matrix kernel
$\\mathbf{G} = L^{-1}$, i.e.\\ to $R_{\\mathbf{G}} = 0$; the identity""",
"G1b-operator-G")

# G2 -- repair the patch-broken fragment ----------------------------------------
rep(
"""couplings that produce it --- which modes, at which winding speeds, with
what weights. The spectroscopy reads the weighted winding measure of the
surviving element $G_{21}$; it does not, by itself, measure
$G_{21} - G_{12}$ ---
which weights, within the proven limits above. We state this as an""",
"""couplings that produce it --- which modes, at which winding speeds, with
what weights, within the proven limits above. The spectroscopy reads the
weighted winding measure of the surviving element $G_{21}$; it does not, by
itself, measure $G_{21} - G_{12}$. We state this as an""",
"G2-fragment")

# G3 -- version note: bump title, cover v4-v6 ------------------------------------
rep(
"""\\paragraph{Version note (v5).} This version repairs the reciprocity statement""",
"""\\paragraph{Version note (v7).} This version repairs the reciprocity statement""",
"G3a-note-title")
rep(
"""is certified by an expanded repair harness built in the same exact symbolic
discipline as the original claims. An
intermediate v4 existed only as an internal draft and was never deposited.""",
"""is certified by an expanded repair harness built in the same exact symbolic
discipline as the original claims. Intermediate drafts v4--v6 existed only
internally and were never deposited.""",
"G3b-note-body")

# G4 -- weights: positive rescalings; relative (not common) phases ---------------
rep(
"""summed kernels. Purely real weight changes act as a volume knob:
interference minima keep their positions while only the contrast moves.
A common complex phase reweights which minima dominate rather than
translating them (the detailed window-dependence of this effect was
diagnosed and is recorded in the repository).""",
"""summed kernels. Positive real rescalings of the weights act as a volume
knob: interference minima keep their positions while only the contrast moves
(a negative real weight carries an angle $\\pi$ and is not a pure volume
change). Relative complex phases between the weights reweight which minima
dominate rather than translating them --- a phase common to all weights
leaves the modulus relief invariant (the detailed window-dependence of the
relative-phase effect was diagnosed and is recorded in the repository).""",
"G4-weights-phases")

# G5a -- floor: probability measure under declared nonnegativity ------------------
rep(
"""Encode a choir of $N$ summed kernels by its \\emph{weighted winding
measure}, the probability measure
$\\mu_N = \\bigl(\\sum_k w_k\\bigr)^{-1} \\sum_k w_k\\, \\delta_{\\nu_k}$ on the""",
"""Encode a choir of $N$ summed kernels by its \\emph{weighted winding
measure}
$\\mu_N = \\bigl(\\sum_k w_k\\bigr)^{-1} \\sum_k w_k\\, \\delta_{\\nu_k}$ --- a
probability measure when the weights are nonnegative, $w_k \\geq 0$, which we
assume for the main statement --- on the""",
"G5a-floor-prob")

# G5b -- floor: complex normalization made explicit --------------------------------
rep(
"""by the same argument provided $\\sum_k w_k$ is bounded away from zero and
every bound is read in total variation ($\\|\\mu_N\\|_{\\mathrm{TV}}$ uniformly
bounded), with $\\mu_N$ then a finite complex measure rather than a
probability measure --- the phase reweighting""",
"""by the same argument provided $\\sum_k w_k$ is bounded away from zero and
every bound is read in total variation ($\\|\\mu_N\\|_{\\mathrm{TV}}$ uniformly
bounded), with $\\mu_N$ then a finite complex measure rather than a
probability measure and the normalized relief read as
$P_N(u)/\\bigl|\\sum_k w_k\\bigr| = |\\hat{\\mu}_N(u)|$ --- the phase reweighting""",
"G5b-floor-complex-norm")

# G6 -- conclusion: exhibited, not characterized ------------------------------------
rep(
"""violations that jointly characterize one-wayness at formula level.""",
"""violations that are both exhibited by the one-way construction at formula
level (they follow from $G_{12} = 0$ with nonvanishing transfer; they do not
by themselves characterize strict unidirectionality).""",
"G6-conclusion")

# G7a -- winding causality: not "alone", apparently new ------------------------------
rep(
"""\\cite{Sornette1998,Derrida1984}. Here the imaginary part of the exponent
is produced by one-way (Jordan) coupling alone, with no hierarchy
anywhere in the construction; to our knowledge this route to the motif
is new, and we flag the usual caveat that niche terminology may hide
precedents.""",
"""\\cite{Sornette1998,Derrida1984}. Here the imaginary part of the exponent
arises with no hierarchy anywhere in the construction --- in this model it
is produced by the one-way (Jordan) coupling, though complex winding is not
exclusive to one-way kernels (a paired reciprocal kernel with complex offset
carries it too, Section~\\ref{sec:chiral}); to our knowledge this
hierarchy-free route to the motif is apparently new, and we flag the usual
caveat that niche terminology may hide precedents.""",
"G7a-winding-559")

# G7b -- same fix in the prior-art restatement ----------------------------------------
rep(
"""contains no hierarchy: the imaginary part of the exponent is produced by
the one-way (Jordan) coupling alone. We therefore read the kernel as a""",
"""contains no hierarchy: in this model the imaginary part of the exponent is
produced by the one-way (Jordan) coupling --- a route realized here, not the
unique origin of complex winding. We therefore read the kernel as a""",
"G7b-winding-970")

# G8a -- protocol (iii): conditionality + reverse acquisition -------------------------
rep(
"""(iii) Reciprocity test: the one-way configuration predicts a single revival
comb; any reciprocal back-coupling produces a twin comb at the mirrored phase.""",
"""(iii) Conditional reciprocity witness: within the loop model the one-way
configuration predicts a single revival comb, and any reciprocal
back-coupling produces a twin comb at the mirrored phase; a direct
measurement of $R_{\\mathbf{G}}$ additionally requires the reverse-injection
acquisition ($G_{12}$: pulse the counter-clockwise port) alongside the
forward one.""",
"G8a-protocol")

# G8b -- noise section: same renaming --------------------------------------------------
rep(
"""whose regressor is separated in the fit. Finally, two facts matter for the
reciprocity test: the isolation floor of a standard 40~dB isolator lies below
the realistic noise-floor of the twin-comb contrast, so single-stage isolation
suffices initially; and loop phase noise pollutes the twin-comb contrast
roughly tenfold before it kills the comb, so the reciprocity test demands a
phase-quiet loop even more than the comb itself does.""",
"""whose regressor is separated in the fit. Finally, two facts matter for the
conditional reciprocity witness: the isolation floor of a standard 40~dB
isolator lies below the realistic noise-floor of the twin-comb contrast, so
single-stage isolation suffices initially; and loop phase noise pollutes the
twin-comb contrast roughly tenfold before it kills the comb, so the witness
demands a phase-quiet loop even more than the comb itself does.""",
"G8b-noise")

# G9 -- three signatures: what they do and do not establish ----------------------------
rep(
"""Observation of the three signatures --- secular exponent, phase-swept revival
comb, single-versus-twin comb down to the isolation floor --- would establish
that the device realizes a two-point transfer kernel of the derived class:
exchange-non-Hermitian, with the anti-holomorphic sector structure of
Section~\\ref{sec:structure}. It would not establish anything beyond that.""",
"""Observation of the three signatures --- secular exponent, phase-swept revival
comb, single-versus-twin comb down to the isolation floor --- would establish
the Jordan structure, the anti-holomorphic sector structure of the surviving
element (Section~\\ref{sec:structure}), and the model-level comb suppression;
establishing strict unidirectionality $G_{12} = 0$ additionally requires the
reverse-injection configuration of Section~\\ref{sec:protocol}. It would not
establish anything beyond that.""",
"G9-signatures")

# G10a -- abstract: spectroscopy scoped to the surviving element ------------------------
rep(
"""Read backwards, the law yields a one-way spectroscopy recovering the winding measure from the relief alone, with proven limits.""",
"""Read backwards, the law yields a spectroscopy of the surviving transfer element, recovering its winding measure from the relief alone, with proven limits.""",
"G10a-abstract-spectro")
rep(
"""(vii) a one-way spectroscopy with proven limits.""",
"""(vii) a spectroscopy of the surviving transfer element, with proven limits.""",
"G10b-contrib-spectro")
rep(
r"""\section{One-way spectroscopy}""",
r"""\section{One-way spectroscopy of the surviving element}""",
"G10c-section-title")

# G11 -- witness paragraph: K_eps named, orientation, matrix link -----------------------
rep(
"""inconclusive --- an entire antisymmetric addition to the kernel changes $R$
without touching any cut.""",
"""inconclusive --- an entire antisymmetric addition to the kernel changes $R$
without touching any cut (explicitly: $K_{\\varepsilon} = \\varepsilon\\,(X -
Y)$ is entire, has zero cut discontinuity, and carries
$R = 2\\varepsilon (X - Y) \\neq 0$). The two sector cuts are compared with
the same orientation, fixed once by the common parametrization of $x$;
physically, the two sector jumps correspond to the two calibrated transfer
configurations ($G_{21}$ and $G_{12}$).""",
"G11-witness-Keps")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print(f"OK: {len(edits)} edits applied -> {DST}")
for e in edits:
    print("  ", e)

# NOTE (applied post-run, same session): three residual fixes H1-H3 --
# outline spectroscopy phrase, abstract and billiard "reciprocity test"
# renamed to (conditional) witness. Integrated directly into the shipped tex;
# anchors: "reads the law backwards into a one-way", the two
# "single-versus-twin-comb reciprocity test" occurrences.
