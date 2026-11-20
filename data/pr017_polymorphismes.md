# PR-017 — Polymorphismes de Siggers et d'Olšák : témoin exécutable de l'entrée E-7 (réplication déclarée + mesure)

Date : 2026-11-21. Instrument : `checks/pr017_polymorphismes.py`
(implémentation INDÉPENDANTE : encodage one-hot de f : A^m → B,
contraintes de polymorphisme par tuple interdit, identités par égalité
des vecteurs one-hot, CaDiCaL 1.9.5 via pysat ; tout témoin SAT
re-vérifié par simulation). Durée totale < 3 s.

## 1. Contrôle — Siggers 4-aire (Schaefer 1978, Hell-Nešetřil 1990 ; Siggers 2010, Kearnes-Marković-McKenzie 2014)

| gabarit | Sig | attendu | clauses |
|---|---|---|---|
| 2-SAT | OUI | P | 380 |
| Horn-3 | OUI | P | 4 860 |
| XOR-3 | OUI | P | 2 104 |
| Z₃-lin | OUI | P | 354 762 |
| K₂ | OUI | P | 88 |
| 1-in-3 | NON | NP-complet | 461 |
| NAE-3 | NON | NP-complet | 2 648 |
| 3-SAT | NON | NP-complet | 19 264 |
| K₃ | NON | NP-complet | 4 356 |

9/9 conformes (le nombre de clauses de Z₃-lin coïncide avec celui de la
candidature).

## 2. Régime de frontière — Olšák K₃⁶ → K_c

| c | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| Ols | NON | NON | NON | **OUI** | OUI |
| variables | 2 187 | 2 916 | 3 645 | 4 374 | 5 103 |

Reproduit à l'identique. Le seuil c* = 6 coïncide avec la frontière de
dureté connue (PCSP(K₃, K₅) NP-dur, BBKO 2021). **Portée : aucune
démontrée.** Pour un PCSP, l'existence d'un polymorphisme d'Olšák ne
donne pas d'algorithme (pas de caractérisation de la traitabilité par
une seule condition de mineur), et son absence n'est pas un critère de
dureté que l'instruction puisse citer. Valeur [NON TROUVÉE] dans la
littérature consultée — mesure.

## Réserves

Réplication déclarée pour le contrôle ; seuil c* = 6 non revendiqué.
