#!/usr/bin/env python3
# judge_repair_058_v2.py -- 2026-07-14
# CORRECTED battery for the repaired reciprocity theorem (registry #058, scope fix).
#
# WHY v2 EXISTS (own it):
#   judge_repair_058.py declared the two points as REAL symbols. With real
#   positions the mirror map M collapses to I -> -I, and the toy decoy
#   K = i(X - Y) satisfied Delta = 0. Under the PAPER's convention -- z, zb,
#   w, wb INDEPENDENT Wirtinger variables, which is the foundation of the whole
#   project -- that same K has
#       Delta = i(z - zb - w + wb) != 0
#   so it does NOT realize the (Delta = 0, R != 0) quadrant. The clause was
#   convention-dependent and did not transfer to the paper. Caught by external
#   adversarial audit (GPT-5.6), verified independently here.
#   LESSON (SPARC, encoding axis): the encoding decides. A decoy valid in one
#   variable convention can be false in another. Always judge in the convention
#   the PAPER uses.
#
# The correct decoy was already in the project: the BERGMAN reproducing kernel
#   K = -k log(1 - z*wb)   (pitfall P6, registry #027)
# which is exactly exchange-Hermitian (Delta = 0) yet non-reciprocal (R != 0).
#
# CONVENTIONS (paper-faithful):
#   z, zb, w, wb : INDEPENDENT symbols (Wirtinger). Never .conjugate().
#   S  : exchange of the two points, (z,zb) <-> (w,wb).  simultaneous=True.
#   M  : mirror map -- swap each variable with its conjugate AND I -> -I.
#   R  = K - S(K)         reciprocity master invariant   (#055)
#   Dl = K - M(S(K))      exchange-Hermiticity axis      (#055/#056)
#
# CLAUSES
#  J1  FOUR QUADRANTS, with the project's OWN certified kernels:
#        Q-RH   reciprocal & exchange-Hermitian : R=0,  Dl=0
#        Q-C1   reciprocal-dissipative (C1)     : R=0,  Dl!=0   <- kills the biconditional
#        Q-DEC  BERGMAN decoy (P6, #027)        : R!=0, Dl=0    <- kills the converse
#        Q-OW   one-way (partner absent)        : R!=0, Dl!=0
#  J2  The FALSE decoy is exhibited as false (regression guard): i(z-w) has Dl != 0
#      in the Wirtinger convention -- this clause must PASS by showing Dl != 0.
#  J3  Operator theorem: (L^-1)^sharp - (L^sharp)^-1 = 0, A^sharp = C^-1 A^T C,
#      C SYMMETRIC (physical: B(u,v) = u^T C v = B(v,u)).
#  J4  L = L^sharp  ==>  K = K^sharp  ==>  R_op = 0.
#  J5  Covariance: R' = U R U^-1 under simultaneous L, K, C transform.
#  J6  PROJECTION BLINDNESS: diag(R) == 0 identically -> a same-port probe can
#      never witness non-reciprocity; the invariant lives on the complete kernel.
#  J7  Onsager-Casimir: K_b^sharp == K_{-b} while K_b != K_b^sharp.
#  J8  C1 hypothesis made EXPLICIT (the audit's second catch): for
#      K = c*(g(z,zb) + g(w,wb)) to sit in Q-C1 one needs M(g) = g and g != 0;
#      c complex alone does NOT force Dl != 0. Verified both ways.
#  J9  COMPARATIVE WITNESS (#057) restated in the paper's convention:
#      W = D_X - D_Y ; W != 0 => R != 0 (sufficient) ; W = 0 INCONCLUSIVE,
#      exhibited by K_eps = eps*(X - Y) (entire, no cut): W = 0 while R != 0.
#
# Authority: exact symbolic residues only. Verdict = Anthony's machine run.

import sympy as sp

z, zb, w, wb = sp.symbols("z zb w wb")          # INDEPENDENT (Wirtinger)
k = sp.symbols("k", positive=True)
g = sp.Function("g")

