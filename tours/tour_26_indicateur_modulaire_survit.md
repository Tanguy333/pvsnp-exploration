# TOUR 26 — L'indicateur modulaire : **SURVIT** (premier tour survivant de l'histoire du dépôt)

- **Date** : 2026-07-23. Proposeur : Qwen. Réfuteur : Claude.
- **Cible** (dossier [`tour_26_cible.md`](tour_26_cible.md)) : borne inf
  super-additive W(MAJ_k(g^k)) ≥ ω(k) pour bloc monotone non-AND, ou
  réfutation constructive.
- **Scripts du Proposeur** : `checks/tour_26_proposeur_modind.py`,
  `checks/tour_26_proposeur_cpsat.py` — livrés AVANT soumission,
  ré-exécutés par le Réfuteur.

## 1. Reformulation (une phrase)

Pour g monotone, le polynôme q_M = Σ_S (ĝ_S mod M)·m_S (Möbius réduit)
est un indicateur EXACT modulo M qui s'annule sur g⁻¹(0) ; sommer
q_k sur les blocs compte les blocs satisfaits modulo k (le couple
(0,k) étant tranché par magnitude), d'où W(SYM_k(g^k)) ≤ k·Σ(ĝ_S mod k)
= O_g(k²) universel — et la difficulté archimédienne de T2 (pas
d'indicateur exact sur ℤ) disparaît en arithmétique modulaire, ne
laissant comme coût que la résolution du compte (M ≥ k).

## 2. Audit du Réfuteur — TOUT CE QUI EST VÉRIFIÉ

**Preuves relues ligne à ligne (toutes correctes)** : L26.0
(annulation — Möbius d'un monotone supporté sur les implicants) ;
U26.1 dans ses DEUX variantes (M = k+1, poids k(k+2) ; M = k, poids
k(k+1) avec l'argument de magnitude pour (0,k)) ; L26.5(a)(b)
(restriction — le terme constant translate uniformément, la
disjonction survit) ; la chaîne de restrictions (k,t) → (4,2) valide
pour tout k ≥ 5.

**Constructions ré-exécutées** : 13/13 [OK] par énumération exhaustive
(k ≤ 7, n ≤ 14), y compris le témoin négatif (la parité seule meurt à
k = 5, collision {3,4,6} — pourquoi M ≥ k est nécessaire).

**Certificats CP-SAT reproduits indépendamment** :
- MAJ₃(OR2³) = 12 OPTIMAL ✓ ;
- décomposables k = 3, 4, 5 : **12, 20, 30 tous OPTIMAUX** ✓ (k = 5
  confirmé en 650 s après un premier run trop court — loi k(k+1)
  exacte dans la classe décomposable sur 3 points) ;
- **THR₂(OR2⁴) = 20 OPTIMAL global** (36 s, re-vérifié — et l'optimum
  EST la forme mod-4 (1,1,3) : les croisés n'aident pas à k = 4) ;
- séparateur mod-4 poids 20 pour THR₃(OR2⁴) : re-vérifié par
  énumération (ones {3,4,...,20} / zeros {0,1,2,5,6,10}) →
  W(THR₃(OR2⁴)) ∈ [18, 20] (le 18 = lb du run 900 s du Proposeur ;
  mon run 600 s atteint 14 — cohérent, non contradictoire).

**Le corollaire central TIENT** :
> **W(MAJ₅(OR2⁵)) ≥ W(THR₂(OR2⁴)) = 20 > 10 = 5·W(OR2)** —
> L26.5(b) (prouvé) + certificat 20 (reproduit). Le point de
> prédiction du dossier est livré au DOUBLE du seuil (c = 2).
> Encadrement final : W(MAJ₅(OR2⁵)) ∈ [20, 30].

**Contre-attaque du Réfuteur sur C26** : run global symétrisé
(cassage par ordre des masses de blocs, cap 30, hint mod-5, 1500 s) —
**30 non battu** (incumbent 30, lb 10). La conjecture k(k+1) résiste
à une attaque sérieuse ; elle reste conjecture (2 points certifiés
k = 3, 4 ; pattern q.12 dûment signalé par le Proposeur lui-même).

## 3. Attaque logique — ce qui reste ouvert (les 3 sauts, tous avoués)

1. **Décomposable ⇒ global à k ≥ 5** : égalité certifiée seulement à
   k = 3, 4. LE pas manquant.
2. **Borne inf décomposable générale** (k(k+1) pour tout k) : prouvée
   par certificats finis k ≤ 5 seulement ; la machinerie d'évitement
   par bloc n'est pas fermée pour les moduli mixtes.
3. **La croissance ω(k)** : les bornes prouvées sont des planchers
   constants (≥ 20 pour k ≥ 5), pas une croissance. La cible
   asymptotique stricto sensu reste ouverte — dit en toutes lettres
   par le Proposeur (« échec honnête » au sens 6.4 revendiqué
   d'avance).

Défauts mineurs consignés : incohérence de présentation M = k vs
M = k+1 entre texte et script (cosmétique, les deux prouvées) ;
XOR₅(OR2⁵) ≤ 35 sous-optimal (le mod-5 donne 30) ; le lb 18 de THR₃
n'est pas reproduit par le Réfuteur (14 à budget moindre — plausible,
non certifié ici).

## 4. Barrières et antériorité

Sans objet direct (modèle fini) — conditions d'honnêteté honorées.
Antériorité correctement signalée par le Proposeur : l'esprit
modulus-amplifying est Toda/Yao/Beigel-Tarui (bib/ ligne 7) ; le
lemme d'annulation dans CE modèle, le choix M = k, l'unification et
les valeurs sont propres au tour. Le Réfuteur confirme l'unification :
ANF = Möbius mod 2, donc la construction parité de F-016 EST q₂, et
l'hybride C(s,2) de F-022 EST q₂(MAJ3) — le zoo avait une échelle.

## 5. VERDICT : **SURVIT**

Premier tour survivant en 26 tours. Acquis pour le dépôt :
- **U26.1 (théorème, 5e mécanisme)** : l'échelle modulaire unifie le
  zoo et borne l'écho jouet du mur TC⁰ à O(k²) universel — toute
  réponse à la cible vit dans [Ω(k), O(k²)].
- **Premier point super-additif PROUVÉ** : W(MAJ₅(OR2⁵)) ≥ 20 = 2·k·W(g).
- Fenêtres resserrées : MAJ₅(OR2⁵) ∈ [20, 30] ; MAJ₃(MAJ3³) ∈ [4, 12]
  (le mod-3 bat le couvert 27 de F-021) ; THR₃(OR2⁴) ∈ [18, 20].
- Leçon d'échelle : restriction + petit point exact ≫ attaque directe
  (20 contre 7 de borne par le solveur à n = 10).

**Sous-lemme prioritaire à tester (la suite du fil)** : prouver la
borne inf décomposable W_dec(MAJ_k(OR2^k)) ≥ k(k+1) pour tout k —
c'est un système fini d'évitement de valeurs par bloc, bien posé,
et sa preuve donnerait Ω(k²) DANS LA CLASSE décomposable : la moitié
inférieure de l'écho jouet, à un pas (décomposable ⇒ global) de la
cible entière.
