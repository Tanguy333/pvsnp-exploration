# TOUR 27 — Dossier de cible pour le Proposeur (ouvert le 2026-07-24)

> Suite directe du Tour 26 (SURVIT) et de ses prolongements T26-S1/S2.
> Dossier AUTONOME, à donner tel quel au Proposeur. Le trou est
> UNIQUE : c'est le dernier saut avoué de la proposition du Tour 26,
> les deux autres ayant été comblés depuis (6 points exhaustifs +
> théorème isotypique ∀k).

## 1. LA CIBLE (unique, non négociable) : décomposable ⇒ global

**Prouver que les monômes croisés n'aident pas :**

> Pour f = MAJ_k^t(OR2^k) (k blocs OR2 disjoints, seuil 2 ≤ t ≤ k−1) :
> **W(f) = W_dec(f)** — tout séparateur général (monômes croisés
> autorisés) pèse au moins autant que le meilleur séparateur
> décomposable (monômes intra-blocs seulement). Une preuve pour tout
> k, ou même pour k = 5 seul, est recevable.

OU BIEN (tout aussi recevable, et VIVANTE — la fenêtre est ouverte) :

> **Réfuter** : exhiber un séparateur global de MAJ₅(OR2⁵) (n = 10,
> t = 3) de poids **< 30**, coefficients explicites — vérifiable par
> énumération des 1024 points en une seconde. La fenêtre actuelle est
> W(MAJ₅(OR2⁵)) ∈ [20, 30] : un témoin à 29 ou moins tue la cible et
> révèle un mécanisme croisé neuf.

## 2. LE MODÈLE (définition complète — aucune variante acceptée)

W(f) = min Σ_S a_S sur p(z) = Σ_S a_S·m_S(z), coefficients ENTIERS
a_S ≥ 0, monômes positifs non vides, ensembles de valeurs
{p : f=1} et {p : f=0} DISJOINTS. Décomposable = tout S est inclus
dans un seul bloc. f = [# blocs i avec x_i ∨ y_i ≥ t].

## 3. CE QUI EST ACQUIS (ne pas relabourer)

- **T26-S1 (exhaustif)** : W_dec(MAJ_k(OR2^k)) = k(k+1) pour
  k = 3..8 (12, 20, 30, 42, 56, 72) — recherche exhaustive par DP
  (m, s), élagage partiel sain, approfondissement itératif.
- **T26-S2 (THÉORÈME, tout k)** : dans la sous-classe isotypique,
  M ≥ k+1 donc W ≥ k(k+1), pour 2 ≤ t ≤ k−1 — preuve par restriction
  {a, M} + 3 cas. Borne exacte (témoin mod-k).
- **U26.1 (Tour 26)** : W(SYM_k(g^k)) ≤ k·Σ(ĝ_S mod k) — donc
  W(MAJ_k(OR2^k)) ≤ k(k+1) TOUJOURS : la cible « preuve » équivaut à
  W = k(k+1) exactement.
- **Égalité global = décomposable CERTIFIÉE à k = 3 et 4** :
  optima globaux 12 et 20 (CP-SAT OPTIMAL, re-vérifiés).
- **k = 3 : un optimum global CROISÉ existe** (les 12 paires
  croisées, F-021) À ÉGALITÉ avec le décomposable — les croisés
  peuvent ÉGALER ; la cible dit qu'ils ne peuvent pas GAGNER.
- **L26.5 (restriction, prouvé)** : W(f) ≥ W(f|bloc:=0) et
  ≥ W(f|bloc:=1) — l'outil qui a donné W(MAJ₅) ≥ W(THR₂(OR2⁴)) = 20.
- Théorème de tranche (F-013), lemme du comptage (F-018), borne
  d'alternance (F-020, aveugle sur monotone — ne pas la proposer).

## 4. CE QUI EST CONNU SUR LE TROU (état exact)

- MAJ₅(OR2⁵) global : incumbent 30 (mod-5), borne inf CP-SAT directe
  7 seulement (n = 10 hors de portée du solveur) ; borne inf PROUVÉE
  20 (restriction). Un run symétrisé de 25 min n'a pas trouvé < 30.
- Le pattern q.12 du dépôt (« vrai aux petits k, faux après ») joue
  DANS LES DEUX SENS ici : l'égalité k = 3, 4 peut casser à k = 5,
  ou tenir pour une raison structurelle à découvrir.
- Piste structurelle offerte (à prendre ou laisser) : à k = 4,
  l'optimum global EST décomposable (mod-4) ; à k = 3, l'optimum
  croisé (paires) et le décomposable (mod-3) coexistent à 12 — toute
  preuve devra expliquer cette coexistence ; toute réfutation devra
  exploiter un mécanisme que les paires croisées seules ne donnent
  pas (le couvert unilatéral croisé pèse C(k,t)·2^t ≫ k(k+1) dès
  k = 5 : 80 > 30 — le croisé naïf est PIRE, il faut un hybride).

## 5. CONDITIONS DE RECEVABILITÉ (anti-esquive, gelées — leçon du Tour 26 : elles produisent de bonnes propositions)

1. **Citer ce dossier** et le trou unique — aucune autre cible.
2. **Calculs livrés AVANT soumission**, exécutés : toute construction
   en coefficients explicites + vérification par énumération ; toute
   affirmation sur k ≤ 5 confrontée aux certificats existants.
3. **Le(s) saut(s) logique(s) restant(s) listés explicitement.**
4. Pas de pivot ; échec honnête recevable.
5. Honnêteté épistémique standard (prouvé / mesuré / conjecturé).

## 6. Ce que la clôture donnerait (portée honnête)

- Sens « preuve » : W(MAJ_k(OR2^k)) = k(k+1) inconditionnel pour
  k ≤ 8 (avec S1) et, avec S2, la chaîne complète pour tout k
  modulo le seul trou résiduel isotypique → décomposable général
  (k ≥ 9) — l'écho jouet du mur TC⁰ serait un théorème Θ(k²) à un
  epsilon près.
- Sens « réfutation » : un mécanisme croisé inconnu du zoo, et la
  chute de l'écho jouet sous k(k+1) — réorientation majeure du fil.
- Dans les deux cas : le Réfuteur vérifiera tout (énumération,
  certificats, contre-attaques CP-SAT symétrisées).
