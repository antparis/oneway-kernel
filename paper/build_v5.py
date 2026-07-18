#!/usr/bin/env python3
# build_v5.py -- 2026-07-16
# Builds oneway_kernel_paper_v5.tex from the SEALED v3 by surgical string
# replacement (asserted unique anchors; v3 never modified). Supersedes the
# internal v4 (blocked: inherited false decoy + residual semantic debt).
# Repair basis: registry #055-#059, all machine + judge certified
# (judge_repair_058_v2.py 14/14, Wirtinger convention).

SRC = "oneway_kernel_paper_v3.tex"
DST = "oneway_kernel_paper_v5.tex"

with open(SRC, encoding="utf-8") as f:
    t = f.read()

edits = []

def rep(old, new, tag):
    global t
    n = t.count(old)
    assert n == 1, f"[{tag}] anchor count = {n} (need 1)"
    t = t.replace(old, new)
    edits.append(tag)

# V1 -- date --------------------------------------------------------------
rep(r"\date{July 10, 2026}", r"\date{July 16, 2026 (v5)}", "V1-date")

# V2 -- abstract: independence statement ----------------------------------
rep(
"""Reciprocity is equivalent to the existence of an
exchange-Hermitian mirror partner of the kernel; unidirectionality removes this
partner.""",
"""Exchange-Hermiticity of the kernel and physical reciprocity are two
independent invariants: the reciprocity content is carried by the exchange
invariant $R = K - S(K)$ alone, evaluated on the complete two-point transfer
kernel, and exchange-Hermitian kernels exist that are not reciprocal (and
conversely), so the mirror partner certifies neither property by itself. The
one-way kernel violates both invariants: unidirectionality deletes the mirror
partner and, independently, makes $R \\neq 0$.""",
"V2-abstract")

# V3 -- abstract: absolutely continuous precision --------------------------
rep("a continuum forgets it)",
    "an absolutely continuous continuum forgets it)",
    "V3-abstract-ac")

# V4 -- contributions (ii) --------------------------------------------------
rep(
"""(ii) a dichotomy --- reciprocity is equivalent
to the presence of an exchange-Hermitian mirror partner of the kernel, and
one-way coupling deletes that partner;""",
"""(ii) an independence theorem --- exchange-Hermiticity
($\\Delta = K - M(S(K))$) and reciprocity ($R = K - S(K)$) are independent
axes, all four sign combinations being realized by certified kernels, and
one-way coupling violates both, deleting the mirror partner and making
$R \\neq 0$ on the complete transfer kernel;""",
"V4-contrib")

# V5+V6 -- version note + section retitle -----------------------------------
rep(
r"""\subsection{Reciprocity as an exchange symmetry; the mirror-partner statement}
\label{sec:mirror}""",
r"""\paragraph{Version note (v5).} This version repairs the reciprocity statement
of the published v3 (DOI 10.5281/zenodo.21317960). Exchange-Hermiticity and
reciprocity, stated as equivalent in v3 (abstract, contribution (ii), and this
section), are independent invariants; the Bergman reproducing kernel, used in
v3 as a reciprocal control, is exchange-Hermitian but not reciprocal
($\Delta = 0$, $R \neq 0$) and is reclassified below as the Hermitian decoy;
the reciprocity invariant must be evaluated on the complete two-point transfer
kernel, the scalar closed form being exchange-symmetric by itself; and the
cut-phase witness is stated comparatively, with its sufficiency-only limit
(Section~\ref{sec:chiral}). No closed form, simulation number, figure, or
protocol changed. The repair was prompted by an external adversarial audit and
is certified by the same exact symbolic harness as the original claims. An
intermediate v4 existed only as an internal draft and was never deposited.

\subsection{Reciprocity and exchange-Hermiticity: two independent invariants}
\label{sec:mirror}""",
"V5V6-note-title")

