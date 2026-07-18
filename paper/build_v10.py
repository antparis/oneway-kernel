#!/usr/bin/env python3
# build_v10.py -- 2026-07-17
# Builds oneway_kernel_paper_v10.tex from oneway_kernel_paper_v9.tex
# (chain: v3 sealed -> build_v5..v9 -> this). Fix basis: SIXTH external
# adversarial audit (GPT-5.6) of v9, each catch verified on the tex.
# Two catches land on the v9 repairs themselves (repair-debt class):
#  - the "sector-preserving" S_C transport was WRONG: a block-diagonal
#    C = diag(c1,c2) rescales one sector relative to the other (the
#    calibration is itself a relative SIZE between channels -- the grand
#    ledger strikes again); a C-reciprocal kernel G21 = (c1/c2) F(X),
#    G12 = F(Y) makes the raw witness W fire falsely. v10 restricts the
#    witness to its certified domain (port basis C = I, #057) and flags
#    the covariant reweighting as an OPEN judge target, asserting nothing.
#  - "moduli and angles from N >= 3" contradicted the N = 2 phase
#    translation three lines above: angles act already at N = 2, only the
#    positive moduli are position-inert there (#060, correctly split now).
# Remaining catches: scalar "one-wayness" wording of case (a) (v3-era text,
# the six-round shared blind spot), alpha domain 0 < alpha < 2, global
# period overclaim (beat periods T_ij; commensurability), disc_reciprocal
# subscript, redundant anteriority claim, BV constant, abstract calendar
# phrasing, complex-measure weak-convergence hypothesis repeated.

import hashlib, sys

SRC = "oneway_kernel_paper_v9.tex"
DST = "oneway_kernel_paper_v10.tex"
SRC_SHA256 = "28a8a37c5d3ed50e7a18de4f5dcc4398aa0a36d41a1235006a7ec49051fe9ed6"

with open(SRC, "rb") as f:
    raw = f.read()
h = hashlib.sha256(raw).hexdigest()
assert h == SRC_SHA256, f"[input] v9.tex sha256 mismatch: {h}"
t = raw.decode("utf-8")

edits = []

def rep(old, new, tag):
    global t
    n = t.count(old)
    assert n == 1, f"[{tag}] anchor count = {n} (need 1)"
    t = t.replace(old, new)
    edits.append(tag)

# ---------------------------------------------------------------- metadata
rep(r"\date{July 17, 2026 (v9)}", r"\date{July 17, 2026 (v10)}", "X0a-date")
rep("transfer kernel (v9)}, pdfauthor={Anthony Monnerot}}",
    "transfer kernel (v10)}, pdfauthor={Anthony Monnerot}}", "X0b-pdftitle")
rep(r"\paragraph{Version note (v9).}", r"\paragraph{Version note (v10).}",
    "X0c-note-title")
rep("Intermediate drafts v4--v8 existed only",
    "Intermediate drafts v4--v9 existed only", "X0d-note-window")

# -------------------- X1: one-wayness returned to the matrix, case (a) text
rep("""avoided it. We emphasize that case (a) shows the one-wayness of the kernel and
its transcendence are independent properties: flat weights produce a one-way
but algebraic kernel, and it is the physical double-pole ladder that supplies
the transcendental class.""",
    """avoided it. We emphasize that case (a) shows the algebraic and
transcendental classes are independent of the one-way construction: flat
weights give an \\emph{algebraic} surviving element $G_{21}$, and it is the
physical double-pole ladder that supplies the transcendental class ---
one-wayness itself lives in $G_{12} = 0$ on the matrix kernel, never in the
scalar closed form (Section~\\ref{sec:mirror}).""",
    "X1-case-a-matrix")

