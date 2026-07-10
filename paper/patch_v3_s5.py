#!/usr/bin/env python3
"""S5 patcher: six surgical edits bringing intro/abstract/discussion to the
level of the new content. Single-line anchors only (wrap-safe). In-place
with dated backup. Run from paper/."""
import shutil

F = "oneway_kernel_paper_v3.tex"
shutil.copyfile(F, F + ".bak-s5")
src = open(F, encoding="utf-8").read()

edits = []

# 1. Abstract extension
A1 = "significantly more demanding in terms of loop-phase stability."
N1 = A1 + (" Beyond the protocol, we characterize the kernel's intrinsic"
" analyticity boundary at $|x| = 1$ --- emergent from the mode ladder, with"
" a chiral phase law of its branch-cut discontinuity separating the one-way"
" kernel from its reciprocal control --- and prove an elementary Fourier"
" floor theorem for the interference relief along the cut: the residual"
" relief of large kernel sums is the window-contrast of the Fourier"
" transform of the weighted winding measure, with closed-form floors for"
" the canonical ladder families and a discreteness dichotomy (finite"
" ladders keep their log-scale interference calendar forever; a continuum"
" forgets it). Read backwards, the law yields a one-way spectroscopy"
" recovering the winding measure from the relief alone, with proven"
" limits.")
edits.append((A1, N1))

# 2. Contributions (iv)-(vii)
A2 = "counterexamples on the reciprocal side."
N2 = A2 + (" At the level of machine-verified simulation and one elementary"
" hand proof, we further establish: (iv) the kernel's intrinsic, emergent"
" analyticity boundary and the chiral phase law of its cut, with"
" class-level genericity; (v) a Fourier floor theorem for the interference"
" relief of large kernel sums, with sampling-dependent convergence rates"
" and a discreteness dichotomy for the log-scale calendar; (vi) closed-form"
" floors for the canonical ladder families; (vii) a one-way spectroscopy"
" with proven limits.")
edits.append((A2, N2))

# 3. Final contribution sentence
A3 = "is a sharply posed question, a certified structural dichotomy, and a"
N3 = ("is a sharply posed question, a certified structural dichotomy, an"
" elementary machine-faced floor theorem with closed-form consequences, an"
" inverse instrument whose limits are proven, and a")
edits.append((A3, N3))

# 4. Outline rewrite (two-line anchor, wrap verified on machine paste)
A4 = ("Section~\\ref{sec:structure} constructs the kernel and states the dichotomy.\n"
"Section~\\ref{sec:prior} situates the object among its nearest neighbors.")
N4 = ("Section~\\ref{sec:structure} constructs the kernel and states the dichotomy.\n"
"Section~\\ref{sec:boundary} characterizes the kernel's analyticity\n"
"boundary: its intrinsic and emergent character, the chiral phase law of\n"
"its cut, the interference relief along the tear, and the log-scale\n"
"calendar of its deep minima. Section~\\ref{sec:floor} states and proves\n"
"the Fourier floor theorem, settles the fate of the calendar in the\n"
"continuum limit, and computes the canonical floors in closed form.\n"
"Section~\\ref{sec:spectroscopy} reads the law backwards into a one-way\n"
"spectroscopy with proven limits.\n"
"Section~\\ref{sec:prior} situates the object among its nearest neighbors.")
edits.append((A4, N4))

# 5. Supplementary sentence
A5 = "certification details, the closed-form derivations, and the simulation"
N5 = ("certification details, the full proof of the floor theorem, the"
" closed-form derivations, and the simulation")
edits.append((A5, N5))

# 6. Discussion perimeter paragraph
A6 = "\\section{Discussion and limitations}\n\\label{sec:discussion}"
N6 = A6 + ("\n\nThe additions of this version call for their own perimeter"
" statement.\nSections~\\ref{sec:boundary}--\\ref{sec:spectroscopy} are"
" structural\ncharacterizations of the kernel as a mathematical object:"
" machine-verified\nsimulation throughout, one elementary hand proof whose"
" ingredients are\nclassical and labelled as such, and closed forms faced"
" against the\nsimulations to their last digits. None of it adds a physical"
" claim. The\nlog-periodic form is classical in the discrete-scale-invariance"
" literature\n(Section~\\ref{sec:dsi}); what we read as potentially new ---"
" the\nhierarchy-free one-way route to it, and the jump-phase witness ---"
" is\nstated with the hedge it deserves, and its arbitration belongs to"
" external\nreview, not to this deposit.")
edits.append((A6, N6))

for a, n in edits:
    assert src.count(a) == 1, f"anchor not unique ({src.count(a)}): {a[:60]!r}"
    src = src.replace(a, n, 1)
open(F, "w", encoding="utf-8").write(src)
print(f"OK: {F} rewritten ({len(src.splitlines())} lines); backup {F}.bak-s5; 6 edits applied")
for k in ["Beyond the protocol", "(iv) the kernel", "(vii) a one-way",
          "machine-faced floor theorem", "reads the law backwards",
          "full proof of the floor theorem", "arbitration belongs to"]:
    print(f"  {k!r}: {src.count(k)}")
