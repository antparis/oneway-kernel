#!/usr/bin/env python3
"""Exact symbolic residues for the quarantined cube internal-axis claims.

The script prints expressions and residues only. Interpretation remains human.
"""
import sympy as sp

Juv, Jvu, gu, gv = sp.symbols("Juv Jvu gu gv", nonzero=True)
Juv_p = gu / gv * Juv
Jvu_p = gv / gu * Jvu
cycle2_residue = sp.simplify(Juv_p * Jvu_p - Juv * Jvu)
ratio2_residue = sp.simplify((Juv_p / Jvu_p) - (gu / gv) ** 2 * (Juv / Jvu))

g1, g2, g3, g4 = sp.symbols("g1 g2 g3 g4", nonzero=True)
a, b, c, d = sp.symbols("a b c d", nonzero=True)
W = a * b * c * d
Wp = (g1 / g2 * a) * (g2 / g3 * b) * (g3 / g4 * c) * (g4 / g1 * d)
cycle4_residue = sp.simplify(Wp - W)

ar, br, cr, dr = sp.symbols("ar br cr dr", nonzero=True)
Wrev = ar * br * cr * dr
A = sp.simplify(W / Wrev)
Arev = sp.simplify(Wrev / W)
reverse_ratio_residue = sp.simplify(A * Arev - 1)

s = sp.symbols("s")
j12, j21 = sp.symbols("j12 j21")
L = sp.Matrix([[s, -j12], [-j21, s]])
G = sp.simplify(L.inv())

print("cycle2_product_residue =", cycle2_residue)
print("cycle2_ratio_covariance_residue =", ratio2_residue)
print("cycle4_product_residue =", cycle4_residue)
print("reverse_ratio_product_residue =", reverse_ratio_residue)
print("two_site_resolvent =", G.tolist())
print("two_site_resolvent_denominator =", sp.factor(G[0, 0].as_numer_denom()[1]))