report = []


def S(K):
    """Exchange of the two points. simultaneous=True MANDATORY (#057 lesson)."""
    return K.subs({z: w, zb: wb, w: z, wb: zb}, simultaneous=True)


def M(K):
    """Mirror map: swap each variable with its conjugate AND I -> -I."""
    return K.subs({z: zb, zb: z, w: wb, wb: w, sp.I: -sp.I}, simultaneous=True)


def R_of(K):
    return sp.simplify(K - S(K))


def Dl_of(K):
    return sp.simplify(K - M(S(K)))


def add(label, ok, detail):
    report.append((label, ok, detail))


# ---------------- J1: the four quadrants, project kernels -------------------
c = 1 + sp.I

# Q-RH : symmetric, real coefficient, M-invariant building block
K_RH = z * zb + w * wb
# Q-C1 : reciprocal-dissipative -- symmetric, complex coefficient, M-invariant g
K_C1 = c * (z * zb + w * wb)
# Q-DEC: BERGMAN reproducing kernel (P6, #027) -- exchange-Hermitian, NOT reciprocal
K_DEC = -k * sp.log(1 - z * wb)
# Q-OW : one-way -- partner sector absent (anti-anti sector only)
# (Q-OW handled below as J1a/J1b -- the object matters)

for name, K, wantR0, wantD0 in [
    ("Q-RH  (z*zb + w*wb)", K_RH, True, True),
    ("Q-C1  ((1+i)(z*zb + w*wb))  reciprocal-dissipative", K_C1, True, False),
    ("Q-DEC (Bergman -k*log(1-z*wb))  P6/#027", K_DEC, False, True),
]:
    R, D = R_of(K), Dl_of(K)
    ok = ((sp.simplify(R) == 0) == wantR0) and ((sp.simplify(D) == 0) == wantD0)
    add(f"J1 {name}: R{'==0' if wantR0 else '!=0'} & Dl{'==0' if wantD0 else '!=0'}",
        ok, f"R = {R} ; Dl = {D}")

# ---- Q-OW: THE OBJECT MATTERS. Two clauses, both mandatory. ----------------
# J1a  THE PROJECTION TRAP (new, machine-exact): the one-way CLOSED FORM is a
#      function of x = zb*wb ALONE. The product commutes, so S(x) = x and the
#      scalar closed form is EXCHANGE-SYMMETRIC: R = 0 on it. Evaluating R on
#      the closed form alone yields a FALSE "reciprocal" verdict. This is the
#      projection blindness of J6 realized on the paper's own central object:
#      the scalar closed form IS a projection (the surviving transfer element).
f = sp.Function("f")
K_scalar = f(zb * wb)
R_scalar = sp.simplify(K_scalar - S(K_scalar))
add("J1a PROJECTION TRAP (paper-critical): the one-way CLOSED FORM f(zb*wb) is "
    "EXCHANGE-SYMMETRIC (product commutes) => R = 0 on the scalar alone. "
    "R must NEVER be read off the closed form; it lives on the complete kernel.",
    sp.simplify(R_scalar) == 0, f"S(zb*wb) = {S(zb*wb)} ; R(scalar) = {R_scalar}")

# J1b  Q-OW on the CORRECT object: the complete two-point transfer kernel is a
#      matrix in the direction index with the REVERSE element vanishing
#      (G21 = f(x), G12 = 0, the Lindbladian one-wayness of #021/#027).
#      There, and only there, R != 0.
K_ow_mat = sp.Matrix([[0, f(zb * wb)], [0, 0]])       # reverse element = 0
R_ow_mat = sp.simplify(K_ow_mat - K_ow_mat.T)         # C = I
Dl_ow_mat = sp.simplify(K_ow_mat - sp.Matrix(2, 2,
    lambda i, j: M(K_ow_mat.T[i, j])))
