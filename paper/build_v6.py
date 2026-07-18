#!/usr/bin/env python3
# build_v6.py -- 2026-07-16
# Builds oneway_kernel_paper_v6.tex from oneway_kernel_paper_v5.tex
# (itself reproducible from the sealed v3 via build_v5.py -- auditable chain).
# Fix basis: external adversarial audit of v5 (GPT-5.6), each catch verified
# on the tex; plus two hand-verified math sharpenings (C-weighted blindness
# v^T C (K - K^sharp) v = 0; floor-theorem complex-weight hypotheses).

SRC = "oneway_kernel_paper_v5.tex"
DST = "oneway_kernel_paper_v6.tex"

with open(SRC, encoding="utf-8") as f:
    t = f.read()

edits = []

def rep(old, new, tag):
    global t
    n = t.count(old)
    assert n == 1, f"[{tag}] anchor count = {n} (need 1)"
    t = t.replace(old, new)
    edits.append(tag)

# F0 -- date bump ------------------------------------------------------------
rep(r"\date{July 16, 2026 (v5)}", r"\date{July 16, 2026 (v6)}", "F0-date")

# F1 -- intro: Bergman no longer "on the reciprocal side" ---------------------
rep(
"""with the reproducing-kernel and paired-sum constructions as certified
counterexamples on the reciprocal side.""",
"""with the paired-sum constructions as certified reciprocal counterexamples
and the reproducing-kernel (Bergman) form as the certified Hermitian decoy
($\\Delta = 0$, $R \\neq 0$).""",
"F1-intro-side")

# F2 -- intro: non-reciprocity is not defined by breaking Delta ---------------
rep(
"""dynamical generator, not of any drive; and non-reciprocity, implemented at the
level of the generator (Lindblad-type one-way coupling), breaks precisely the
conjugation-exchange symmetry that reality locking enforces.""",
"""dynamical generator, not of any drive; and one-way coupling, implemented at
the level of the generator (Lindblad-type), deletes the conjugate-paired
sector that reality locking enforces and, independently, breaks the
reciprocity invariant $R = K - S(K)$ on the complete transfer kernel
(Section~\\ref{sec:mirror}).""",
"F2-intro-conflation")

# F3 -- phase-law control: drop "Bergman-type", name it correctly -------------
rep(
"""$\\kappa/\\delta = 0.2$), whereas the reciprocal (Bergman-type,
dilogarithm) control, whose offset is real, has a frozen jump phase at
every point of the cut.""",
"""$\\kappa/\\delta = 0.2$), whereas the real-offset dilogarithm control has a
frozen jump phase at every point of the cut.""",
"F3-control-name")

# F4 -- "twist belongs to the one-way class" ricochet -------------------------
rep(
"""polylogarithm controls agreeing to better than $10^{-9}$). The twist of
the jump belongs to the one-way class; the envelope belongs to the
specimen.""",
"""polylogarithm controls agreeing to better than $10^{-9}$; the symbolic
identities are exact, the $10^{-9}$ figure is the numerical cross-check).
Within the family studied the twist separates the one-way kernel from its
real-offset control; it is not exclusive to the one-way class (a paired
reciprocal kernel with complex offset carries the same twist in both
sectors, Section~\\ref{sec:chiral}), and only the comparative difference
witnesses $R$. The envelope belongs to the specimen.""",
"F4-twist")

# F5 -- calendar "one-way only" ricochet ---------------------------------------
rep(
"""and it is one-way only: the reciprocal control (all $\\nu_k = 0$) is flat
to machine zero, with no minima at all.""",
"""and it separates the kernel from its flat control: the real-offset control
(all $\\nu_k = 0$) is flat to machine zero, with no minima at all.
Reciprocity by itself does not force $\\nu_k = 0$ --- a paired reciprocal
kernel with rotating sectors carries a calendar too --- so the calendar,
like the twist, assigns one-wayness only through the comparative reading.""",
"F5-calendar")