# ------------- X2: witness restricted to certified domain C = I (repair-debt)
rep("""the same orientation, fixed once by the common parametrization of $x$ and
transported unchanged under $S_C$ for sector-preserving calibrations
(block-diagonal in the channel basis, the exchange then mapping each sector
cut onto the other without reversing the ray; a channel-mixing $C$ falls
outside the separable-class scope of this witness); physically,""",
    """the same orientation, fixed once by the common parametrization of $x$;
the witness is stated in the port basis $C = I$, its certified domain --- a
general calibration rescales one sector relative to the other, so the raw
difference requires a covariant reweighting, which we flag as an open
certification target rather than assert here; physically,""",
    "X2-witness-portbasis")

# --------------------------- X3: alpha domain + moduli-only inertia at N = 2
rep("""whose deep minimum sits at $u = \\arccos(-\\alpha/2)$ and moves with
$\\alpha$; at $N = 2$ the minima positions are weight-independent for
positive weights (and a negative real weight carries an angle $\\pi$, not a
volume change at all).""",
    """whose deep minimum sits at $u = \\arccos(-\\alpha/2)$ for
$0 < \\alpha < 2$ and moves with $\\alpha$ (beyond, the minimum locks at
$u = \\pi$); at $N = 2$ the minima positions are insensitive to the
positive \\emph{moduli} (and a negative real weight carries an angle $\\pi$,
not a volume change at all).""",
    "X3-alpha-domain")

# --------------------------------------- X4: define Dphi and Dnu explicitly
rep("""for two needles a relative phase $\\Delta\\varphi$ translates the""",
    """for two needles a relative phase $\\Delta\\varphi = \\varphi_2 -
\\varphi_1$ between the weights, with winding split $\\Delta\\nu = \\nu_2 -
\\nu_1$, translates the""",
    "X4-dphi-dnu-defined")

# ---------- X5: calendar -- beat periods, commensurability, moduli vs angles
rep("""class-level in its \\emph{frequency content} --- the period law is an
algebraic identity in the $\\nu_k$, independent of the weight family ---
while the depth, selection and position of its deep minima are set by the
weight moduli and angles from $N \\geq 3$ on (Section~\\ref{sec:relief}); it
is stable under fully randomized choirs of ladders ---""",
    """class-level in its \\emph{frequency content} --- the beat frequencies are
an algebraic identity in the $\\nu_k$, independent of the weight family,
with pairwise beat periods $T_{ij} = 2\\pi/|\\nu_i - \\nu_j|$ and a single
global period only when the winding splits are commensurable (the
two-needle law $T = 2\\pi/|\\Delta\\nu|$ is the certified instance) ---
while the depth, selection and position of its deep minima are set by the
weight moduli from $N \\geq 3$ on and by the weight angles already at
$N = 2$ (the relative-phase translation of Section~\\ref{sec:relief}); it
is stable under fully randomized choirs of ladders ---""",
    "X5-calendar-beats")

# -------------------------- X6: winding carried by the surviving sector alone
rep("""$a = 1 + \\kappa/(2i\\delta)$ of the physical double-pole ladder --- carried
alone by the one-way kernel, whose partner sector is deleted --- makes the""",
    """$a = 1 + \\kappa/(2i\\delta)$ of the physical double-pole ladder --- carried
by the surviving sector alone, the one-way coupling having deleted the
partner sector --- makes the""",
    "X6-surviving-sector")

# ------------------------------------------- X7: disc subscript real-offset
rep(r"$\mathrm{disc}_{\text{one-way}}/\mathrm{disc}_{\text{reciprocal}}",
    r"$\mathrm{disc}_{\text{one-way}}/\mathrm{disc}_{\text{real-offset}}",
    "X7-disc-subscript")

# ------------------------------- X8: redundant anteriority claim converted
rep("""to unity to $10^{-21}$). We are not aware of a published use of the
cut-discontinuity phase law, read comparatively across the two sectors, as a
(sufficient) reciprocity witness; the closest works""",
    """to unity to $10^{-21}$). A published use of the cut-discontinuity phase
law, read comparatively across the two sectors, as a (sufficient)
reciprocity witness appears unreported in the literature we searched; the
closest works""",
    "X8-anteriority-merge")