# V7 -- mirror body: definitions, independence, operator form, trap, table --
rep(
"""\\emph{exchange-Hermitian} when $K = M(S(K))$ up to an additive constant; because
logarithmic branches can contribute a piecewise constant, the operationally safe
test is the constancy of $\\exp\\!\\bigl(K - M(S(K))\\bigr)$. Exchange-Hermiticity
is the formula-level expression of reciprocity: the response from 2 to 1 is the
conjugate of the response from 1 to 2.""",
"""\\emph{exchange-Hermitian} when $K = M(S(K))$ up to an additive constant; because
logarithmic branches can contribute a piecewise constant, the operationally safe
test is the constancy of $\\exp\\!\\bigl(K - M(S(K))\\bigr)$. Alongside
$\\Delta = K - M(S(K))$ we define the \\emph{reciprocity invariant}
$R = K - S(K)$: reciprocity is the statement $R = 0$ (the response from 2 to 1
equals the response from 1 to 2), while $\\Delta = 0$ is an anti-linear
Hermiticity condition. These two invariants are \\emph{independent} ---
conflating them was the error of earlier versions of this paper --- and all
four sign combinations are realized by certified kernels:

\\begin{center}
\\begin{tabular}{lll}
\\hline
quadrant & certified representative & invariants \\\\
\\hline
reciprocal--Hermitian & $g(z,\\zb) + g(w,\\wb)$, real coefficient & $R = 0$, $\\Delta = 0$ \\\\
dissipative reciprocal & $c\\,(g(z,\\zb) + g(w,\\wb))$, $c \\notin \\mathbb{R}$, $M(g) = g$ & $R = 0$, $\\Delta \\neq 0$ \\\\
Hermitian decoy & Bergman $-k\\log(1 - z\\wb)$ & $R \\neq 0$, $\\Delta = 0$ \\\\
one-way & matrix kernel, $G_{21} = f(\\zb\\wb)$, $G_{12} = 0$ & $R \\neq 0$, $\\Delta \\neq 0$ \\\\
\\hline
\\end{tabular}
\\end{center}

The dissipative-reciprocal row requires the stated hypothesis: the complex
coefficient breaks $\\Delta$ only if the building block is itself mirror-fixed
($M(g) = g$, $g \\neq 0$); dissipation is fully compatible with reciprocity, a
point long emphasized in the electromagnetic literature
\\cite{Caloz2018,Silveirinha2019}. At the operator level, with a symmetric
non-degenerate pairing $C$ and the reciprocal transpose
$A^{\\sharp} = C^{-1} A^{T} C$ (no complex conjugation, hence loss-compatible),
$L = L^{\\sharp}$ for the generator is equivalent to $K = K^{\\sharp}$ for the
kernel $K = L^{-1}$, i.e.\\ to $R = 0$; the identity
$(L^{-1})^{\\sharp} = (L^{\\sharp})^{-1}$ and the covariance $R' = U R U^{-1}$
under simultaneous transformation of $L$, $K$, $C$ are certified by the same
exact symbolic harness as the rest of the paper.

Two structural corollaries are certified with them, and the first is critical
for reading this paper. \\emph{The object matters:} the one-way closed form is
a function of the single product $x = \\zb\\wb$, and the product commutes, so
the scalar closed form is exchange-\\emph{symmetric} --- $R$ evaluated on it is
identically zero, a false ``reciprocal'' verdict. Non-reciprocity lives on the
complete two-point transfer kernel, the matrix with the reverse element
vanishing ($G_{21} = f(\\zb\\wb)$, $G_{12} = 0$), and only there is
$R \\neq 0$. This realizes the general projection blindness
$\\operatorname{diag}(R) = 0$: no same-port (one-point) probe can ever witness
non-reciprocity; the invariant is irreducibly two-point. \\emph{Second,} under
an external bias $b$ the Onsager--Casimir relation $K_b = K_{-b}^{\\sharp}$
(device against bias-reversed device) must not be conflated with reciprocity
of the device against itself ($K_b = K_b^{\\sharp}$): a gyrotropic kernel
satisfies the former while violating the latter.""",
"V7-mirror-body")

