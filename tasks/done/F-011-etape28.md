# TÂCHE F-011, étape 28 : certificats minimaux par MaxSAT — ✅ les structures deviennent lisibles

- **Type** : F (canonicalisation)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e28_maxsat_canon.py`](../../checks/task_f011e28_maxsat_canon.py)
  (RC2/WCNF : dures = couverture, souples = 1 par orbite active ;
  vérification par profils)

## Les minima (tous en < 1 s)

| cellule | minimum | lisibilité |
|---|---|---|
| (13, (4,4,5)) | 21 orbites | encore opaque |
| (14, (2,5,7)) | 19 | encore opaque |
| (19, (3,7,9)) | 31 | opaque |
| (20, (4,7,9)) | 38 | opaque |
| **(23, (8,15))** | **11** | **LISIBLE** |
| **(24, (7,17))** | **10** | **LISIBLE** |

## Les deux formes lisibles (t = 12)

**n = 23, P = (8,15)** : u_k = 1 pour **k ∈ [1, 8]** (plage contiguë —
i.e. `U = e₁₂(total) − e₀(A)e₁₂(B)` sur F₂) ; v = trois orbites
seulement : (0,12)→1, (3,9)→1, (8,4)→2.

**n = 24, P = (7,17)** : u = deux orbites {(0,12), (1,11)} ; v_k =
**(1, 2,2,2,2,2,2, 1)** sur k = 0..7 — quasi-constant :
`V = 2·e₁₂(total) − e₀(A)e₁₂(B) − e₇(A)e₅(B) (mod 3)`.

> Le pattern émergent pour t = 12 : **e_t global ± un petit nombre de
> corrections produits aux bouts de la plage des k** — la même grammaire
> que K′ (e_t + correction équilibrée), avec des corrections de bord au
> lieu du centre. Matériau direct pour K″.

## Limite honnête

Les cellules tri/quadripartites (t = 7, 10, 11) restent à 19-38 orbites
même minimisées — leurs formes closes, si elles existent, demandent soit
de meilleures partitions, soit une grammaire plus riche. K″ se lira
d'abord sur les t pairs à bipartitions (12, puis vérifier 14… non — 14
est t=7 impair ; prochains : t = 12 fait, viser t = 15, 18 déjà K′…).

## e29 candidate

Formuler et prouver la construction « e_t + corrections de bord » pour
une nouvelle famille de t (les certificats de t = 12 en gabarit), par
les mêmes lemmes de Lucas que K′.
