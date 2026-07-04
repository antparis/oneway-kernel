"""make_figures.py -- publication figures for the one-way kernel paper.

Imports protocol_time_domain_sim.py UNCHANGED (no modification of certified
code) and renders two publication-grade figures from its deterministic model:

  fig1_secular_envelope.(pdf|png)
      Revival comb |E(t)| for the Jordan (one-way, defective) ladder vs the
      diagonalizable control, with the secular envelope ~ t exp(-kappa t / 2)
      anchored on the fitted peaks. Fitted exponent p printed in the legend.

  fig2_mirror_deletion.(pdf|png)
      One-way vs reciprocal impulse response. Main revival positions
      (phi + 2 pi k)/delta and mirrored positions (2 pi - phi + 2 pi k)/delta
      marked: the reciprocal field shows the twin comb, the one-way field does
      not -- the mirror-deletion law read directly in the time domain.

Status: figures illustrate the MODEL of protocol_time_domain_sim.py
([HEURISTIQUE sandbox] until executed on Anthony's machine). Deterministic:
fixed seeds, no randomness in the noiseless panels.

Run from oneway-kernel/code/:   python3 make_figures.py
Output:                         ../paper/figures/
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import protocol_time_domain_sim as sim

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "paper", "figures")
os.makedirs(OUTDIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.0,
    "legend.frameon": False,
    "figure.dpi": 120,
    "savefig.dpi": 300,
})

DLT, KAP, PHI = sim.DLT, sim.KAP, sim.PHI
t = np.linspace(1e-3, sim.TMAX, sim.NT)

E_j = sim.field_oneway(t, jordan=True)
E_d = sim.field_oneway(t, jordan=False)
E_r = sim.field_reciprocal(t)

# ---------------------------------------------------------------- figure 1
pk = sim.find_revival_peaks(t, E_j)
p_hat, p_sig, kap_hat = sim.fit_p(pk)

# envelope C * t * exp(-kap t/2), C anchored on the first fitted peak
C = pk[0, 1] / (pk[0, 0] * np.exp(-KAP * pk[0, 0] / 2))
tenv = np.linspace(pk[0, 0] * 0.5, t[-1], 400)
env = C * tenv * np.exp(-KAP * tenv / 2)

fig, ax = plt.subplots(figsize=(5.4, 3.4))
ax.semilogy(t, np.abs(E_j) / pk[0, 1], color="C0",
            label="one-way Jordan ladder")
ax.semilogy(t, np.abs(E_d) / pk[0, 1], color="C1", alpha=0.55,
            label="diagonalizable control")
ax.semilogy(tenv, env / pk[0, 1], "k--", lw=1.2,
            label=(r"envelope $t\,e^{-\kappa t/2}$"
                   f"  (fit $p={p_hat:.3f}\\pm{p_sig:.3f}$)"))
ax.semilogy(pk[:, 0], pk[:, 1] / pk[0, 1], "kv", ms=5, zorder=5,
            label="revival peaks")
ax.set_xlabel(r"time $t$  [units of $1/\delta$]")
ax.set_ylabel(r"$|E(t)|$  (normalized to first revival)")
ax.set_xlim(0, t[-1])
ax.set_ylim(1e-4, 6)
ax.legend(loc="lower center", ncol=2, fontsize=7.5,
          bbox_to_anchor=(0.5, 0.0), borderaxespad=0.4)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(OUTDIR, f"fig1_secular_envelope.{ext}"))
plt.close(fig)

# ---------------------------------------------------------------- figure 2
mr_j = sim.mirror_energy_ratio(t, E_j) if hasattr(sim, "mirror_energy_ratio") else None
mr_r = sim.mirror_energy_ratio(t, E_r) if hasattr(sim, "mirror_energy_ratio") else None

norm_j = np.abs(E_j).max()
norm_r = np.abs(E_r).max()

fig, axes = plt.subplots(2, 1, figsize=(5.4, 4.2), sharex=True)
for ax, E, nrm, name, mr in (
        (axes[0], E_j, norm_j, "one-way", mr_j),
        (axes[1], E_r, norm_r, "reciprocal", mr_r)):
    ax.plot(t, np.abs(E) / nrm, color="C0" if name == "one-way" else "C3",
            lw=0.9)
    for k in range(8):
        tk = (PHI + 2 * np.pi * k) / DLT
        tm = (2 * np.pi - PHI + 2 * np.pi * k) / DLT
        if tk < t[-1]:
            ax.axvline(tk, color="0.55", lw=0.7, ls=":", zorder=0)
        if tm < t[-1]:
            ax.axvline(tm, color="C3", lw=0.7, ls="--", alpha=0.6, zorder=0)
    label = name
    if mr is not None:
        label += f"   (mirror/main energy = {mr:.1e})"
    ax.text(0.015, 0.86, label, transform=ax.transAxes, fontsize=9)
    ax.set_ylabel(r"$|E(t)|$ (norm.)")
    ax.set_ylim(0, 1.1)
axes[1].set_xlabel(r"time $t$  [units of $1/\delta$]")
axes[0].set_title(r"main positions $(\phi+2\pi k)/\delta$ (dotted)  vs  "
                  r"mirror $(2\pi-\phi+2\pi k)/\delta$ (dashed)",
                  fontsize=8.5)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(OUTDIR, f"fig2_mirror_deletion.{ext}"))
plt.close(fig)

print("=" * 70)
print("make_figures.py -- done. Deterministic model figures written to:")
print("  " + os.path.abspath(OUTDIR))
print(f"  fig1: Jordan fit p = {p_hat:.4f} +- {p_sig:.4f} "
      f"(expect 1), kappa_hat = {kap_hat:.4f} (true {KAP})")
if mr_j is not None:
    print(f"  fig2: mirror/main energy -- one-way = {mr_j:.3e}, "
          f"reciprocal = {mr_r:.3f}")
print("Status: model illustration; machine execution = the arbiter.")
print("=" * 70)
