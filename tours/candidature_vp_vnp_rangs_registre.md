# Candidature n° 10 (prompt v4.4, 2026-11-20) : « La voie algébrique par mesures de rang (VP vs VNP) » (présentée comme entrée de registre E-6) — instruction du Réfuteur (PR-015)

**Verdict : ENTRE AU REGISTRE (E-6).** Le quadruplet est rempli
honnêtement et sa pièce porteuse est confirmée : la direction du
transfert de Bürgisser (TCS 235, 2000) va de la cible vers l'énoncé
algébrique — abstract officiel : si l'hypothèse de Valiant était
fausse, « *the nonuniform versions of NC and PH would coincide, and the
polynomial hierarchy would collapse to the second level* » (corps finis ;
caractéristique 0 sous GRH). Donc NP ⊄ P/poly ⟹ NC/poly ≠ PH/poly ⟹
VP ≠ VNP : la séparation algébrique est PLUS FAIBLE que la forme non
uniforme de P ≠ NP, elle ne l'implique pas. Le témoin est reproduit à
l'identique (19 valeurs) et le sous-lemme fin est tranché : l'écart
SPD_{1,1} vaut 2n(n − 1), exactement les relations de Laplace-Cramer
hors diagonale du déterminant. Une prise de numérotation, une précision
de miroir, et une conséquence pour la ligne 8 transmise à l'utilisateur.

Contexte : dixième candidature ; présentée d'emblée comme entrée de
registre ; pas de dérogation déclarée (la n° 10 ne l'écrit pas — sans
conséquence pour une entrée de registre). Tâche PR-015 déclarée au
backlog avant exécution ; instrument `checks/pr015_rangs_det_perm.py` ;
données `data/pr015_rangs_det_perm.md`.

## 1. Reformulation (§5.1)

Rayer la voie « mesures de rang sur espaces de dérivées » (Nisan-Wigderson
1997 → partielles décalées, Kayal 2012, GKKS 2013 → projections
multilinéaires par ensembles, LST 2021) : son G (une borne n^{ω(√d)} pour
perm en profondeur 4 homogène) donnerait VP ≠ VNP par réduction de
profondeur (Agrawal-Vinay, Koiran, Tavenas), mais VP ≠ VNP n'a aucune
flèche vers P ≠ NP — les transferts prouvés vont dans l'autre sens.

## 2. Ce qui tient

- **La pièce porteuse** (Bürgisser 2000) : direction confirmée sur
  l'abstract (texte intégral non ouvert — numéro de théorème non relevé,
  comme la candidature l'annonçait). Formulation exacte : NC/poly contre
  PH/poly — la candidature écrivait « forme exacte à lire sur texte »,
  c'est fait au niveau de l'abstract.
- **Le témoin** : 19 valeurs reproduites par un instrument indépendant
  (PD_k = C(n,k)² pour n ≤ 5 ; SPD det < perm aux cas k = 1 ou ℓ ≥ 1
  indiqués ; égalité à k = n − 1).
- **Les ombres booléennes de perm sont dans P** : « perm(A) > 0 » sur
  matrices 0/1 = existence d'un couplage parfait (polynomial) ; perm ≡
  det mod 2. Classique, exact — c'est l'illustration la plus directe du
  reflet : l'objet VNP-complet n'est dur que par le COMPTAGE.
