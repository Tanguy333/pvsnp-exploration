# TÂCHE F-011, étape 29 : formes closes t = 12 ✅ + conjecture 3-lisse ❌

- **Type** : F (théorème fini + test de conjecture — issue mixte)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e29_smooth.py`](../../checks/task_f011e29_smooth.py)

## [1] Les formes closes de t = 12 — ÉTABLIES

Vérifiées (identités de Vandermonde + couverture, tous profils) :

**n = 24, P = (7,17)** :
`U = C(b,12) + a·C(b,11) (mod 2)` ;
`V = 2·C(w,12) − C(b,12) − C(a,7)·C(b,5) (mod 3)`.

**n = 23, P = (8,15)** :
`U = C(w,12) − C(b,12) (mod 2)` ;
`V = C(b,12) + C(a,3)·C(b,9) + 2·C(a,8)·C(b,4) (mod 3)`.

Premières **mosaïques de Lucas mixtes** établies — les morceaux morts de
e₁₂ mod 3 (w ∈ [18,20]) sont couverts par des fenêtres mod 2 en b, et
réciproquement.

## [2] La conjecture 3-lisse — RÉFUTÉE par t = 5

| t | 3-lisse ? | observé | verdict |
|---|---|---|---|
| 3, 4, 6, 8, 9, 12 | oui | solubles | ✓ |
| 7, 10, 11, 13 | non | insolubles | ✓ |
| **5** | **non** | **soluble (bipartition (5,5))** | **✗ CONTRE-EXEMPLE** |

**6e conjecture du dépôt tuée le jour de sa formulation.** La loi de la
solvabilité bipartite à n = 2t est plus fine : aucun invariant base-3
simple ne sépare encore {2,3,4,5,6,8,9,12} de {7,10,11,13}. Plus de
données nécessaires (t = 14..20, e30 candidate) avant de re-conjecturer.

## État du fil

Plate confirmée n = 4..24 + 32 ; 2 familles infinies prouvées (K, K′) ;
formes closes finies pour t = 12 ; la **loi de solvabilité bipartite**
est la nouvelle question structurée (données : 12 points, 1 frontière
inexpliquée à t = 5 vs 7).
