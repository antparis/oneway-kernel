#!/usr/bin/env python3
# build_v8.py -- 2026-07-17
# Builds oneway_kernel_paper_v8.tex from oneway_kernel_paper_v7.tex
# (chain: v3 sealed -> build_v5.py -> v5 -> build_v6.py -> v6 -> build_v7.py
#  (+H1-H3 folded into the shipped v7) -> v7 -> this).
# Canonical input: the SHIPPED v7.tex, sha256 6570569f... (H1-H3 already in),
# which restores full patcher reproducibility from v8 onward (rule 3l).
# Fix basis: fourth external adversarial audit (GPT-5.6) of v7, each catch
# verified on the tex; plus session catches 2026-07-17 (per-occurrence
# decisions on "reciprocal control"; v4--v7 history window; metadata sweep;
# X/Y definitions with NO W<->R_G identity asserted -- witness stays
# sufficient-only per registry #057/#057b deposit gate).
#
# Per-occurrence decisions on the seven "reciprocal control":
#   - abstract, sec 3.2, sec 3.3, sec 4.2 (x2): renamed "real-offset
#     (scalar) control" (reserve "reciprocal" for the paired matrix level);
#   - version note ("used in v3 as a reciprocal control"): KEPT -- it is a
#     historical statement about v3's own label;
#   - Fig. 2 caption ("Bottom: reciprocal control"): KEPT -- the bottom panel
#     is the two-way coupled loop configuration (G12 restored), a genuinely
#     matrix-level reciprocal device control, which is exactly the usage the
#     vocabulary rule reserves the word for.
# Expected post-build count of "reciprocal control": exactly 2.

import hashlib, sys

SRC = "oneway_kernel_paper_v7.tex"
DST = "oneway_kernel_paper_v8.tex"
SRC_SHA256 = "6570569fd88405eb06ed75c59ec64c773fdd2365131b55ce56d0d750eeba30ea"

with open(SRC, "rb") as f:
    raw = f.read()
h = hashlib.sha256(raw).hexdigest()
assert h == SRC_SHA256, f"[input] v7.tex sha256 mismatch: {h}"
t = raw.decode("utf-8")

edits = []

def rep(old, new, tag):
    global t
    n = t.count(old)
    assert n == 1, f"[{tag}] anchor count = {n} (need 1)"
    t = t.replace(old, new)
    edits.append(tag)

# ---------------------------------------------------------------- metadata
rep(r"\date{July 16, 2026 (v7)}",
    r"\date{July 17, 2026 (v8)}",
    "V0a-date")

rep("transfer kernel (v6)}, pdfauthor={Anthony Monnerot}}",
    "transfer kernel (v8)}, pdfauthor={Anthony Monnerot}}",
    "V0b-pdftitle")

# ------------------------------------------------- 3a: final K/G collision
rep(r"K(\mathbf{r}_1;\mathbf{r}_2) \;=\; \sum_{m \geq 1} g_m\, x^m,",
    r"G_{21}(\mathbf{r}_1;\mathbf{r}_2) \;=\; \sum_{m \geq 1} g_m\, x^m,",
    "V1a-eq2-G21")

rep(r"  K \;=\; -\frac{k}{\delta^{2}} \left[\, \Phi(x, 2, c) - \frac{1}{c^{2}} \,\right],",
    r"  G_{21} \;=\; -\frac{k}{\delta^{2}} \left[\, \Phi(x, 2, c) - \frac{1}{c^{2}} \,\right],",
    "V1b-eq3-G21")

rep("""is absent and whose reciprocity invariant $R = K - S(K)$, evaluated on the""",
    """is absent and whose reciprocity invariant $R_{\\mathbf{G}} = \\mathbf{G} - S(\\mathbf{G})$, evaluated on the""",
    "V1c-conclusion-RG")

# ------------------------------- 3b: reciprocal control -> real-offset (5/7)
rep("separating the one-way kernel from its reciprocal control",
    "separating the one-way kernel from its real-offset (scalar) control",
    "V2a-abstract")

