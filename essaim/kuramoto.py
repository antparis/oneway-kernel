"""
kuramoto.py : noyau minimal d'un essaim d'oscillateurs de phase couplés.

Modèle (temps continu) :
    dθ_i = [ ω_i + κ_g(i) · K · r · sin(ψ - θ_i) ] dt + sqrt(2 D_g(i)) dW_i
avec  r e^{iψ} = (1/N) Σ_j e^{iθ_j}.

Identité utilisée (exacte, vérifiée dans verify.py) :
    (K/N) Σ_j sin(θ_j - θ_i) = K · r · sin(ψ - θ_i)
Le coût passe donc de O(N²) à O(N) sans approximation.

Le terme f_i(s) du cahier des charges est réalisé ici par trois paramètres
par sous-groupe g, tous explicites :
    Δ_g : décalage de fréquence naturelle (biais d'objectif),
    κ_g : réceptivité au couplage (κ=1 conformiste, 0<κ<1 « se protège »,
          κ<0 contrarien),
    D_g : intensité de bruit de phase (« explore »).
Aucun de ces termes ne contient ψ seul : l'unique canal vers le collectif
est le couplage de Kuramoto lui-même.

Intégrateur : Heun stochastique (ordre 2 en dt pour la partie déterministe,
ordre fort 1 pour un bruit additif). Avec D=0 c'est Heun déterministe.
Version discrète : step="euler" donne l'application itérée
    θ ← θ + dt·(ω + κ K r sin(ψ-θ)) + bruit.
"""
from __future__ import annotations

import numpy as np


def order_parameter(theta: np.ndarray) -> complex:
    """Retourne Z = r e^{iψ} = moyenne de e^{iθ}. Accepte (N,) ou (..., N)."""
    return np.exp(1j * theta).mean(axis=-1)


def coupling_direct(theta: np.ndarray, K: float) -> np.ndarray:
    """Somme O(N²) littérale : (K/N) Σ_j sin(θ_j - θ_i). Sert de référence."""
    d = theta[None, :] - theta[:, None]
    return K * np.sin(d).mean(axis=1)


def coupling_meanfield(theta: np.ndarray, K: float) -> np.ndarray:
    """Forme O(N) : K r sin(ψ - θ_i) = K Im(Z e^{-iθ_i})."""
    Z = order_parameter(theta)
    return K * np.imag(Z * np.exp(-1j * theta))


