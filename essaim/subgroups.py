"""
subgroups.py : livrable 2. Trois sous-essaims aux « objectifs » différents.

Réalisation EXPLICITE de f_i(s) (choix de modélisation, discutable) :
  A « exploite »   : Δ_A = 0,   κ_A = 1,   D_A = 0
  B « explore »    : Δ_B = 0,   κ_B = 1,   D_B = bruit de phase
  C « se protège » : Δ_C = décalage de fréquence, κ_C = réceptivité (κ<0 : contrarien)
Couplage tous-à-tous : chaque agent reçoit le champ moyen GLOBAL, aucun
couplage préférentiel intra-groupe.

Trois balayages, chacun sur plusieurs graines :
  S1 : Δ_C ∈ [0, 4]   (κ_C=1, D_B=0.2)   diversité des objectifs-fréquences
  S2 : κ_C ∈ [-1, 1]  (Δ_C=0, D_B=0.2)   réceptivité, jusqu'au contrarien
  S3 : D_B ∈ [0, 3]   (Δ_C=0, κ_C=1)     bruit des explorateurs
Mesures sur la 2e moitié : r global, r_A, r_B, r_C, écart-type temporel de r
(indicateur de cohérence qui apparaît et se perd), |<e^{i(ψ_A-ψ_C)}>| et
l'angle moyen ψ_A-ψ_C (verrouillage inter-groupes).
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import kuramoto as km

ap = argparse.ArgumentParser()
ap.add_argument("--N", type=int, default=600)
ap.add_argument("--K", type=float, default=3.0)
ap.add_argument("--sigma", type=float, default=0.5)
ap.add_argument("--seeds", type=int, default=3)
ap.add_argument("--T", type=float, default=120.0)
ap.add_argument("--dt", type=float, default=0.01)
a = ap.parse_args()
N, K = a.N, a.K
G = np.repeat([0, 1, 2], N // 3)
N = G.size
print(f"# PARAMS N={N} K={K} sigma={a.sigma} seeds={a.seeds} T={a.T} dt={a.dt}")


def run(seed, dC=0.0, kC=1.0, DB=0.2, keep=False):
    rng = np.random.default_rng(seed)
    om = km.natural_frequencies(N, "gauss", a.sigma, rng) + np.where(G == 2, dC, 0.0)
    kap = np.where(G == 2, kC, 1.0)
    D = np.where(G == 1, DB, 0.0)
    th0 = rng.uniform(0, 2 * np.pi, N)
    res = km.simulate(om, K, a.T, a.dt, theta0=th0, kappa=kap, D=D, rng=rng, record_every=10)
    nul = km.simulate(om, 0.0, a.T, a.dt, theta0=th0, kappa=kap, D=D,
                      rng=np.random.default_rng(seed), record_every=10)
    t = res["t"]; m = t >= t[-1] / 2
    Zg = [km.order_parameter(res["thetas"][:, G == g]) for g in range(3)]
    out = dict(r=res["r"][m].mean(), r_std=res["r"][m].std(),
               rA=np.abs(Zg[0][m]).mean(), rB=np.abs(Zg[1][m]).mean(), rC=np.abs(Zg[2][m]).mean(),
               lockAC=np.abs(np.mean(np.exp(1j * (np.angle(Zg[0][m]) - np.angle(Zg[2][m]))))),
               angAC=np.angle(np.mean(np.exp(1j * (np.angle(Zg[0][m]) - np.angle(Zg[2][m]))))),
               r_null=nul["r"][m].mean())
    out["emerg"] = km.emergence_verdict(out["r"], out["r_null"], N)
    if keep:
        out.update(t=t, rt=res["r"], Zg=Zg, theta=res["theta"], psi=res["psi"][-1])
    return out


KEYS = ["r", "r_std", "rA", "rB", "rC", "lockAC", "angAC", "r_null"]


def sweep(name, param, values, **fixed):
    rows = []
    print(f"\n# {name}: {param} | " + " ".join(f"{k}(moy±ét)" for k in KEYS) + " | émergence(n/seeds)")
    for v in values:
        outs = [run(s, **{param: v}, **fixed) for s in range(a.seeds)]
        agg = {k: (np.mean([o[k] for o in outs]), np.std([o[k] for o in outs])) for k in KEYS}
        ne = sum(o["emerg"] for o in outs)
        rows.append((v, agg))
        print(f"{v:6.3f} | " + " ".join(f"{agg[k][0]:.3f}±{agg[k][1]:.3f}" for k in KEYS) + f" | {ne}/{a.seeds}")
    return rows


S1 = sweep("S1", "dC", np.linspace(0, 4, 9), kC=1.0, DB=0.2)
S2 = sweep("S2", "kC", np.linspace(-1, 1, 9), dC=0.0, DB=0.2)
S3 = sweep("S3", "DB", np.linspace(0, 3, 7), dC=0.0, kC=1.0)

fig, axs = plt.subplots(2, 3, figsize=(15, 8))
for ax, rows, lab in zip(axs[0], (S1, S2, S3), ("Δ_C", "κ_C", "D_B")):
    x = [r[0] for r in rows]
    for k, sty in (("r", "k-o"), ("rA", "C0--"), ("rB", "C1--"), ("rC", "C2--"), ("lockAC", "C3:"), ("r_std", "C7-.")):
        ax.errorbar(x, [r[1][k][0] for r in rows], yerr=[r[1][k][1] for r in rows], fmt=sty, ms=3, label=k)
    ax.set(xlabel=lab, ylim=(-0.02, 1.02), title=f"balayage {lab} (K={K}, σ={a.sigma}, {a.seeds} graines)")
axs[0, 0].legend(fontsize=7)
# exemples de séries temporelles
for ax, kw, ttl in zip(axs[1], (dict(dC=0.0), dict(dC=3.0), dict(kC=-1.0)),
                       ("référence Δ_C=0", "Δ_C=3 (C décroche)", "κ_C=-1 (contrarien)")):
    o = run(0, keep=True, **kw)
    ax.plot(o["t"], o["rt"], "k", lw=1, label="r global")
    for g, c in zip(range(3), ("C0", "C1", "C2")):
        ax.plot(o["t"], np.abs(o["Zg"][g]), c, lw=0.8, label="ABC"[g])
    ax.set(xlabel="t", ylim=(0, 1.02), title=ttl)
axs[1, 0].legend(fontsize=7)
fig.tight_layout()
fig.savefig("figures/subgroups.png", dpi=130)
