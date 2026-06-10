# TÂCHE F-011, étape 20 : décision de la plate à n = 10 — ⚠ NON CONCLU

- **Type** : F (décision exacte — issue : non conclu, documenté)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e20_decide_n10.py`](../../checks/task_f011e20_decide_n10.py)

## La question et les deux attaques

`deg₆(MAJ_10) = 5 ?` (Lemme 5 : à degré 5, support = les 252 monômes de
taille 5 ; 638 ensembles à couvrir par U mod 2 / V mod 3.)

| Attaque | Résultat |
|---|---|
| Recuit **joint** (u, v ensemble, sans ansatz, 240 s) | échec — coût final 27 après **35,5 M d'itérations** |
| ILP exact (CBC : Σu = 2k+U_S, Σv = 3m+V_S, U_S+V_S ≥ 1 ; 420 s) | **timeout**, ni faisable ni infaisable |

## Lecture honnête

- L'étape 19 (ansatz u≡1) calait à 42 ; le recuit joint cale à 27 :
  l'élargissement de l'espace aide peu. Deux heuristiques indépendantes
  qui plafonnent loin de 0 sur 638 contraintes → **soupçon sérieux
  d'infaisabilité** (deg₆(MAJ_10) ≥ 6, plate fausse hors points
  spéciaux) — mais un échec heuristique n'est pas une preuve (q.12).
- Le statut reste **ouvert**. Pour trancher : (i) SAT (encodage XOR
  natif, CryptoMiniSat — dépendance nouvelle), (ii) ILP plus long /
  meilleur solveur, (iii) argument théorique de comptage (sommes de U(S)
  sur les strates : Σ_{|S|=6} U(S) ≡ Σ_T u_T mod 2, identités de design
  à exploiter).

## État de l'hypothèse plate

| n | statut |
|---|---|
| 4..9 | ✅ plate vraie (exhaustif / certificats vérifiés) |
| 16, 32 (t = 2^a) | ✅ plate vraie (Théorème K) |
| **10..13** | ⚠ ouverte — soupçon d'échec à 10 (deux heuristiques calent) |

C'est une frontière de calcul assumée : le dépôt documente l'instance
précise (252 variables ternaires + 252 binaires, 638 contraintes) comme
problème ouvert exécutable.
