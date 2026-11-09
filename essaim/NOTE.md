# Essaim rythmique : note de première passe (2026-11-09)

Statut global : **[HEURISTIQUE]**. Tous les chiffres ci-dessous sortent du bac à sable
de l'assistant (NumPy, Python 3, graines fixées). Ils ne valent rien tant qu'ils ne sont
pas rejoués sur la machine de l'auteur (`python3 verify.py && python3 base.py && python3 subgroups.py`).
Ils certifient au mieux une simulation, jamais un phénomène réel.

## 1. Modèle exact simulé

dθ_i = [ω_i + Δ_g + κ_g K r sin(ψ − θ_i)] dt + √(2D_g) dW_i,  r e^{iψ} = (1/N) Σ e^{iθ_j}.

- La forme `K r sin(ψ−θ_i)` est **identique** à `(K/N) Σ sin(θ_j−θ_i)` (testé, V1, écart 1.7e-16).
- Conséquence non cosmétique : en couplage tous-à-tous, chaque agent lit exactement
  le champ moyen global. « Sans centre ni observateur » n'est donc **pas** réalisé par
  ce modèle : le champ moyen joue le rôle d'un centre virtuel. Seule une version à
  réseau creux (extension 2, non faite) testerait l'hypothèse « sans centre ».
- f_i(s) est réalisé par trois paramètres de groupe (Δ, κ, D), choix de modélisation
  et non dérivation. D'autres choix donneraient d'autres résultats.
- Intégrateur Heun stochastique, dt = 0.01, phases initiales uniformes aléatoires
  (aucune unité imposée au départ).

## 2. Vérificateur (écrit avant les expériences, `verify.py`, 14/14 PASS dans le bac à sable)

| test | contenu | résultat bac à sable |
|---|---|---|
| V1 | couplage O(N²) = O(N) | 1.7e-16 |
| V2 | K=0 : solution exacte | 6.9e-13 |
| V3 | ω identiques → r→1 | r=1.00000000 |
| V4 | convergence en dt | ordre observé ≈ 3.6 (≥ 1.5 exigé) |
| V5 | Lorentz γ=0.5, quantiles, N=4000 vs √(1−2γ/K) | écarts ≤ 0.0003 (tol. 0.03) |
| V6 | Gauss σ=1 vs auto-cohérence | écarts ≤ 0.0001 |
| V7 | K = Kc/2 → r ≈ O(1/√N) | 0.022 < 0.079 |
| T1, T2 | tricheurs : unité imposée par θ0 alignées | rejetés |
| T3 | contrôle positif K=3 | accepté |
| M1 | mutant K → −K | détecté |

Critère d'émergence fixé a priori : r_tardif(couplé) > r_tardif(témoin K=0, mêmes ω, θ0, bruit) + 5/√N,
sur la 2e moitié du run. Il exclut l'unité « héritée » de la condition initiale (T1, T2).

Les formules théoriques (K_c = 2γ et r = √(1−K_c/K) pour Lorentz ; K_c = 2/(πg(0)) pour Gauss)
viennent de la littérature Kuramoto (Kuramoto 1975/1984 ; revue Strogatz, Physica D 2000 ;
Ott & Antonsen, Chaos 2008). **[LIMITE : citations de mémoire, non vérifiées dans la session.]**
Leur accord avec la simulation est ici un test du code, pas une découverte.

## 3. Résultats observés (bac à sable, [HEURISTIQUE])

**Base (N=1000, ω ~ N(0,1), graine 0, `base.py`).**
- K/Kc = 0.7 : r_tardif = 0.056, verdict « pas d'émergence ».
- K/Kc = 1.3 : r_tardif = 0.717 ± 0.011 ; K/Kc = 2.5 : 0.962, verdict « émergence ».
- La courbe r(K) suit la théorie N→∞ au-dessus de ~1.5 Kc ; près de Kc la simulation
  est en dessous (0.44 contre 0.56 à 1.125 Kc), effet de taille finie et de tirage
  aléatoire des ω, attendu mais non quantifié ici.
- Réponse à « r élevé et stable sans forçage ? » : **oui dans ce modèle**, au-dessus de Kc,
  ce qui est le résultat classique de Kuramoto, pas un résultat nouveau.

**Trois sous-groupes (N=600, K=3, σ=0.5, 3 graines, `subgroups.py`, log dans `figures/subgroups_log.txt`).**
- S1, décalage Δ_C du groupe C : C reste verrouillé à A avec un retard de phase qui croît
  (−0.18 rad à Δ_C=0.5, −1.15 à 2.5). Entre Δ_C ≈ 2.6 et 3.0, le verrouillage se dégrade
  (lockAC 0.998 → 0.94) ; au-delà, C décroche, r global tombe à ≈ 0.62 et **oscille**
  (écart-type temporel 0.06 à 0.13, figure en bas au centre). C'est le seul régime vu
  où la cohérence globale « apparaît puis se perd » de façon répétée. Mécanisme
  (glissements de phase, battement entre deux amas) non démontré : **[CONJECTURE]**.
- S2, réceptivité κ_C : κ_C=0 laisse C incohérent (r_C = 0.059 ≈ 1/√200). κ_C < 0 (contrarien) :
  A et C sont verrouillés en quasi anti-phase (|ψ_A−ψ_C| entre 2.95 et 3.08 rad, toutes graines),
  r global chute (0.33 à κ_C=−0.5 ; 0.10 à κ_C=−1 avec 0/3 verdict d'émergence) alors que
  chaque groupe garde une cohérence interne (r_A ≈ 0.34 à 0.81). Un état analogue (« état π »)
  est décrit pour le modèle conformistes-contrariens de Hong & Strogatz (PRL 2011)
  **[LIMITE : non vérifié dans la session]** ; à considérer comme [REDÉCOUVERTE] probable.
- S3, bruit des explorateurs D_B : r_B décroît de 0.99 à 0.36 pour D_B de 0 à 3, A et C
  restent à ≈ 0.98, r global décroît continûment (0.985 → 0.767). Pas de transition vue dans cette plage.

**Réponse à « des sous-groupes coexistent-ils dans un motif global ? »** : oui, deux formes
observées (amas décalés en phase verrouillés ; amas en anti-phase). Point clé : **r global
seul ne voit pas cette structure** (r=0.10 avec trois groupes internes cohérents à κ_C=−1).
Toute affirmation d'« unité » doit donc s'appuyer sur les r par groupe et les verrouillages,
pas sur r global.

## 4. Limites

1. Tous-à-tous = centre virtuel (cf. §1). Le cœur philosophique du projet n'est pas encore testé.
2. Une seule valeur de K, de σ, de N pour les sous-groupes ; 3 graines seulement.
3. Fenêtre finie (T=100 à 120) : « stable » veut dire stable sur la 2e moitié du run, rien de plus.
4. Les groupes sont étiquetés par construction ; l'émergence de groupes non étiquetés n'est pas étudiée.
5. Aucun résultat ici n'est apparemment neuf : tout relève de la littérature Kuramoto classique
   (à confirmer par une recherche d'antériorité réelle).
