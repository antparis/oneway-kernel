# essaim/ : essaim rythmique auto-cohérent (première passe)

Modèle de Kuramoto avec sous-groupes. Dépendances : `numpy`, `matplotlib` (voir `requirements.txt`).

```
python3 verify.py      # vérificateur (14 tests, tricheurs et mutant), ~30 s
python3 base.py        # livrable 1 : r(t), phases, balayage r(K) ; ~40 s
python3 subgroups.py   # livrable 2 : trois sous-groupes, trois balayages ; ~3 min
```
`NOTE.md` : résultats et limites. `ADVERSARIAL.md` : points faibles et tests suivants.
Les figures et le log dans `figures/` proviennent du bac à sable de l'assistant : statut [HEURISTIQUE] tant que non rejoués.