# F6 -- "mute on the reciprocal by design" ricochet ----------------------------
rep(
"""the instrument is \\emph{mute on the reciprocal by design}: a flat relief
falls below the protocol contrast floor and the inversion is refused
rather than hallucinated --- the reciprocal kernel is unreadable, as""",
"""the instrument is \\emph{mute on the flat control by design}: a flat relief
falls below the protocol contrast floor and the inversion is refused
rather than hallucinated --- the flat control is unreadable, as""",
"F6-mute")

# F7 -- "certify one-wayness" oversell -----------------------------------------
rep(
"""would allow one not only to certify one-wayness (the jump-phase witness
of Section~\\ref{sec:chiral}) but to \\emph{read} the composition of the""",
"""would allow one not only to witness broken reciprocity (the comparative
jump witness of Section~\\ref{sec:chiral}: $W \\neq 0 \\Rightarrow R \\neq 0$;
strict unidirectionality $G_{12} = 0$ requires comparing the two calibrated
transfer configurations) but to \\emph{read} the composition of the""",
"F7-certify")

# F8 -- grammar bug (mine, V14b) ------------------------------------------------
rep(
"""transcendental, cross-conjugate, non-mirror-symmetric formula that is
nevertheless carries the mirror partner.""",
"""transcendental, cross-conjugate formula that is not invariant under the
mirror map alone and yet carries the mirror partner under the composed
exchange $M \\circ S$ ($\\Delta = 0$).""",
"F8-grammar")

# F9 -- floor: probability measure -> hypotheses for complex weights -----------
rep(
"""verbatim with $\\mu_N$ a finite complex measure --- the phase reweighting""",
"""by the same argument provided $\\sum_k w_k$ is bounded away from zero and
every bound is read in total variation ($\\|\\mu_N\\|_{\\mathrm{TV}}$ uniformly
bounded), with $\\mu_N$ then a finite complex measure rather than a
probability measure --- the phase reweighting""",
"F9-floor-complex")

# F10 -- size asymmetry: module vs angle (the size-cone lesson) -----------------
rep(
"""without touching any cut. The complex difference is essential: a size
asymmetry ($F_a(X) + \\rho F_a(Y)$, $\\rho \\neq 1$) leaves phase and slope
identical in both sectors and is read only by the modulus of $W$, with the""",
"""without touching any cut. The complex difference is essential: a size
asymmetry ($F_a(X) + \\rho F_a(Y)$, $\\rho > 0$ real, $\\rho \\neq 1$; a
unimodular complex $\\rho$ would instead shift the weight angle, not the
size) leaves phase and slope identical in both sectors and is read only by
the modulus of $W$, with the""",
"F10-size-angle")

# F11 -- S on channel indices: the bridge definition ---------------------------
rep(
"""convergent for $|x| < 1$ (observation and source inside the carrier circle). The""",
"""convergent for $|x| < 1$ (observation and source inside the carrier circle).
Throughout, $K$ denotes this surviving transfer element, $K \\equiv G_{21}$;
the complete two-channel kernel is the matrix with $G_{12} = 0$, and for
matrix-valued kernels the exchange $S$ also transposes the channel indices,
$(S G)_{ij}(\\mathbf{r}_1, \\mathbf{r}_2) = G_{ji}(\\mathbf{r}_2, \\mathbf{r}_1)$
(or its $C$-covariant version): with this definition the scalar element, a
function of the commuting product $\\zb\\wb$, is exchange-symmetric on its own,
while the matrix kernel has $R \\neq 0$ --- reciprocity statements always
refer to the matrix (Section~\\ref{sec:mirror}). The""",
"F11-S-bridge")

