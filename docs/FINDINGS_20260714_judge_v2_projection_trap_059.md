# FINDINGS 2026-07-14 — Judge v2 (#059): convention fix + PROJECTION TRAP

Status: [ESTABLISHED machine + judge]. 14/14 exact clauses,
judge_repair_058_v2.py (sha256 cffac21a), Anthony's machine, sandbox-identical.
Supersedes the battery of judge_repair_058.py (#058).

## Why v2 exists (the error, owned)
judge_repair_058.py declared positions as REAL symbols. Its Q-DEC decoy
i(X-Y) had Delta = 0 only in that convention. Under the PAPER's convention
(z, zb, w, wb INDEPENDENT Wirtinger variables) the same kernel has
Delta = i(z - zb - w + wb) != 0: the clause did not transfer to the paper.
Caught by external adversarial audit (GPT-5.6), verified independently.
LESSON (SPARC, encoding axis): a decoy valid in one variable convention can
be false in another. Always judge in the convention the paper uses.
The correct decoy was already graved: Bergman -k*log(1 - z*wb) (P6, #027),
exchange-Hermitian (Delta = 0) and non-reciprocal (R != 0). Certified here.

## Corrections integrated (both audit catches)
1. Q-DEC = Bergman kernel; regression guard J2 exhibits the old decoy as
   false (Delta != 0 shown, not assumed).
2. C1 hypothesis EXPLICIT (J8): complex coefficient alone does NOT force
   Delta != 0; one needs M(g) = g and g != 0. Shown both ways.

## NEW RESULT — the PROJECTION TRAP (J1a/J1b, machine-exact)
The one-way CLOSED FORM is a function of x = zb*wb alone. The product
commutes: S(zb*wb) = wb*zb = zb*wb, so the scalar closed form is
EXCHANGE-SYMMETRIC and R = 0 ON IT. Reading R off the closed form yields a
FALSE "reciprocal" verdict on the paper's central object.
Non-reciprocity lives ONLY on the complete two-point kernel: the transfer
matrix with the REVERSE element vanishing (G21 = f(zb*wb), G12 = 0), where
R = [[0, f], [-f, 0]] != 0 and Delta != 0 (both invariants violated, as
#055 states -- but only on this object).
This REALIZES the projection-blindness law (diag(R) == 0, J6) on the
paper's own central object: the scalar closed form IS a projection.
CONSEQUENCE for any deposit: the paper must state explicitly ON WHICH
OBJECT R is evaluated, or a reader computes R on the closed form, finds 0,
and wrongly concludes the one-way kernel is reciprocal.

## State of the paper versions
v3 sealed, untouched. v4 BLOCKED (false decoy inherited + 14 residual
debt passages found by external audit; never deposited). v5 pending: wide
patch (14 passages, corrected decoy, printed quadrant table, object-of-R
clause, separable scope of W, K_eps named, singular-continuous gap open).

Traces: judge_repair_058_v2.py (sha256 cffac21a), IDEAS_REGISTRY.md #059.