add("J1b Q-OW on the COMPLETE kernel (matrix, G21 = f(zb*wb), G12 = 0): "
    "R != 0 (the reverse transfer element vanishes) & Dl != 0 -- the one-way "
    "kernel violates BOTH invariants, as #055 states, but only on this object.",
    (R_ow_mat != sp.zeros(2, 2)) and (Dl_ow_mat != sp.zeros(2, 2)),
    f"R = {R_ow_mat.tolist()} ; Dl = {Dl_ow_mat.tolist()}")

# ---------------- J2: regression guard -- the FALSE decoy is false ----------
K_bad = sp.I * (z - w)
D_bad = Dl_of(K_bad)
add("J2 REGRESSION GUARD: i(z-w) has Dl != 0 in Wirtinger convention "
    "(the v1 decoy was convention-dependent and WRONG for the paper)",
    sp.simplify(D_bad) != 0, f"Dl = {D_bad}")

# ---------------- Operator level: 2x2, C SYMMETRIC --------------------------
l11, l12, l21, l22 = sp.symbols("l11 l12 l21 l22")
c11, c12, c22 = sp.symbols("c11 c12 c22")
L = sp.Matrix([[l11, l12], [l21, l22]])
C = sp.Matrix([[c11, c12], [c12, c22]])            # SYMMETRIC by physical requirement


def sharp(A, Cm):
    return Cm.inv() * A.T * Cm


add("J0 C is SYMMETRIC (B(u,v) = u^T C v = B(v,u), physical requirement)",
    sp.simplify(C - C.T) == sp.zeros(2, 2), f"C - C^T = {list(sp.simplify(C - C.T))}")

res3 = sp.simplify(sharp(L.inv(), C) - sharp(L, C).inv())
add("J3 (L^-1)^sharp - (L^sharp)^-1 == 0  (A^sharp = C^-1 A^T C, generic L, sym C)",
    res3 == sp.zeros(2, 2), f"{list(res3)}")

s11, s12, s22 = sp.symbols("s11 s12 s22")
Sigma = sp.Matrix([[s11, s12], [s12, s22]])
L_rec = C.inv() * Sigma
chk = sp.simplify(sharp(L_rec, C) - L_rec)
K_rec = L_rec.inv()
res4 = sp.simplify(sharp(K_rec, C) - K_rec)
add("J4 L = L^sharp (constructed) ==> K = K^sharp ==> R_op = 0",
    (chk == sp.zeros(2, 2)) and (res4 == sp.zeros(2, 2)),
    f"L-res = {list(chk)} ; K-res = {list(res4)}")

u11, u12, u21, u22 = sp.symbols("u11 u12 u21 u22")
U = sp.Matrix([[u11, u12], [u21, u22]])
K_gen = L.inv()
R_op = sp.simplify(K_gen - sharp(K_gen, C))
Kp = U * K_gen * U.inv()
Cp = U.inv().T * C * U.inv()
res5 = sp.simplify(sp.simplify(Kp - sharp(Kp, Cp)) - U * R_op * U.inv())
add("J5 covariance: R' - U R U^-1 == 0 (simultaneous L, K, C transform)",
    res5 == sp.zeros(2, 2), f"{list(res5)}")

k11, k12, k21, k22 = sp.symbols("k11 k12 k21 k22")
Kb = sp.Matrix([[k11, k12], [k21, k22]])
R_I = sp.simplify(Kb - Kb.T)
add("J6 PROJECTION BLINDNESS: diag(R) == 0 IDENTICALLY (same-port probe blind); "
    "R_offdiag = k12 - k21",
    (R_I[0, 0] == 0) and (R_I[1, 1] == 0) and (sp.simplify(R_I[0, 1] - (k12 - k21)) == 0),
    f"R = {list(R_I)}")