rep("""Within the family studied here the reciprocal control has a real offset, so
the frozen-versus-rotating dichotomy separates the two kernels.""",
    """Within the family studied here the control is the real-offset (scalar)
one, so the frozen-versus-rotating dichotomy separates the two kernels.""",
    "V2b-chiral")

rep("""extrema appearing), while the reciprocal control remains flat at
machine precision throughout.""",
    """extrema appearing), while the real-offset (scalar) control remains flat at
machine precision throughout.""",
    "V2c-relief")

rep("""threads. First, the reciprocal control is now a theorem line: all""",
    """threads. First, the real-offset (scalar) control is now a theorem line: all""",
    "V2d-theorem-line")

rep("""relief on every window --- the machine-flat reciprocal controls of""",
    """relief on every window --- the machine-flat real-offset (scalar) controls of""",
    "V2e-corollary")

# -------------------- 3c: protocol conditionality + phase-referenced reading
rep("""; the test therefore reads the
mirror-deletion statement of Section~\\ref{sec:mirror} directly on an
oscilloscope, down to that floor.""",
    """; within the loop model the test
therefore reads the modulus asymmetry implied by the mirror-deletion
statement of Section~\\ref{sec:mirror} directly on an oscilloscope, down to
that floor; the complex invariant $R_{\\mathbf{G}}$ itself is not read on a
modulus trace --- its direct measurement requires the reverse-injection,
phase-referenced acquisition of (iii).""",
    "V3a-oscilloscope-scope")

rep("""measurement of $R_{\\mathbf{G}}$ additionally requires the reverse-injection
acquisition ($G_{12}$: pulse the counter-clockwise port) alongside the
forward one.""",
    """measurement of $R_{\\mathbf{G}}$ additionally requires the reverse-injection
acquisition ($G_{12}$: pulse the counter-clockwise port) alongside the
forward one, with phase-referenced detection in both configurations
(heterodyne or quadrature demodulation against a common reference, the
calibration $C$ fixed once): $R_{\\mathbf{G}}$ is complex-valued, and
modulus-only records are mirror-blind (Section~\\ref{sec:limits}).""",
    "V3b-protocol-iii")

rep("""weighted winding measure of the surviving element $G_{21}$; it does not, by
itself, measure $G_{21} - G_{12}$. We state this as an
outlook on the mathematics of the kernel, not as an experimental claim.""",
    """weighted winding measure of the surviving element $G_{21}$; it does not, by
itself, measure $G_{21} - G_{12}$. Two acquisition-level caveats bound this
reading. The witness $W$ is a complex difference of cut discontinuities,
while Section~\\ref{sec:limits} proves modulus-only records mirror-blind:
reading $W$, like any direct access to $R_{\\mathbf{G}}$, requires
phase-referenced acquisition. Within the model, a known injected reference
needle restores the missing phase: demodulating the relief against the
reference beat recovers the complex transform from modulus-only records
(quadrature pair), lifting the mirror ambiguity of
Section~\\ref{sec:limits}; the scheme and its exact demodulation law are
certified in the repository accompanying this deposit, for the weight class
certified there. We state this as an
outlook on the mathematics of the kernel, not as an experimental claim.""",
    "V3c-outlook-052")

# ------------------------- 3d: define X, Y, D_X, D_Y; orientation under S_C
# (session decision: NO identity relating W to R_G is asserted -- the
#  witness stays sufficient-only, per the #057 FINDINGS deposit gate)
rep("""alone, however, is not a standalone reciprocity witness: for a separable
kernel $F_a(X) + F_a(Y)$ with the same complex offset in both sectors, each""",
    """alone, however, is not a standalone reciprocity witness. Write
$X = \\zbone \\wbtwo$ and $Y = \\bar{z}_2\\, \\bar{w}_1$ for the two sector
variables --- the arguments of the two transfer configurations ($G_{21}$
and $G_{12}$ respectively, with $S(X) = Y$) --- and $D_X$, $D_Y$ for the
cut discontinuities of the kernel in each sector variable, taken across the
same ray. For a separable
kernel $F_a(X) + F_a(Y)$ with the same complex offset in both sectors, each""",
    "V3d1-XY-definition")

