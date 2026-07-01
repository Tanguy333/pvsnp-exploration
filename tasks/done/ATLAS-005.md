# ATLAS-005 — Contrôle positif Δ_w : le gain asymétrique PROUVÉ n'est PAS visible à n ≤ 7 — auto-relativisation des mesures MAJ

- **Type** : V (contrôle d'instrument, zone génératrice 6, ligne 14)
- **Exécutée le** : 2026-06-27
- **Script** : [`checks/task_atlas005_delta_controle.py`](../../checks/task_atlas005_delta_controle.py)
  (+ log bancarisé `checks/atlas005_controle_log.txt`)

## Le principe du contrôle

Notre instrument MILP mesure « pas de gain asymétrique pour MAJ, n ≤ 7 »
(V-001/V-002/ATLAS-003). KV 2024 PROUVENT un gain asymétrique pour les
Δ_w (indicatrice du poids w ; Δ_n = AND). Si l'instrument reproduit ce
gain prouvé → il est validé et le contraste MAJ/Δ_w est réel. S'il ne le
voit pas → les égalités MAJ aux petites tailles ne discriminent rien.

## Résultat : AUCUN gain certifié, nulle part

| n | w testés | d testés | gains asym certifiés |
|---|---|---|---|
| 5 | 5 (=AND), 4, 2 | 1..4 | **aucun** (certifié d ≤ 3 ; d=4 incumbents égaux au sym) |
| 6 | 6 (=AND), 5, 3 | 1..4 | **aucun** (certifié sauf (6,5,3) incumbent égal) |
| 7 | 7 (=AND) | 1..4 | **aucun** (d=1 certifié ; d=2..4 incumbents égaux) |

Toutes les valeurs générales trouvées coïncident avec l'optimum
symétrique. Aucune cellule ne montre eg < es. (Caveat : dans les
cellules « ~ » l'optimalité générale n'est pas certifiée — un gain caché
sous l'incumbent n'y est pas exclu ; mais aucun n'a été TROUVÉ.)

## Conséquence — auto-relativisation (le point important)

**Le gain prouvé par KV n'apparaît pas aux tailles accessibles.** Donc :

1. L'égalité MAJ à n ≤ 7 **perd l'essentiel de sa valeur probante** pour
   la Conjecture 1.5 : à ces tailles, RIEN ne montre de gain — même les
   fonctions où il est prouvé. L'égalité MAJ ne discrimine pas MAJ de Δ_w.
2. La lecture de V-002 (« nos données petites-tailles vont dans le sens
   de la conjecture ») était SUR-INTERPRÉTÉE — recadrée par ce contrôle.
   Les données restent exactes ; leur portée était surestimée.
3. Étendre MAJ à n = 8 (ex-ATLAS-005b) devient PEU INTÉRESSANT tant qu'on
   ne sait pas à partir de quelle taille/régime le gain Δ_w devient
   visible — c'est CE seuil qui calibre la valeur des mesures MAJ.

## Caveats honnêtes

- La séparation de KV a des paramètres précis (régime de w, ε, degré) que
  notre audit n'a pas extraits — notre balayage (ε\* à degré fixé,
  w ∈ {n, n−1, ~n/2}, d ≤ 4) peut viser À CÔTÉ de leur régime. À lire
  dans leur preuve avant de conclure « asymptotique ».
- K_BOUND = 5 et time_limit 120-240 s hérités ; cellules « ~ » non closes.

## Suite (ATLAS-006 candidat)

Extraire du texte KV (TR24-074) les paramètres EXACTS de leur séparation
sym < asym pour Δ_w (quel w, quel ε, quel degré), puis pointer
l'instrument exactement là. C'est une tâche de lecture (type A), zéro
calcul — et c'est elle qui dira si le seuil de visibilité est atteignable.