# V8a -- observation paragraph: Bergman requalified -------------------------
rep(
"""We observe the following dichotomy, verified symbolically on all cases above
and on control kernels. Reciprocal constructions always produce the mirror
partner: the diagonal (reproducing-kernel) sum of a single holomorphic sector,
$-k \\log(1 - z\\wb)$, is exchange-Hermitian exactly; the Hermitian two-sector sum""",
"""We record the following observations, verified symbolically on all cases above
and on control kernels, organized by the two invariants. The diagonal
(reproducing-kernel) sum of a single holomorphic sector, $-k \\log(1 - z\\wb)$,
is exchange-Hermitian exactly --- yet, as a two-point kernel, non-reciprocal
($R \\neq 0$): it realizes the Hermitian-decoy quadrant, and earlier versions
of this paper mislabeled it reciprocal; the Hermitian two-sector sum""",
"V8a-bergman")

# V8b -- log(z-wb) control: Hermiticity axis, not reciprocity ---------------
rep(
"""two-dimensional chiral propagators, is exchange-Hermitian up to a branch
constant ($\\exp(\\Delta) = -1$) and is therefore compatible with reciprocity.""",
"""two-dimensional chiral propagators, is exchange-Hermitian up to a branch
constant ($\\exp(\\Delta) = -1$) and therefore lies on the Hermiticity axis up
to that constant; its $R$ is a separate question, not needed here.""",
"V8b-branch-control")

# V8c -- closing summary -----------------------------------------------------
rep(
"""restores the conjugate-exchanged term. We summarize this as: reciprocity is
equivalent to the presence of the exchange-Hermitian mirror partner;
one-wayness removes it, and the unpaired anti-holomorphic half survives alone.""",
"""restores the conjugate-exchanged term. We summarize this as: the mirror
partner marks exchange-Hermiticity, not reciprocity; the reciprocity statement
is carried by $R = K - S(K)$ on the complete transfer kernel. One-wayness
removes the partner and, independently, breaks $R$; the unpaired
anti-holomorphic half survives alone.""",
"V8c-summary")

# V9 -- classification: controls are exchange-Hermitian, not "reciprocal" ---
rep(
"""non-pairing: $K$ is not invariant under the mirror map, and no mirror partner
accompanies it, in contrast with every reciprocal control.""",
"""non-pairing: $K$ is not invariant under the mirror map, and no mirror partner
accompanies it, in contrast with the exchange-Hermitian controls above.""",
"V9-classification")

# V10 -- certification methodology -------------------------------------------
rep(
"""derivatives, the pairing tests, the exchange-Hermiticity dichotomy including
its branch-safe form""",
"""derivatives, the pairing tests, the exchange-Hermiticity axis and the
independent reciprocity invariant $R$, including the branch-safe form""",
"V10-methodology")

# V11 -- floor theorem: AC precision + singular-continuous gap ---------------
rep(
"""phenomenon: a finite ladder keeps it forever, a continuum of windings
forgets it and the tear heals at large scale. No novelty is claimed for""",
"""phenomenon: a finite ladder keeps it forever, an absolutely continuous
continuum of windings forgets it and the tear heals at large scale. Singular
continuous measures form a third class, not treated here: their transforms
need not decay (the middle-thirds Cantor measure persists on the subsequence
$u_n = 2\\pi\\,3^n$), and no universal destiny is claimed for them. No novelty
is claimed for""",
"V11-sc-gap")

