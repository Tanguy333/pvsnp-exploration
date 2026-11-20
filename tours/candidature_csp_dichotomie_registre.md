# Candidature n° 11 (prompt v4.5, 2026-11-21) : « La classification algébrique des CSP — quand classifier épuise l'espace des G » (entrée de registre E-7) — instruction du Réfuteur (PR-017)

**Verdict : ENTRE AU REGISTRE (E-7).** Le témoin est reproduit à
l'identique (9/9 contrôles ; seuil d'Olšák à c = 6) ; le statut de G est
exact ; la dichotomie Bulatov-Zhuk vide bien l'espace des G pour les CSP
à gabarit fini. Deux prises : le mécanisme n° 11 est une OBSERVATION à
falsificateur précis, pas un théorème (la candidature le dit ; je
l'assortis de sa frontière exacte), et le seuil c* = 6 est une mesure
sans portée démontrée.

Contexte : onzième candidature, présentée en entrée de registre. Tâche
PR-017 déclarée au backlog AVANT exécution. Instrument
`checks/pr017_polymorphismes.py` ; données `data/pr017_polymorphismes.md`.

## 1. Reformulation

Rayer la direction « P = NP par la classification des CSP » : pour les
gabarits finis, la dichotomie (Bulatov 2017, Zhuk 2020) dit que tout
CSP(Γ) est dans P ou NP-complet, si bien qu'aucun G de la forme
« CSP(Γ) ∈ P » n'est à la fois ouvert et non miroir ; pour les PCSP, la
frontière (coloriage approché, (K₃, K₅) NP-dur, BBKO 2021) est ouverte,
mais un G comme « PCSP(K₃, K₆) ∈ P » est soit miroir (s'il est NP-dur),
soit sans transfert.

## 2. Ce qui tient

- **Le témoin** : 9/9 contrôles de Siggers conformes à Schaefer et
  Hell-Nešetřil ; Olšák K₃⁶ → K_c : NON pour c = 3, 4, 5, OUI pour
  c = 6, 7 — identique, jusqu'aux tailles d'encodage.
- **Le statut de G** : PCSP(K₃, K₆) ouvert à ma connaissance ; aucune
  dureté 2021-2026 trouvée [NON TROUVÉ — recherche non exhaustive]. Un
  piège à consigner : la dureté de (K₃, K₅) n'implique PAS celle de
  (K₃, K₆) — relâcher la promesse rend le problème plus FACILE (un
  outil de recherche a soutenu l'inverse ; c'est faux).
- **La forme v4.5** : direction P = NP déclarée, miroir et absence
  correctement distingués au champ 4 (d), test de plafond sur la
  propriété consommée (les conditions de mineur), aucun numéro cité de
  mémoire.
- **Les barrières** : traitées exactement (famille algorithmique ;
  « algébrique » au sens de l'algèbre universelle, mise en garde
  utile) ; face monotone juste (Datalog est monotone, les équations
  linéaires en sont le Tardos — Feder-Vardi 1998).

## 3. Prises

### Prise 1 — Le mécanisme n° 11 est une observation, et sa frontière se nomme

« Toute dérivation connue de "Π ∈ P ⟹ P = NP" est une réduction » n'est
pas un énoncé mathématique (il quantifie sur les preuves connues) ; il
entre au registre comme observation, avec son falsificateur. Sa
frontière est plus nette que ne l'écrit la candidature : les transferts
NON réductifs connus atterrissent tous en deçà de P = NP —
Valiant-Vazirani (USAT ∈ P ⟹ NP = RP, réduction aléatoire) ;
Kabanets-Cai (MCSP ∈ P ⟹ pas de fonctions à sens unique, pas P = NP) ;
Karp-Lipton et Mahaney (leurs hypothèses contiennent déjà une
NP-dureté). L'exemple MCSP est le meilleur témoin du mécanisme : c'est
le candidat NP-intermédiaire le plus étudié, et son transfert s'arrête
aux OWF — c'est la ligne 13 qui cherche à le rendre NP-dur. Formulation
retenue : *un G de la forme « Π ∈ P » n'a de transfert connu vers
P = NP que par réduction (miroir) ; les transferts non réductifs connus
atterrissent en deçà (RP, absence d'OWF)*.

### Prise 2 — Le seuil c* = 6 : une coïncidence sans portée démontrée

Le seuil d'Olšák tombe sur la frontière de dureté connue, mais
l'existence d'un polymorphisme d'Olšák pour (K₃, K₆) ne donne aucun
algorithme (la traitabilité des PCSP n'est pas caractérisée par une
condition de mineur unique), et son absence pour c ≤ 5 n'est pas un
critère de dureté citable — la dureté de (K₃, K₅) a été prouvée
autrement (BBKO ; version topologique Krokhin-Opršal-Wrochna-Živný).
Je ne tranche pas l'explication ; la candidature avait annoncé que le
verdict n'en dépendait pas, et c'est exact.

### Prise 3 — Numérotation

Le mécanisme entre comme (11) : la numérotation de la candidature est
juste.

## 4. Verdict

**ENTRE AU REGISTRE (E-7)**, mécanisme transversal (11) « classifier
n'est pas séparer », au statut d'observation. Aucun fil. Réserves :
statut de PCSP(K₃, K₆) établi par recherche non exhaustive ; BBKO,
Bulatov, Zhuk, KMM, Olšák non ouverts (classiques, non contredits).