def _norm_ppf(q):
    """Quantile de la loi normale standard par bissection sur erf (NumPy seul,
    précision ~1e-14). Évite la dépendance à SciPy."""
    from math import erf, sqrt
    erfv = np.vectorize(erf)
    lo = np.full_like(q, -40.0)
    hi = np.full_like(q, 40.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        below = 0.5 * (1 + erfv(mid / sqrt(2))) < q
        lo = np.where(below, mid, lo)
        hi = np.where(below, hi, mid)
    return 0.5 * (lo + hi)


def natural_frequencies(N, dist="gauss", width=1.0, rng=None, quantile=False):
    """
    Fréquences naturelles centrées en 0.
      dist="gauss"  : écart-type `width`
      dist="lorentz": demi-largeur `width` (γ)
    quantile=True : tirage déterministe par quantiles (q_j=(j-1/2)/N),
    supprime le bruit d'échantillonnage (utile pour comparer à la théorie).
    """
    if quantile:
        q = (np.arange(N) + 0.5) / N
    else:
        rng = rng if rng is not None else np.random.default_rng()
        q = rng.random(N)
    if dist == "gauss":
        if not quantile:
            return width * rng.standard_normal(N)
        return width * _norm_ppf(q)
    if dist == "lorentz":
        return width * np.tan(np.pi * (q - 0.5))
    raise ValueError(dist)


def simulate(omega, K, T, dt, theta0=None, kappa=None, D=None,
             rng=None, step="heun", record_every=1, record_phases_at=None):
    """
    Intègre le modèle. Retourne un dict :
      t        : instants enregistrés
      r, psi   : paramètre d'ordre global
      Z_groups : (si `groups` fourni via kappa/D tableaux) non calculé ici
      theta    : phases finales (non repliées)
      snapshots: {t: θ mod 2π} pour les instants demandés
    kappa, D : scalaires ou tableaux (N,) ; défaut κ=1, D=0.
    """
    rng = rng if rng is not None else np.random.default_rng()
    N = omega.size
    kappa = np.ones(N) if kappa is None else np.broadcast_to(kappa, (N,)).astype(float)
    D = np.zeros(N) if D is None else np.broadcast_to(D, (N,)).astype(float)
    theta = rng.uniform(0, 2 * np.pi, N) if theta0 is None else np.array(theta0, float)
    sig = np.sqrt(2 * D * dt)
    noisy = np.any(D > 0)

    def drift(th):
        return omega + kappa * coupling_meanfield(th, K)

    nsteps = int(round(T / dt))
    rec_idx = np.arange(0, nsteps + 1, record_every)
    Zs = np.empty(rec_idx.size, complex)
    thetas_rec = []  # phases complètes aux instants enregistrés (pour sous-groupes)
    snaps = {}
    want = set() if record_phases_at is None else {int(round(s / dt)) for s in record_phases_at}
    k_rec = 0
    for n in range(nsteps + 1):
        if n % record_every == 0:
            Zs[k_rec] = order_parameter(theta)
            thetas_rec.append(theta.copy())
            k_rec += 1
        if n in want:
            snaps[n * dt] = np.mod(theta, 2 * np.pi)
        if n == nsteps:
            break
        xi = sig * rng.standard_normal(N) if noisy else 0.0
        f0 = drift(theta)
        if step == "euler":
            theta = theta + dt * f0 + xi
        elif step == "heun":
            pred = theta + dt * f0 + xi
            theta = theta + 0.5 * dt * (f0 + drift(pred)) + xi
        else:
            raise ValueError(step)
    return dict(t=rec_idx * dt, r=np.abs(Zs), psi=np.angle(Zs), Z=Zs,
                theta=theta, thetas=np.array(thetas_rec), snapshots=snaps)


def r_infinity_theory(K, dist, width):
    """
    Branche partiellement synchronisée stationnaire, limite N→∞ (littérature,
    voir NOTE.md, citation [LIMITE : non vérifiée dans la session]) :
      Lorentz : K_c = 2γ,  r = sqrt(1 - K_c/K)  (exact)
      Gauss   : K_c = 2/(π g(0)) = σ sqrt(8/π) ; r obtenu ici en résolvant
                numériquement l'auto-cohérence r = K r ∫ cos²φ g(K r sinφ) dφ.
    """
    K = np.atleast_1d(np.asarray(K, float))
    out = np.zeros_like(K)
    if dist == "lorentz":
        Kc = 2 * width
        m = K > Kc
        out[m] = np.sqrt(1 - Kc / K[m])
        return out, Kc
    if dist == "gauss":
        s = width
        Kc = s * np.sqrt(8 / np.pi)
        phi = np.linspace(-np.pi / 2, np.pi / 2, 4001)
        g = lambda w: np.exp(-w ** 2 / (2 * s ** 2)) / (s * np.sqrt(2 * np.pi))

        def F(r, k):  # F(r)=0 <=> auto-cohérence, r>0
            return k * np.trapezoid(np.cos(phi) ** 2 * g(k * r * np.sin(phi)), phi) - 1

        for i, k in enumerate(K):
            if k <= Kc:
                continue
            lo, hi = 1e-12, 1.0
            for _ in range(80):  # bissection
                mid = 0.5 * (lo + hi)
                if F(mid, k) > 0:
                    lo = mid
                else:
                    hi = mid
            out[i] = 0.5 * (lo + hi)
        return out, Kc
    raise ValueError(dist)


# ---------------------------------------------------------------------------
# Critère d'émergence (fixé AVANT les expériences, cf. verify.py)
# ---------------------------------------------------------------------------
def late_stats(r, t, frac=0.5):
    """Moyenne et écart-type de r sur la dernière fraction `frac` du temps."""
    m = t >= t[-1] * (1 - frac)
    return float(r[m].mean()), float(r[m].std())


def emergence_verdict(r_cpl, r_null, N, margin_sigma=5.0):
    """
    Une cohérence est dite « émergente par couplage » ssi
      (a) r_tardif(couplé) > r_tardif(nul) + margin_sigma / sqrt(N),
      (b) le run nul (K=0, MÊMES ω, MÊMES θ0, MÊME bruit) sert de témoin.
    1/sqrt(N) est l'échelle des fluctuations de r pour des phases
    indépendantes uniformes. Le critère ne dit rien de la stabilité au-delà
    de la fenêtre simulée.
    """
    return bool(r_cpl > r_null + margin_sigma / np.sqrt(N))
