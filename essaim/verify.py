"""
verify.py : vérificateur écrit AVANT les expériences.
Chaque test imprime PASS/FAIL ; code de sortie 1 si un test échoue.
Tolérances fixées a priori (avant tout run de ce fichier).
Inclut des tricheurs (unité imposée par la condition initiale) et un
mutant (signe du couplage inversé) qui DOIVENT être rejetés.
"""
import sys
import numpy as np
import kuramoto as km

FAILS = []


def check(name, ok, info=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {info}")
    if not ok:
        FAILS.append(name)


rng = np.random.default_rng(12345)

# V1 identité O(N²) == O(N)
th = rng.uniform(0, 2 * np.pi, 500)
err = np.max(np.abs(km.coupling_direct(th, 1.7) - km.coupling_meanfield(th, 1.7)))
check("V1 identité couplage direct = champ moyen", err < 1e-12, f"max|Δ|={err:.2e}")

# V2 K=0, D=0 : solution exacte θ0 + ω t
N = 200
om = km.natural_frequencies(N, "gauss", 1.0, rng)
th0 = rng.uniform(0, 2 * np.pi, N)
res = km.simulate(om, 0.0, T=10, dt=0.01, theta0=th0, rng=rng)
err = np.max(np.abs(res["theta"] - (th0 + om * 10)))
check("V2 K=0 solution exacte", err < 1e-9, f"max|Δ|={err:.2e}")

# V3 ω identiques, K>0 : synchronisation complète
res = km.simulate(np.zeros(N), 1.0, T=60, dt=0.02, rng=rng)
check("V3 ω identiques → r→1", res["r"][-1] > 1 - 1e-6, f"r_final={res['r'][-1]:.8f}")

# V4 convergence en dt (Heun déterministe, ordre 2 attendu : ratio ≈ 4)
om = km.natural_frequencies(N, "gauss", 1.0, quantile=True)
th0 = rng.uniform(0, 2 * np.pi, N)
fin = {}
for dt in (0.04, 0.02, 0.01, 0.005):
    fin[dt] = km.simulate(om, 2.5, T=20, dt=dt, theta0=th0, rng=rng)["theta"]
e1 = np.max(np.abs(fin[0.04] - fin[0.005]))
e2 = np.max(np.abs(fin[0.02] - fin[0.005]))
e3 = np.max(np.abs(fin[0.01] - fin[0.005]))
check("V4 convergence dt (ordre ≥ 1.5)", e2 < e1 and np.log2(e1 / e2) > 1.5,
      f"err(0.04)={e1:.2e} err(0.02)={e2:.2e} err(0.01)={e3:.2e} ordre≈{np.log2(e1/e2):.2f}")

# V5 Lorentz, quantiles, comparaison à r∞ = sqrt(1-2γ/K)   (tol a priori 0.03)
N = 4000
gam = 0.5
om = km.natural_frequencies(N, "lorentz", gam, quantile=True)
for K in (1.5, 2.0, 3.0):
    res = km.simulate(om, K, T=80, dt=0.01, rng=rng, record_every=10)
    rl, sl = km.late_stats(res["r"], res["t"])
    rt = km.r_infinity_theory(K, "lorentz", gam)[0][0]
    check(f"V5 Lorentz γ={gam} K={K}", abs(rl - rt) < 0.03, f"r_sim={rl:.4f}±{sl:.4f} r_th={rt:.4f}")

# V6 Gauss σ=1, quantiles
om = km.natural_frequencies(N, "gauss", 1.0, quantile=True)
for K in (2.0, 3.0):
    res = km.simulate(om, K, T=80, dt=0.01, rng=rng, record_every=10)
    rl, sl = km.late_stats(res["r"], res["t"])
    rt = km.r_infinity_theory(K, "gauss", 1.0)[0][0]
    check(f"V6 Gauss σ=1 K={K}", abs(rl - rt) < 0.03, f"r_sim={rl:.4f}±{sl:.4f} r_th={rt:.4f}")

# V7 sous-critique : r tardif de l'ordre de 1/sqrt(N)
Kc = km.r_infinity_theory(1.0, "gauss", 1.0)[1]
res = km.simulate(om, 0.5 * Kc, T=80, dt=0.01, rng=rng, record_every=10)
rl, _ = km.late_stats(res["r"], res["t"])
check("V7 K=Kc/2 → incohérent", rl < 5 / np.sqrt(N), f"r_sim={rl:.4f}  5/√N={5/np.sqrt(N):.4f}")

# T1 TRICHEUR : unité imposée par θ0 (toutes phases nulles), ω identiques, K=0.
# r reste 1 sans aucun couplage. Le critère doit refuser d'y voir une émergence.
N = 500
th0 = np.zeros(N)
cpl = km.simulate(np.zeros(N), 1.0, T=20, dt=0.02, theta0=th0)
nul = km.simulate(np.zeros(N), 0.0, T=20, dt=0.02, theta0=th0)
v = km.emergence_verdict(km.late_stats(cpl["r"], cpl["t"])[0], km.late_stats(nul["r"], nul["t"])[0], N)
check("T1 tricheur θ0 alignées rejeté", v is False, f"verdict={v}")

# T2 TRICHEUR : θ0 alignées, ω dispersées, K sous-critique : r(0)=1 puis décroît.
# Une lecture naïve de r(0) ou du max de r(t) conclurait à l'unité.
om = km.natural_frequencies(N, "gauss", 1.0, quantile=True)
cpl = km.simulate(om, 0.5 * Kc, T=80, dt=0.02, theta0=np.zeros(N))
nul = km.simulate(om, 0.0, T=80, dt=0.02, theta0=np.zeros(N))
rc = km.late_stats(cpl["r"], cpl["t"])[0]
rn = km.late_stats(nul["r"], nul["t"])[0]
v = km.emergence_verdict(rc, rn, N)
check("T2 tricheur r(0)=1 sous-critique rejeté", v is False and cpl["r"].max() > 0.99,
      f"max r={cpl['r'].max():.3f} r_tardif={rc:.3f} r_nul={rn:.3f} verdict={v}")

# T3 contrôle positif : le critère doit accepter un vrai cas supercritique
cpl = km.simulate(om, 3.0, T=80, dt=0.02, rng=np.random.default_rng(1))
nul = km.simulate(om, 0.0, T=80, dt=0.02, rng=np.random.default_rng(1))
v = km.emergence_verdict(km.late_stats(cpl["r"], cpl["t"])[0], km.late_stats(nul["r"], nul["t"])[0], N)
check("T3 contrôle positif K=3 accepté", v is True, f"verdict={v}")

# M1 MUTANT : signe du couplage inversé ; doit échouer la comparaison V5.
N = 4000
om = km.natural_frequencies(N, "lorentz", gam, quantile=True)
res = km.simulate(om, -3.0, T=80, dt=0.01, rng=rng, record_every=10)
rl, _ = km.late_stats(res["r"], res["t"])
rt = km.r_infinity_theory(3.0, "lorentz", gam)[0][0]
check("M1 mutant K→-K détecté par V5", abs(rl - rt) >= 0.03, f"r_mutant={rl:.4f} r_th={rt:.4f}")

print("\nRÉSUMÉ :", "TOUT PASSE" if not FAILS else f"ÉCHECS = {FAILS}")
sys.exit(1 if FAILS else 0)