- **Le statut de G** : ouvert ; la méthode plafonne au seuil (bornes
  n^{Ω(√d)} valant déjà pour l'IMM ∈ VP) ; LST 2021 = le sommet
  inconditionnel en profondeur constante. Indifférence à la classe
  (champ 4c) correctement diagnostiquée : c'est le symptôme d'E-1 en
  algèbre.
- **La forme v4.4** : six étiquettes utilisées à bon escient (PROUVÉ /
  OUVERTE / ABSENT ; EXCLUE et MIROIR côté P = NP), aucun numéro cité de
  mémoire. Aucun régime d'échec.

## 3. Attaque logique (§5.2) — les prises

### Prise 1 — Le sous-lemme fin, tranché : 2n(n − 1) relations de Laplace-Cramer

Mesuré : écart SPD_{1,1} = 12 à n = 3, 24 à n = 4 = 2n(n − 1). Lecture :
perm et det partagent les 2n − 2 relations d'Euler par lignes et
colonnes (81 − 77 = 4 pour perm à n = 3) ; det seul a les n(n − 1)
relations Σ_j x_ij ∂det/∂x_kj = 0 (i ≠ k) et leurs n(n − 1) transposées.
Vérifié à deux points, argumenté pour tout n. Conséquence pour la thèse
de la candidature : la mesure décalée sépare det de perm par une
identité algébrique propre au déterminant — pas par l'appartenance à
VP. Elle CONFIRME l'indifférence à la classe au lieu de la contredire.

### Prise 2 — Numérotation du mécanisme

La candidature propose « le n° 8, le reflet de comptage » ; (8) et (9)
sont pris depuis E-5 (triangle naturel/apprentissage/distingueur ;
échelle RR-exposée). Le reflet entre comme **(10)**. Il est bien
distinct de (3) l'ombre (énoncé plus fort que la cible, dont le
programme prend la cible pour hypothèse) : le reflet est un énoncé
PLUS FAIBLE que la cible, impliqué par elle. Et distinct de (4) la
barrière héritée : rien ne s'hérite ici, la flèche manque.

### Prise 3 — Précision du côté P = NP

« VP = VNP ⟹ NP ⊆ P/poly, flèche EXCLUE par uniformité » : exact —
Bürgisser donne l'effondrement de PH au second niveau, pas P = NP. Mais
la lecture inverse doit être écrite aussi : la ligne 19 utilise « FP =
#P ⟹ P = NP » (trivial, uniforme) ; VP = VNP est la version NON
uniforme et algébrique de FP = #P, et c'est l'absence d'uniformité qui
coupe la flèche. Le mécanisme (10) se lit donc : le comptage transfère
vers P = NP seulement en version uniforme ; vers P ≠ NP, jamais.

### Prise 4 — La conséquence pour la ligne 8 n'est pas à trancher ici

Si le reflet tient, la cellule 8 (GCT, perm contre det) n'a pas de
flèche OUVERTE vers P ≠ NP dans sa formulation algébrique — la règle du
2026-09-08 l'enverrait au registre. Mais Mulmuley revendique une
formulation booléenne (GCT pour NP ⊄ P/poly en caractéristique p) qui
pourrait porter une flèche directe ; la candidature ne tranche pas et
elle a raison. Rétrograder une ligne de la matrice n'est pas l'objet
d'une instruction de candidature : inscrit au backlog
(`ATLAS-L8-fleche [auto]`), décision utilisateur.

## 4. Barrières (§5.4)

Conformes. Relativisation sans objet structurel (aucun argument de
transfert à faire survivre — formulation exacte, distincte de l'erreur
type n° 1) ; preuves naturelles : analogue algébrique conditionnel
(Forbes-Shpilka-Volk 2018 ; Grochow-Kumar-Saks-Saraf 2017), touche le
mécanisme ; algébrisation : bloque toute traduction booléenne par le
comptage (#P ⊄ FP/poly derrière le mur, témoin AW — déjà au §3 du
prompt) ; monotone : Valiant 1980 / Jerrum-Snir 1982, non transférable.
Verrou réel : la flèche manquante, transferts prouvés à rebours ;
secondairement le plafond de méthode. Critères (a)/(b) : (a) actif,
(b) actif (la candidature teste chaque barrière avec sa raison).

## 5. Verdict (§5.5)

**ENTRE AU REGISTRE (E-6)**, avec le mécanisme transversal (10) le
reflet de comptage. Aucun fil. Réserves : Bürgisser lu au niveau de
l'abstract ; « plafond n^{O(√d)} des partielles décalées » — théorème
écrit (EGOW 2018, survey Saptharishi) ou constat : non tranché, sans
effet sur l'entrée (la flèche manque de toute façon).

## 6. Pièces et sources

`checks/pr015_rangs_det_perm.py` ; `data/pr015_rangs_det_perm.md` ;
`tasks/done/PR-015.md`. Vérifié : [Bürgisser, TCS 235 (2000), abstract](https://www.sciencedirect.com/science/article/pii/S0304397599001838).
Non ouverts : Agrawal-Vinay 2008, Koiran 2012, Tavenas 2013, GKKS 2013,
KLSS 2014, LST 2021, EGOW 2018, FSV 2018, GKSS 2017, GCT I/JACM 2011.