# F12 -- blindness: scope to C = I, give the C-weighted form --------------------
rep(
"""$R \\neq 0$. This realizes the general projection blindness
$\\operatorname{diag}(R) = 0$: no same-port (one-point) probe can ever witness
non-reciprocity; the invariant is irreducibly two-point.""",
"""$R \\neq 0$. This realizes a general projection blindness: in the port basis
($C = I$) the diagonal of $R$ vanishes identically, and for a general
symmetric pairing the certified statement is $v^{T} C\\,(K - K^{\\sharp})\\,v
= 0$ for every probe $v$ --- no same-port (one-point) measurement can ever
witness non-reciprocity; the invariant is irreducibly two-point.""",
"F12-blindness")

# F13 -- version note: "expanded repair harness" --------------------------------
rep(
"""is certified by the same exact symbolic harness as the original claims.""",
"""is certified by an expanded repair harness built in the same exact symbolic
discipline as the original claims.""",
"F13-harness")

# F14 -- prior-art: neighbouring class, not the same ----------------------------
rep(
"""such as $-\\log(1 - z\\wb)$; at the formula level they occupy the same
cross-conjugate class as our kernel and served as our principal controls.""",
"""such as $-\\log(1 - z\\wb)$; at the formula level they mix one plain and one
conjugated coordinate ($z\\wb$), a neighbouring cross-conjugate class to our
doubly-conjugated sector ($\\zb\\wb$), and served as our principal controls.""",
"F14-class")

# F15a/b -- "sign combinations" -> "zero/non-zero combinations" ------------------
rep("""axes, all four sign combinations being realized by certified kernels, and""",
    """axes, all four zero/non-zero combinations being realized by certified
kernels, and""", "F15a-signs")
rep("""four sign combinations are realized by certified kernels:""",
    """four zero/non-zero combinations are realized by certified kernels:""",
    "F15b-signs")

# F16 -- spectroscopy scope: reads the measure, not G21 - G12 -------------------
rep(
"""would allow one not only to witness broken reciprocity (the comparative
jump witness of Section~\\ref{sec:chiral}: $W \\neq 0 \\Rightarrow R \\neq 0$;
strict unidirectionality $G_{12} = 0$ requires comparing the two calibrated
transfer configurations) but to \\emph{read} the composition of the
couplings that produce it --- which modes, at which winding speeds, with""",
"""would allow one not only to witness broken reciprocity (the comparative
jump witness of Section~\\ref{sec:chiral}: $W \\neq 0 \\Rightarrow R \\neq 0$;
strict unidirectionality $G_{12} = 0$ requires comparing the two calibrated
transfer configurations) but to \\emph{read} the composition of the
couplings that produce it --- which modes, at which winding speeds, with
what weights. The spectroscopy reads the weighted winding measure of the
surviving element $G_{21}$; it does not, by itself, measure
$G_{21} - G_{12}$ ---""",
"F16-spectro-scope")

# F17 -- twin-comb: conditional witness, bridge to R ----------------------------
rep(
"""and the single-versus-twin revival comb is a direct witness of broken""",
"""and the single-versus-twin revival comb is, within the loop model, a
conditional witness of broken""",
"F17-twin-comb")

# F18 -- classification announcement: scalar formula vs matrix ------------------
rep(
"""\\subsection{Classification of the kernel}

Three independent formula-level properties position the one-way kernel.""",
"""\\subsection{Classification of the kernel}

The classification below concerns the scalar closed form (the content of the
surviving element $G_{21}$); the reciprocity statement lives on the matrix
kernel (Section~\\ref{sec:mirror}). Three independent formula-level
properties position the one-way kernel.""",
"F18-classif-scope")

# F19 -- PDF metadata -----------------------------------------------------------
rep(
r"""\usepackage[colorlinks=true,allcolors=blue]{hyperref}""",
r"""\usepackage[colorlinks=true,allcolors=blue]{hyperref}
\hypersetup{pdftitle={When is anti-holomorphic dependence forced? The one-way
transfer kernel (v6)}, pdfauthor={Anthony Monnerot}}""",
"F19-metadata")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print(f"OK: {len(edits)} edits applied -> {DST}")
for e in edits:
    print("  ", e)
