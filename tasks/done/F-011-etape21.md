# TÂCHE F-011, étape 21 : la plate par SAT — ✅ n = 10, 11 tranchés ; ⚠ n = 12, 13 = frontière de calcul

- **Type** : F (décision par SAT — issue mixte, documentée)
- **Exécutée le** : 2026-06-11/12
- **Scripts** : [`task_f011e21_sat_n10.py`](../../checks/task_f011e21_sat_n10.py),
  [`e21b_split`](../../checks/task_f011e21b_split.py),
  [`e21c_cms`](../../checks/task_f011e21c_cms.py) ;
  outil ajouté : [`tools/cryptominisat5.exe`](../../tools/cryptominisat5.exe)
  (binaire officiel v5.14.5, clauses XOR natives + élimination gaussienne)

## Résultats

| n | t | verdict | temps | certificat |
|---|---|---|---|---|
| 10 | 5 | **SAT — deg₆ = 5, plate confirmée** | ~1 s (CaDiCaL) | vérifié 1024 points |
| 11 | 6 | **SAT — deg₆ = 6, plate confirmée** | ~1 s (CaDiCaL) | vérifié 2048 points |
| 12 | 6 | **INDÉCIS** | CaDiCaL 36+45 min, CMS+Gauss 20 min | — |
| 13 | 7 | **INDÉCIS** | CaDiCaL ~13 min, CMS+Gauss 20 min | — |

L'instance ouverte de l'étape 20 (n = 10, où recuit et ILP avaient
échoué) est **close en 1 seconde par le bon outil** — leçon de méthode.

## État de l'hypothèse plate

Confirmée : n = 4..11, 16, 32 (exhaustif/SAT/Théorème K). **Indécise** :
n = 12, 13 — et la résistance est *structurée* :

- **n = 12** : le cas pair avec w = 12 = 2t et C(12,6) ≡ 0 mod 6 — le
  poids de type anomalie. Soupçon d'UNSAT (la plate serait réfutée là).
- **n = 13** : C(w,7) est **pair sur tout [8,13]** — le gabarit mod 2 ne
  couvre presque rien, le mod 3 porte tout. **La dureté SAT suit la
  couverture mod 2 du gabarit, pas la parité de n** (ma prédiction
  « impair = facile » est réfutée — consignée).

## Incidents consignés

1. Prédiction « n = 13 facile » fausse (cf. ci-dessus).
2. Le garde-fou `solver.interrupt()` de pysat/CaDiCaL **n'a pas
   fonctionné** (45 min au lieu de 20 — détecté par l'utilisateur) ;
   le garde-fou `--maxtime` de CryptoMiniSat, lui, a fonctionné.
3. Escalade d'outils documentée : recuit → ILP → CaDiCaL → CMS+Gauss —
   chaque outil a son domaine ; n = 12, 13 résistent à tous sous ~1 h.

## Options pour trancher n = 12, 13 (futur)

1. **Cassage de symétrie** — le vrai levier : l'instance a la symétrie
   S_n complète (toute permutation des variables préserve les solutions),
   poison connu des solveurs surtout pour UNSAT. BreakID ou contraintes
   lex partielles sur les orbites.
2. Budgets multi-heures (nuit) avec CMS.
3. Théorie : un argument d'infaisabilité ciblé à n = 12 (le mécanisme
   d'anomalie C(12,6) ≡ 0 dans le modèle général).