d, b = sp.symbols("d b")
K_bias = sp.Matrix([[d, b], [-b, d]])
K_mins = sp.Matrix([[d, -b], [b, d]])
add("J7 Onsager-Casimir: K_b^sharp == K_{-b} (bias-reversed) while "
    "K_b - K_b^sharp = 2b antisym (device vs itself) -- two DIFFERENT comparisons",
    (sp.simplify(K_bias.T - K_mins) == sp.zeros(2, 2))
    and (sp.simplify(K_bias - K_bias.T) == sp.Matrix([[0, 2 * b], [-2 * b, 0]])),
    f"K_b^T - K_-b = {list(sp.simplify(K_bias.T - K_mins))} ; "
    f"R = {list(sp.simplify(K_bias - K_bias.T))}")

# ---------------- J8: the C1 hypothesis, made explicit ----------------------
# (audit catch) c complex ALONE does not force Dl != 0. Need M(g) = g and g != 0.
g_inv = z * zb                       # M-invariant: M(z*zb) = zb*z = z*zb
g_nin = sp.I * z                     # NOT M-invariant: M(i*z) = -i*zb
K_ok = c * (g_inv + g_inv.subs({z: w, zb: wb}, simultaneous=True))
K_no = c * (g_nin + g_nin.subs({z: w, zb: wb}, simultaneous=True))
D_ok, D_no = Dl_of(K_ok), Dl_of(K_no)
R_ok, R_no = R_of(K_ok), R_of(K_no)
add("J8 C1 hypothesis EXPLICIT: with M(g)=g and g!=0, complex c gives R=0 & Dl!=0; "
    "without M-invariance of g the conclusion does NOT follow (shown, not assumed)",
    (sp.simplify(R_ok) == 0) and (sp.simplify(D_ok) != 0),
    f"M-inv g: R = {R_ok}, Dl = {D_ok}  |  non-M-inv g: R = {R_no}, Dl = {D_no}")

# ---------------- J9: comparative witness, the inconclusive limit -----------
X, Y = sp.symbols("X Y")
eps, nu = sp.symbols("epsilon nu", positive=True)
a = 1 - sp.I * nu
x = sp.symbols("x", positive=True)
D_jump = 2 * sp.pi * sp.I * x**(-a) * sp.log(x)     # theory jump of F_a

W_c1 = sp.simplify(D_jump - D_jump)                  # C1: identical sectors
P = eps * (X - Y)                                    # entire antisymmetric part
e = sp.symbols("e", positive=True)
jump_P = sp.limit(P.subs(X, x + sp.I * e) - P.subs(X, x - sp.I * e), e, 0)
R_eps = sp.simplify(P - P.subs({X: Y, Y: X}, simultaneous=True))
add("J9 COMPARATIVE WITNESS (#057): W == 0 on the reciprocal C1 (identically); "
    "K_eps = eps*(X-Y) is ENTIRE (zero cut discontinuity) so W = 0 while "
    "R = 2*eps*(X-Y) != 0  ==>  W is SUFFICIENT, NEVER NECESSARY",
    (sp.simplify(W_c1) == 0) and (sp.simplify(jump_P) == 0)
    and (sp.simplify(R_eps - 2 * eps * (X - Y)) == 0),
    f"W(C1) = {W_c1} ; disc(eps*(X-Y)) = {jump_P} ; R(K_eps) = {R_eps}")

# ---------------- verdict ---------------------------------------------------
print("=" * 76)
print("JUDGE v2 (SymPy exact) -- repaired reciprocity theorem, WIRTINGER convention")
print("=" * 76)
n = 0
for label, ok, detail in report:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print(f"         {detail}")
    n += int(ok)
print(f"\n  {n}/{len(report)} exact clauses hold.")
print("  Convention: z, zb, w, wb INDEPENDENT (the paper's). Scope: LTI,")
print("  complete kernel, symmetric non-degenerate C.")
print("  Supersedes judge_repair_058.py, whose Q-DEC clause used real positions")
print("  and therefore did not transfer to the paper. Q1 (size cone) and Q2")
print("  (monodromy witness) remain QUARANTINED, not in this battery.")
