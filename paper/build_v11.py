#!/usr/bin/env python3
# build_v11.py -- 2026-07-17 (rev2, fail-closed)
# rev2 (same day, eighth-audit catch): python3 -O strips assert statements,
# so the input-sha and anchor-uniqueness guards of rev1 vanished under -O
# and a tampered input could silently produce an altered v11. rev2 is
# fail-closed under every interpreter mode: explicit SystemExit guards,
# and the EXPECTED OUTPUT sha256 is pinned and verified BEFORE the file is
# written. The 15 edits are byte-identical to rev1; the generated v11.tex
# is unchanged (sha256 a801936d...). (revision b, fail-closed)
# Revision b, prompted by the EIGHTH external audit's adversarial test:
# the original (sha b970146d) used `assert` for the input-sha and
# anchor-uniqueness guards, which `python3 -O` strips -- an altered input
# could silently yield a different v11. This revision replaces every
# structural guard by explicit `raise SystemExit` (immune to -O) and adds
# the auditor-suggested OUTPUT sha guard: the script refuses to write
# anything but the canonical v11.tex (sha a801936d). Output byte-identical
# to revision a; only the guard mechanics changed.
# Builds oneway_kernel_paper_v11.tex from oneway_kernel_paper_v10.tex
# (chain: v3 sealed -> build_v5..v10 -> this). Fix basis: SEVENTH external
# adversarial audit (GPT-5.6) of v10; its central catch -- the paper's own
# uniform sinc (Eq. (6)) refutes "absolutely continuous => the calendar is
# forgotten" -- was machine-certified on Anthony's machine (6/6) and graved
# as registry #061 (semantic-debt supersession on the WORDING of #049
# Theorem 3; theorem content intact) BEFORE entering this text. The four
# calendar sites are rewritten as the certified AMPLITUDE dichotomy:
# decaying is not forgetting; zeros, minima positions and relative contrast
# are decided by neither measure class alone. Plus three minor validated
# catches: standalone G12=0 with G21!=0; distinct windings for T_ij; the
# W size law written pointwise then maximized (matches judge #057 J4).

import hashlib, sys

def die(msg):
    raise SystemExit("FAIL-CLOSED: " + msg)

SRC = "oneway_kernel_paper_v10.tex"
DST = "oneway_kernel_paper_v11.tex"
SRC_SHA256 = "98ca664556dc894a18549c3812929e77783be97d1259998151cd877b99754819"

DST_SHA256 = "a801936d3aeb791530fb68ae2485394f069adcedac26f4212d67c145aa2c92ee"

with open(SRC, "rb") as f:
    raw = f.read()
h = hashlib.sha256(raw).hexdigest()
if h != SRC_SHA256:
    raise SystemExit(f"[input] v10.tex sha256 mismatch: {h}")
t = raw.decode("utf-8")

edits = []

def rep(old, new, tag):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit(f"[{tag}] anchor count = {n} (need 1)")
    t = t.replace(old, new)
    edits.append(tag)

# ---------------------------------------------------------------- metadata
rep(r"\date{July 17, 2026 (v10)}", r"\date{July 17, 2026 (v11)}", "Y0a-date")
rep("transfer kernel (v10)}, pdfauthor={Anthony Monnerot}}",
    "transfer kernel (v11)}, pdfauthor={Anthony Monnerot}}", "Y0b-pdftitle")
rep(r"\paragraph{Version note (v10).}", r"\paragraph{Version note (v11).}",
    "Y0c-note-title")
rep("Intermediate drafts v4--v9 existed only",
    "Intermediate drafts v4--v10 existed only", "Y0d-note-window")

# ------------------------- Y1: abstract -- amplitude dichotomy (#061)
rep("""and a discreteness dichotomy (the relief of a finite ladder is Bohr almost periodic, its interference configurations recurring forever; an absolutely continuous continuum forgets its calendar).""",
    """and an amplitude dichotomy (the relief of a finite ladder is Bohr almost periodic and cannot decay; the amplitude of an absolutely continuous continuum dies away --- the persistence of the interference minima being a separate property, exemplified by the uniform sinc whose exact zeros recur forever).""",
    "Y1-abstract-amplitude")

# ------------------------------------- Y2: contribution (v) -- amplitude
rep("""a discreteness dichotomy for the log-scale calendar;""",
    """an amplitude dichotomy for the continuum limit (decay of amplitude, not oblivion of the minima);""",
    "Y2-contribution-v")

# ---------------------------------------------- Y3: outline -- amplitude
rep("""the Fourier floor theorem, settles the fate of the calendar in the
continuum limit, and computes""",
    """the Fourier floor theorem, establishes the amplitude dichotomy of the
continuum limit --- and its boundary: amplitude decay does not erase the
minima --- and computes""",
    "Y3-outline-amplitude")

# ------------------------------------------ Y4: Sec. 4 opening -- amplitude
rep("""settles
the fate of the log-scale calendar of Section~\\ref{sec:calendar} in the
continuum limit, and computes""",
    """establishes
the amplitude dichotomy of the continuum limit for the log-scale calendar
of Section~\\ref{sec:calendar}, and computes""",
    "Y4-sec4-amplitude")

# --------------------------------------- Y5: Sec. 4.3 opener -- amplitude
rep("""The theorem's sharpest consequence concerns the long-range destiny of
the calendar of Section~\\ref{sec:calendar}, and splits on the nature of
the measure.""",
    """The theorem's sharpest consequence concerns the long-range amplitude of
the relief carrying the calendar of Section~\\ref{sec:calendar}, and
splits on the nature of the measure.""",
    "Y5-tides-opener")

