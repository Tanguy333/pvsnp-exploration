# D-001 : Méthode Williams (algorithmic method) × Preuves naturelles (RR)

> Tâche type D. Exécutée le 2026-06-09. Sources : audits A-001 (Williams
> 2011, texte CCC'11) et A-007 (Razborov-Rudich 1997, texte PS Razborov).
> Citations « > » reprises de ces audits (vérifiées sur textes).

## 1. La barrière

RR 1997 (A-007) : toute propriété **constructive** (décidable en `2^{O(n)}`
dans la table de vérité) et **large** (fraction ≥ `2^{−O(n)}`) qui est
**utile** contre une classe C contenant des PRF casserait les générateurs
pseudo-aléatoires de dureté `2^{n^ε}`. Sous crypto standard : pas de preuve
naturelle de bornes super-polynomiales contre P/poly (ni TC⁰, qui contient
les PRF de Naor-Reingold).

## 2. Comment la méthode Williams est censée la franchir

La méthode : (i) connexion « algorithme SAT non-trivial pour C ⇒ borne
NEXP ⊄ C » (générique, A-001 Thm 3.1-3.2) ; (ii) algorithme SAT non-trivial
pour C = ACC (via Beigel-Tarui, A-002).

## 3. Verdict : **FRANCHISSEMENT — par double sortie, documentée dans les textes**

### Sortie 1 : l'argument n'est pas une propriété de tables de vérité

Williams, verbatim (A-001 §6) :

> « Intuitively, we circumvent the natural proofs barrier [RR97] because of
> the use of diagonalization. More precisely, we rely heavily on strong
> completeness properties of a specific NEXP language, namely SUCCINCT
> 3SAT […] So it looks unlikely that one may extract any P-natural or
> NP-natural properties from the proof. »

Et RR eux-mêmes avaient désigné cette porte (A-007 §5.3) :

> « a counting argument is presumably not a natural argument. »

La preuve de Williams ne produit aucun prédicat `f_n ∈? C*_n` sur les tables
de vérité : elle dérive une contradiction avec la hiérarchie du temps
non-déterministe. La *constructivité* et la *largeness* sont sans objet.

### Sortie 2 : ACC ne contient probablement pas de PRF

Williams, verbatim :

> « there is little evidence that ACC contains pseudorandom functions, so
> natural proofs may not be a barrier for ACC after all. »

Même si la preuve se naturalisait, la prémisse crypto de RR (PRF dans la
classe cible) n'est pas remplie pour ACC⁰.

### Réserve honnête (du texte même)

> « It is hard to formally rule out that a proof cannot possibly be made
> natural, without showing either an algorithmic lower bound […] or a
> circuit upper bound (the circuit class under discussion has pseudorandom
> functions). »

Le franchissement est donc *argumenté fortement* (deux sorties
indépendantes), pas *démontré formellement* — contrairement au
franchissement de relativisation/algébrisation qui, lui, est démontré
(oracle d'Aaronson, cf. A-001).

## 4. Conséquence pour la ligne TC⁰ de l'Atlas

Si la méthode s'étendait à TC⁰, la sortie 2 disparaît (TC⁰ ⊇ PRF de
Naor-Reingold) — seul resterait l'argument « diagonalisation, pas une
propriété ». La sortie 1 suffit en principe : le verrou de l'extension
TC⁰ n'est PAS RR, c'est l'**absence d'algorithme SAT non-trivial** (cf.
cellule « Williams × TC⁰ » : A-002 + F-001).

## Références de la cellule

A-001 (`bib/williams_2011.md`), A-007 (`bib/razborov_rudich_1997.md`),
A-002 (`bib/beigel_tarui_1994.md`), F-001 (`tasks/done/F-001.md`).
