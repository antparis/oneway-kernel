"""
base.py : livrable 1. Modèle de base, r(t) et distribution des phases.
Usage : python3 base.py [--seed 0] [--N 1000]
Sorties : figures/base_rt.png, figures/base_sweep.png, résumé texte sur stdout.
Chaque valeur imprimée est un résultat de simulation, pas une mesure physique.
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import kuramoto as km

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--N", type=int, default=1000)
ap.add_argument("--dist", default="gauss", choices=["gauss", "lorentz"])
ap.add_argument("--width", type=float, default=1.0)
ap.add_argument("--T", type=float, default=100.0)
ap.add_argument("--dt", type=float, default=0.01)
a = ap.parse_args()

rng = np.random.default_rng(a.seed)
omega = km.natural_frequencies(a.N, a.dist, a.width, rng)       # tirage aléatoire
theta0 = rng.uniform(0, 2 * np.pi, a.N)                          # aucune unité imposée
_, Kc = km.r_infinity_theory(1.0, a.dist, a.width)
print(f"# PARAMS seed={a.seed} N={a.N} dist={a.dist} width={a.width} T={a.T} dt={a.dt} Kc_th={Kc:.4f}")

# --- 1. r(t) pour trois couplages + témoin nul ------------------------------
Ks = [0.0, 0.7 * Kc, 1.3 * Kc, 2.5 * Kc]
snaps_at = [0.0, a.T]
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
finals = {}
for K in Ks:
    res = km.simulate(omega, K, a.T, a.dt, theta0=theta0, rng=np.random.default_rng(a.seed + 1),
                      record_every=10, record_phases_at=snaps_at)
    rl, sl = km.late_stats(res["r"], res["t"])
    finals[K] = (res, rl, sl)
    ax[0].plot(res["t"], res["r"], lw=1, label=f"K={K:.2f} (K/Kc={K/Kc:.1f})")
rnull = finals[0.0][1]
for K in Ks:
    _, rl, sl = finals[K]
    v = km.emergence_verdict(rl, rnull, a.N) if K > 0 else "témoin"
    print(f"K={K:.3f} K/Kc={K/Kc:.2f}  r_tardif={rl:.4f} ± {sl:.4f}  émergence={v}")
ax[0].axhline(1 / np.sqrt(a.N), color="k", ls=":", lw=0.8, label="1/√N")
ax[0].set(xlabel="t", ylabel="r(t)", title=f"r(t), N={a.N}, ω~{a.dist}({a.width}), seed={a.seed}")
ax[0].legend(fontsize=8)
# distribution finale des phases, référentiel tournant (θ - ψ)
for K in Ks[1:]:
    res = finals[K][0]
    rel = np.angle(np.exp(1j * (res["snapshots"][a.T] - res["psi"][-1])))
    ax[1].hist(rel, bins=60, histtype="step", density=True, label=f"K/Kc={K/Kc:.1f}")
ax[1].set(xlabel="θ - ψ (rad)", ylabel="densité", title="phases à t=T, relatives à ψ")
ax[1].legend(fontsize=8)
fig.tight_layout()
fig.savefig("figures/base_rt.png", dpi=130)

# --- 2. balayage r_tardif(K) vs théorie N→∞ --------------------------------
Kgrid = np.linspace(0, 3 * Kc, 25)
rs, ss = [], []
for K in Kgrid:
    res = km.simulate(omega, K, a.T, a.dt, theta0=theta0, rng=np.random.default_rng(a.seed + 1), record_every=10)
    rl, sl = km.late_stats(res["r"], res["t"])
    rs.append(rl); ss.append(sl)
rth, _ = km.r_infinity_theory(Kgrid, a.dist, a.width)
fig, axs = plt.subplots(figsize=(6, 4.2))
axs.errorbar(Kgrid / Kc, rs, yerr=ss, fmt="o", ms=3, label="simulation (moy ± éc.-type, 2e moitié)")
axs.plot(Kgrid / Kc, rth, "-", label="théorie N→∞ (littérature)")
axs.axhline(1 / np.sqrt(a.N), color="k", ls=":", lw=0.8, label="1/√N")
axs.set(xlabel="K / Kc", ylabel="r tardif", title=f"Transition, N={a.N}, seed={a.seed}")
axs.legend(fontsize=8)
fig.tight_layout()
fig.savefig("figures/base_sweep.png", dpi=130)
print("# SWEEP K/Kc, r_sim, std, r_th")
for K, r_, s_, t_ in zip(Kgrid, rs, ss, rth):
    print(f"{K/Kc:.3f} {r_:.4f} {s_:.4f} {t_:.4f}")