rep("""The two sector cuts are compared with
the same orientation, fixed once by the common parametrization of $x$;
physically, the two sector jumps correspond to the two calibrated transfer
configurations ($G_{21}$ and $G_{12}$).""",
    """The two sector cuts are compared with
the same orientation, fixed once by the common parametrization of $x$ and
transported unchanged under $S_C$ (the exchange maps each sector cut onto
the other without reversing the ray); physically, the two sector jumps
correspond to the two calibrated transfer configurations ($G_{21}$ and
$G_{12}$).""",
    "V3d2-orientation-SC")

# --------------------------------------- 3e: the phase sentence (G4, FALSE)
rep("""change). Relative complex phases between the weights reweight which minima
dominate rather than translating them --- a phase common to all weights
leaves the modulus relief invariant (the detailed window-dependence of the
relative-phase effect was diagnosed and is recorded in the repository).""",
    """change). Relative complex phases between the weights move the pattern
itself: for two needles a relative phase $\\Delta\\varphi$ translates the
interference minima by $\\Delta\\varphi/\\Delta\\nu$ in logarithmic scale
($u = \\ln x$, Section~\\ref{sec:calendar}), and for three or more needles it
deforms the pattern --- minima shift and their relative depths change ---
rather than acting as a volume knob; a phase common to all weights
leaves the modulus relief invariant (the detailed window-dependence of the
relative-phase effect was diagnosed and is recorded in the repository).""",
    "V3e-phases-translate")

# ------------------------------- 3f: calendar scoped to real positive weights
rep("""class-level --- independent of the weight family (an algebraic identity
in the $\\nu_k$) and stable under fully randomized choirs of ladders ---""",
    """class-level --- independent of the weight family among real positive
weights (an algebraic identity in the $\\nu_k$; relative complex phases
translate and deform the calendar, Section~\\ref{sec:relief}) and stable
under fully randomized choirs of ladders ---""",
    "V3f-calendar-scope")

# -------------------------------------------------- 3g: version note repairs
rep(r"\paragraph{Version note (v7).}",
    r"\paragraph{Version note (v8).}",
    "V3g1-note-title")

rep("""(Section~\\ref{sec:chiral}). No closed form, simulation number, figure, or
protocol changed. The repair was prompted""",
    """(Section~\\ref{sec:chiral}). No closed form, simulation number, or figure
changed; the measurement protocol was strengthened with the
reverse-injection acquisition and the phase-referenced detection that a
direct measurement of $R_{\\mathbf{G}}$ requires. The repair was prompted""",
    "V3g2-note-protocol")

rep("Intermediate drafts v4--v6 existed only",
    "Intermediate drafts v4--v7 existed only",
    "V3g3-note-window")

# ----------------------------------------- 3h: anteriority deflation (4 sites)
rep("""what we believe has no
direct precedent is the combination""",
    """what we did not find a direct
precedent for in our search is the combination""",
    "V3h1-sec6-opening")

rep("""violating both. To our knowledge this kernel-level independence table is not
stated in the cascaded-systems literature.""",
    """violating both. We did not find this kernel-level independence table stated
in the cascaded-systems literature covered by our search.""",
    "V3h2-cascaded")

rep("""The secular envelope itself is therefore not claimed as new; its
use as a cheap, noise-robust certification channel for one-way kernels is.""",
    """The secular envelope itself is therefore not claimed as new; what appears
new in our search is its use as a cheap, noise-robust certification channel
for one-way kernels.""",
    "V3h3-envelope")

rep("what we read as potentially new --- the",
    "what we read as apparently new --- the",
    "V3h4-apparently")

# ------------------------------------------------------- 3i: quadrant table
rep(r"reciprocal--Hermitian & $g(z,\zb) + g(w,\wb)$, real coefficient & $R = 0$, $\Delta = 0$ \\",
    r"reciprocal--Hermitian & $g(z,\zb) + g(w,\wb)$, real coefficient, $M(g) = g$ & $R = 0$, $\Delta = 0$ \\",
    "V3i1-table-row1")