# ------------------------------------ X9: BV constant includes total variation
rep("""the decay is $O(1/u)$, with constants set by the boundary values of the
density --- for the log-uniform family the boundary term scales as
$1/(ua)$:""",
    """the decay is $O(1/u)$, with constants set by the boundary values and the
total variation of the density --- for the log-uniform family the boundary
term scales as $1/(ua)$:""",
    "X9-bv-constant")

# --------------------------------------------- X10: abstract calendar (Bohr)
rep("""a discreteness dichotomy (finite ladders keep their log-scale interference calendar forever; an absolutely continuous continuum forgets it).""",
    """a discreteness dichotomy (the relief of a finite ladder is Bohr almost periodic, its interference configurations recurring forever; an absolutely continuous continuum forgets its calendar).""",
    "X10-abstract-bohr")

# ------------- X11: complex measures -- weak-convergence hypothesis repeated
rep("""by the same argument provided $\\sum_k w_k$ is bounded away from zero and""",
    """by the same argument --- again under weak convergence of the $\\mu_N$ ---
provided $\\sum_k w_k$ is bounded away from zero and""",
    "X11-weak-convergence")

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

# --- negative: sixth-audit catches gone; earlier fixes alive
forbid("(v9)", "meta")
forbid("v4--v8", "meta")
forbid("one-way but algebraic kernel", "X1")
forbid("sector-preserving calibrations", "X2")
forbid("weight-independent for positive weights", "X3")
forbid("weight moduli and angles from $N \\geq 3$", "X5")
forbid("the period law is an algebraic identity", "X5")
forbid("carried alone by the one-way kernel", "X6")
forbid(r"\mathrm{disc}_{\text{reciprocal}}", "X7")
forbid("We are not aware of a published use", "X8")
forbid("keep their log-scale interference calendar forever", "X10")
forbid("minima keep their positions", "v9-regression")
forbid("produced by one-way coupling makes the", "v9-regression")
forbid("O(1/(ua))", "v9-regression")
forbid("none states", "v9-regression")
forbid("purely atomic", "v8-regression")
forbid("potentially new", "v8-regression")
forbid(r"K \equiv G_{21}", "v7-regression")
exact("reciprocal control", "two-kept", 2)

# --- positive: new clauses + regression guards
exact("(v10)", "meta", 3)
require("v4--v9", "meta", 1)
require("algebraic} surviving element", "X1", 1)
require("one-wayness itself lives in $G_{12} = 0$", "X1", 1)
require("port basis $C = I$, its certified domain", "X2", 1)
require("open certification target", "X2", 1)
require(r"0 < \alpha < 2", "X3", 1)
require(r"locks at $u = \pi$", "X3", 1)
require(r"insensitive to the positive \emph{moduli}", "X3", 1)
require(r"\Delta\varphi = \varphi_2 - \varphi_1", "X4", 1)
require(r"T_{ij} = 2\pi/|\nu_i - \nu_j|", "X5", 1)
require("commensurable", "X5", 1)
require("already at $N = 2$", "X5", 1)
require("by the surviving sector alone", "X6", 1)
require(r"\mathrm{disc}_{\text{real-offset}}", "X7", 1)
require("appears unreported in the literature we searched", "X8", 2)
require("total variation of the density", "X9", 1)
require("Bohr almost periodic, its interference configurations", "X10", 1)
require("again under weak convergence", "X11", 1)
require("real-offset (scalar) control", "regression", 4)
require(r"R_{\mathbf{G},C} = \mathbf{G} - S_C(\mathbf{G})", "regression", 1)
require(r"\mathcal{C}(f)", "regression", 1)
require(r"\arccos(-\alpha/2)", "regression", 1)
require(r"-\Delta\varphi/\Delta\nu", "regression", 1)
require("specified but not simulated", "regression", 2)
require("of the surviving element", "regression", 3)
require("apparently new", "regression", 2)

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
print("SWEEPS: negative + positive + v7/v8/v9-regression all PASS (normalized text)")
print("sha256:", hashlib.sha256(t.encode("utf-8")).hexdigest())
