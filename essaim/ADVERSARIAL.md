# Points faibles et tests adversariaux à faire ensuite

## Points faibles connus
1. **Centre caché** : le couplage tous-à-tous est mathématiquement un agent central (le champ moyen).
2. **Seuil d'émergence arbitraire** : 5/√N choisi a priori, non calibré sur la distribution réelle de r sous le témoin.
3. **Fenêtre d'observation** : statistiques sur la 2e moitié ; aucun test de stationnarité (dérive lente non exclue).
4. **lockAC et angAC** : moyennes circulaires sur une fenêtre ; un verrouillage intermittent donne une valeur intermédiaire
   ambiguë (zone Δ_C 2.6 à 3.0).
5. **Taille finie** : pas d'étude en N ; l'écart à la théorie près de Kc n'est pas expliqué quantitativement.
6. **Choix de f_i** : (Δ, κ, D) n'est qu'une famille ; « objectif », « exploration », « protection » sont des étiquettes,
   pas des comportements dérivés.
7. **Bruit** : Heun stochastique non validé contre une solution exacte avec bruit (ex. Fokker-Planck, K=0 : diffusion de phase).

## Tests à écrire (vérificateur d'abord)
- A1 Témoin brouillé : permuter aléatoirement les ω entre groupes ; si les métriques de groupe restent identiques, l'effet n'est pas lié aux objectifs.
- A2 Distribution nulle de r : 200 runs K=0 → seuil empirique au quantile 99.9 % au lieu de 5/√N.
- A3 Balayage en N (250, 1000, 4000, 16000) : les régimes oscillants (S1) survivent-ils, ou sont-ils des effets de taille finie ?
- A4 Réseau creux (Erdős-Rényi, petit-monde, anneau) à degré moyen fixé : retrouve-t-on une cohérence sans aucun champ global lu par les agents ?
- A5 Test du bruit : K=0, D>0, vérifier ⟨e^{iΔθ}⟩ = e^{−Dt} (solution exacte de la diffusion de phase).
- A6 Hystérésis : balayer K montant puis descendant ; bistabilité éventuelle (attendue absente pour ω unimodal, présente pour bimodal).
- A7 Mutants supplémentaires : sin → cos, normalisation 1/N oubliée, ψ gelé à t=0 ; chacun doit casser au moins un test V.
- A8 Indépendance d'implémentation : réécrire le noyau sous une autre forme (O(N²) direct, autre intégrateur RK4) et comparer les r tardifs à 1e-3 près.
- A9 Antériorité : Hong & Strogatz 2011 (contrariens), Kuramoto bimodal (Martens et al. 2009), chimères (Abrams & Strogatz 2004) ; lire les sources et écrire la différence exacte. [Références de mémoire, non résolues.]