# V12 -- comparative witness + scope in sec:chiral ----------------------------
rep(
"""The law was subsequently stress-tested across coupling strengths and""",
"""Within the family studied here the reciprocal control has a real offset, so
the frozen-versus-rotating dichotomy separates the two kernels. The rotation
alone, however, is not a standalone reciprocity witness: for a separable
kernel $F_a(X) + F_a(Y)$ with the same complex offset in both sectors, each
sector carries the same rotating jump phase while the kernel is exactly
reciprocal ($R = 0$). The repaired witness is \\emph{comparative}: with
$W(x) = D_X(x) - D_Y(x)$ the complex difference of the two sector jumps,
$W \\neq 0$ implies $R \\neq 0$ (the witness is sufficient), while $W = 0$ is
inconclusive --- an entire antisymmetric addition to the kernel changes $R$
without touching any cut. The complex difference is essential: a size
asymmetry ($F_a(X) + \\rho F_a(Y)$, $\\rho \\neq 1$) leaves phase and slope
identical in both sectors and is read only by the modulus of $W$, with the
exact law $\\max|W| = |1-\\rho|\\,|D|$. All clauses (refusal on the reciprocal
counterexample, firing on the one-way, size and speed columns, and the
inconclusive limit) are certified by the same exact symbolic harness. The
witness is established in the separable class $K = F(X) + G(Y)$ with two
sectors; outside that class the sector jumps need not be separately defined,
and no claim is made there.

The law was subsequently stress-tested across coupling strengths and""",
"V12-witness")

# V13 -- novelty sentence: comparative framing --------------------------------
rep(
"""We are not aware of a published use of the
cut-discontinuity phase law as a reciprocity witness;""",
"""We are not aware of a published use of the
cut-discontinuity phase law, read comparatively across the two sectors, as a
(sufficient) reciprocity witness;""",
"V13-novelty")

# V14a -- prior-art reproducing kernels: kill the "i.e." ----------------------
rep(
"""construction --- they are exactly exchange-Hermitian, i.e., they belong to the
reciprocal class. In our terms, they always come with their mirror partner. Our""",
"""construction --- they are exactly exchange-Hermitian. In the invariant table
of Section~\\ref{sec:mirror} this marks the Hermiticity axis $\\Delta = 0$, not
reciprocity: as a two-point kernel the Bergman form has $R \\neq 0$, occupying
the Hermitian-decoy quadrant. In our terms, they always come with their mirror
partner. Our""",
"V14a-priorart-bergman")

# V14b -- "fully compatible with reciprocity" --------------------------------
rep(
"""nevertheless fully compatible with reciprocity. The exchange-Hermiticity test""",
"""nevertheless carries the mirror partner. The exchange-Hermiticity test""",
"V14b-priorart-decoy")

# V15 -- prior-art cascaded: independence, not equivalence --------------------
rep(
"""transcendence class), and the statement that reciprocity at kernel level is
equivalent to the presence of the exchange-Hermitian mirror partner. To our
knowledge the kernel-level dichotomy is not stated in the cascaded-systems
literature.""",
"""transcendence class), and the statement that exchange-Hermiticity and
reciprocity are independent kernel-level invariants, the one-way kernel
violating both. To our knowledge this kernel-level independence table is not
stated in the cascaded-systems literature.""",
"V15-priorart-cascaded")

# V16 -- conclusion ------------------------------------------------------------
rep(
"""produces a Lerch-transcendent kernel whose exchange-Hermitian mirror partner is
absent, whereas every reciprocal construction we tested retains that partner.""",
"""produces a Lerch-transcendent kernel whose exchange-Hermitian mirror partner
is absent and whose reciprocity invariant $R = K - S(K)$, evaluated on the
complete two-point transfer kernel (the scalar closed form alone is
exchange-symmetric and blind to it), is non-zero --- two independent
violations that jointly characterize one-wayness at formula level.""",
"V16-conclusion")

# V17 -- bibliography: two verified primary sources ---------------------------
rep(
r"""\bibitem{Colom2023}""",
r"""\bibitem{Caloz2018} C.~Caloz, A.~Al\`u, S.~Tretyakov, D.~Sounas, K.~Achouri,
and Z.-L. Deck-L\'eger, Electromagnetic nonreciprocity,
Phys. Rev. Applied \textbf{10}, 047001 (2018).
\bibitem{Silveirinha2019} M.~G.~Silveirinha, Hidden time-reversal symmetry in
dissipative reciprocal systems, Opt. Express \textbf{27}, 14328--14337 (2019).
\bibitem{Colom2023}""",
"V17-bib")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print(f"OK: {len(edits)} edits applied -> {DST}")
for e in edits:
    print("  ", e)