rep(r"Hermitian decoy & Bergman $-k\log(1 - z\wb)$ & $R \neq 0$, $\Delta = 0$ \\",
    r"Hermitian decoy & Bergman $-k\log(1 - z\wb)$, $k \in \mathbb{R}$ & $R \neq 0$, $\Delta = 0$ \\",
    "V3i2-table-bergman")

# ------------------------------------------------------------ 3j: S vs S_C
rep("""Let $S$ denote the exchange of the two points, $(z, \\zb) \\leftrightarrow (w, \\wb)$,
and let the mirror map $M$ act""",
    """Let $S$ denote the exchange of the two points, $(z, \\zb) \\leftrightarrow (w, \\wb)$
(for matrix-valued kernels $S$ is understood in the port basis, $C = I$, so
that $S \\equiv S_C$; a general calibration enters through the $S_C$ of
Section~\\ref{sec:closedform}, and the invariant is then written
$R_{\\mathbf{G},C}$),
and let the mirror map $M$ act""",
    "V3j-S-SC")

# --------------------------------------- 3k: purely atomic -> finitely supported
rep("""the measure. If $\\mu$ is \\emph{purely atomic} --- any finite choir ---""",
    """the measure. If $\\mu$ is \\emph{finitely supported} --- any finite choir ---""",
    "V3k-finitely-supported")

# ============================== SWEEPS =====================================
# All checks run on whitespace-normalized text (hard line wraps must never
# hide a phrase -- the grep-channel lesson of 2026-07-17).
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

# --- negative sweep: forbidden phrases (audit v7 + history) ---
forbid("purely atomic", "3k")
forbid("potentially new", "3h")
forbid("reweight which minima dominate rather than translating", "3e")
forbid("figure, or protocol changed", "3g")
forbid("the test therefore reads the mirror-deletion statement", "3c")
forbid("what we believe has no direct precedent", "3h")
forbid("independence table is not stated", "3h")
forbid("(v6)", "meta")
forbid("(v7)", "meta")
forbid("jointly characterize", "v7-G6-regression")
forbid(r"K \equiv G_{21}", "v7-G1a-regression")
forbid("a one-way spectroscopy with proven limits", "v7-G10-regression")
exact("reciprocal control", "3b-two-kept", 2)

# --- positive sweep: required clauses + v7-fix regression guards ---
require("real-offset (scalar) control", "3b", 4)
require("real-offset (scalar) controls", "3b-plural", 1)
if flat.lower().count("conditional reciprocity witness") < 2:
    fails.append("POSITIVE [v7-G8]: 'conditional reciprocity witness' < 2")
require(r"R_{\mathbf{G}}", "RG", 4)
require(r"S \equiv S_C", "3j", 1)
require(r"R_{\mathbf{G},C}", "3j", 1)
require("of the surviving element", "v7-G10", 3)
require(r"K_{\varepsilon}", "v7-G11", 1)
require("exhibited by the one-way construction", "v7-G6", 1)
require("apparently new", "3h", 2)
require("finitely supported", "3k", 1)
require("phase-referenced", "3c", 3)
exact("$M(g) = g$", "3i", 3)  # table row1 (new) + row2 + C1 prose hypothesis
require("v4--v7", "3g", 1)
exact("(v8)", "meta", 3)
require(r"\Delta\varphi/\Delta\nu", "3e", 1)
require(r"w_k \geq 0", "v7-G5a-regression", 1)
require("for the weight class certified there", "052-scope", 1)
require(r"X = \zbone \wbtwo", "3d", 1)
require(r"G_{21}(\mathbf{r}_1;\mathbf{r}_2)", "3a-eq2", 1)
require(r"R_{\mathbf{G}} = \mathbf{G} - S(\mathbf{G})", "3a", 2)
require("transported unchanged under $S_C$", "3d-orientation", 1)

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
print("SWEEPS: negative + positive + v7-regression all PASS (normalized text)")
print("sha256:", hashlib.sha256(t.encode("utf-8")).hexdigest())