# ----------------------- Y6: Bohr side -- non-null finite choir cannot decay
rep("""recurs within any tolerance infinitely often, and the deep rendezvous
recur forever""",
    """recurs within any tolerance infinitely often --- in particular a
non-null finite choir cannot decay to zero --- and the deep rendezvous
recur forever""",
    "Y6-bohr-cannot-decay")

# ------------------------------------ Y7: "whole profile" -> amplitude only
rep("""term scales as $1/(ua)$: the whole profile dies on far windows""",
    """term scales as $1/(ua)$: the maximal amplitude dies on far windows""",
    "Y7-amplitude-dies")

# ----------------- Y8: THE core -- amplitude dichotomy + in-paper sinc (#061)
rep("""$1/u$). The log-scale calendar is therefore a \\emph{discreteness}
phenomenon: a finite ladder keeps it forever, an absolutely continuous
continuum of windings forgets it and the tear heals at large scale. Singular""",
    """$1/u$). The dichotomy is therefore one of \\emph{amplitude}: a finite
ladder's relief cannot decay, while an absolutely continuous continuum's
amplitude dies away. Amplitude decay, however, does not erase the
calendar: the persistence of zeros, the positions of the minima and the
relative window contrast are decided by neither class alone --- the
uniform measure, whose closed form is computed in the next subsection, is
absolutely continuous, yet its sinc transform keeps exact zeros at
$u_n = 2\\pi n/(b-a)$ forever, with window contrast equal to one on every
far window containing one (machine: contrast $0.9999999996$ at
$u \\approx 1.9 \\times 10^{7}$ while the maximal amplitude fell a
thousandfold). Singular""",
    "Y8-amplitude-core-061")

# ------------------------------- Y9: standalone one-wayness (G21 nonzero)
rep("""one-wayness itself lives in $G_{12} = 0$ on the matrix kernel, never in the""",
    """one-wayness itself lives in $G_{12} = 0$ with $G_{21} \\neq 0$ on the
matrix kernel, never in the""",
    "Y9-G21-nonzero")

# --------------------------------------- Y10: distinct windings for T_ij
rep(r"""with pairwise beat periods $T_{ij} = 2\pi/|\nu_i - \nu_j|$ and a single""",
    r"""with pairwise beat periods $T_{ij} = 2\pi/|\nu_i - \nu_j|$ between
distinct windings ($\nu_i \neq \nu_j$) and a single""",
    "Y10-Tij-distinct")

# ---------------------- Y11: W size law pointwise then maximized (#057 J4)
rep(r"""exact law $\max|W| = |1-\rho|\,|D|$. All clauses""",
    r"""exact pointwise law $W(x) = (1-\rho)\,D(x)$ --- hence
$\max_x|W| = |1-\rho|\,\max_x|D(x)|$. All clauses""",
    "Y11-W-pointwise")

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

# --- negative: seventh-audit catches gone; earlier fixes alive
forbid("(v10)", "meta")
forbid("v4--v9", "meta")
forbid("discreteness dichotomy", "Y1")
forbid("forgets its calendar", "Y1")
forbid("settles the fate", "Y3")
forbid("the whole profile dies", "Y7")
forbid("forgets it and the tear heals", "Y8")
forbid(r"\emph{discreteness}", "Y8")
forbid(r"$\max|W| = |1-\rho|\,|D|$", "Y11")
forbid("one-way but algebraic kernel", "v10-regression")
forbid("sector-preserving calibrations", "v10-regression")
forbid("minima keep their positions", "v10-regression")
forbid("purely atomic", "v8-regression")
forbid("potentially new", "v8-regression")
exact("reciprocal control", "two-kept", 2)

# --- positive: new clauses + regression guards
exact("(v11)", "meta", 3)
require("v4--v10", "meta", 1)
require("amplitude dichotomy", "Y", 4)
require("cannot decay", "Y", 3)
require("decided by neither class alone", "Y8", 1)
require(r"u_n = 2\pi n/(b-a)", "Y8", 1)
require("exact zeros", "Y8", 1)
require(r"with $G_{21} \neq 0$", "Y9", 1)
require(r"\nu_i \neq \nu_j", "Y10", 1)
require(r"W(x) = (1-\rho)\,D(x)", "Y11", 1)
require("Bohr almost periodic and cannot decay", "Y1", 1)
require("real-offset (scalar) control", "regression", 4)
require("apparently new", "regression", 2)
require("port basis $C = I$, its certified domain", "regression", 1)
require(r"0 < \alpha < 2", "regression", 1)
require("commensurable", "regression", 1)
require("specified but not simulated", "regression", 2)
require("of the surviving element", "regression", 3)
require(r"R_{\mathbf{G},C} = \mathbf{G} - S_C(\mathbf{G})", "regression", 1)

if fails:
    print(f"SWEEP FAILED ({len(fails)}):")
    for f_ in fails:
        print("  ", f_)
    sys.exit(1)

out_sha = hashlib.sha256(t.encode("utf-8")).hexdigest()
if out_sha != DST_SHA256:
    raise SystemExit(f"[output] v11.tex sha256 mismatch: {out_sha}")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print(f"OK: {len(edits)} edits applied -> {DST}")
for e in edits:
    print("  ", e)
print("SWEEPS: negative + positive + regression guards all PASS (normalized text)")
print("sha256:", hashlib.sha256(t.encode("utf-8")).hexdigest())
