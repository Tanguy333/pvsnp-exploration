# A-005 : Audit — Cai-Fürer-Immerman 1992 + Atserias-Bulatov-Dawar 2007

> Tâche type A. Exécutée le 2026-06-09.
> **Sourçage** : CFI 1992 original paywallé (Springer/IEEE) ; construction et
> théorème extraits de Dawar-Richerby-Rossman 2008 (*« Choiceless polynomial
> time, counting and the Cai-Fürer-Immerman graphs »*, APAL 152,
> [PDF Duke](https://users.cs.duke.edu/~br148/CPT-CFI.pdf), **33 pages
> greppées**). ABD 2007 lu en **texte intégral** (12 pages,
> [PDF Cambridge](https://www.cl.cam.ac.uk/~ad260/papers/abd-icalp07.pdf)).
> Citations « > » attribuées à leur source.

## 1. Références canoniques

- J.-Y. Cai, M. Fürer, N. Immerman, *« An optimal lower bound on the number
  of variables for graph identification »*, Combinatorica 12(4), 1992,
  pp. 389-410 (FOCS 1989).
  [doi:10.1007/BF01305232](https://doi.org/10.1007/BF01305232).
- A. Atserias, A. Bulatov, A. Dawar, *« Affine systems of equations and
  counting infinitary logic »*, ICALP 2007 ; version journal Theoretical
  Computer Science 410(18), 2009.
- Source secondaire utilisée : A. Dawar, D. Richerby, B. Rossman, Annals of
  Pure and Applied Logic 152(1-3), 2008, pp. 31-50.

## 2. Théorèmes principaux — énoncés exacts

### CFI (via DRR 2008)

> « The example constructed by Cai et al. gives, for each k ∈ ℕ, a pair of
> graphs, rich in automorphisms, that cannot be distinguished in C^k_{∞ω},
> the k-variable fragment of infinitary logic with counting quantifiers. It
> follows that the graphs are not distinguished by any formula of IFP+C
> […] There is, however, a single polynomial-time Turing machine that is
> able to distinguish the members of every pair. »

Donc : **IFP+C (= FPC) ⊊ P**, avec témoin explicite.

Forme générale de la construction (DRR) :

> « a general construction that gives, for each finite connected graph G
> with at least two vertices, a pair of graphs G⁰ (referred to as 'even')
> and G¹ ('odd') which cannot be distinguished in C^k if G has no separators
> of size k. »

### Le mécanisme de parité globale (DRR, Definition 3)

> « Let T ⊆ V. For each v ∈ T, let v_T = {v_X : ‖X‖ is odd} and, for each
> v ∈ V∖T, let v_T = {v_X : ‖X‖ is even}. G_T is the subgraph of Ĝ induced
> […] G_T is even if ‖T‖ is even and odd, otherwise. »

**C'est l'invariant que la construction du Tour 25 n'avait pas** : la classe
d'isomorphisme de G_T ne dépend que de la *parité globale* de ‖T‖ — les
twists locaux se compensent deux à deux par les automorphismes des gadgets,
seule la somme mod 2 survit.

### ABD 2007 (texte intégral)

> « We show that testing the solvability of systems of equations over a
> finite Abelian group, a tractable CSP that was previously known not to be
> definable in Datalog, is not definable in an infinitary logic with
> counting and hence that it is not definable in least fixed point logic or
> its extension with counting. »

Et la généralisation par théorie des congruences modérées :

> « if this variety admits either the unary or affine type, the
> corresponding CSP is not definable in the infinitary logic with counting. »

ABD réinterprète donc CFI en termes de **CSP affines** : la solvabilité
d'équations linéaires sur Z₂ (chaque variable dans exactement deux
équations pour la version graphe) est *le* contenu computationnel des
graphes CFI.

## 3. Hypothèses non-triviales

1. **CFI** : le graphe de base G doit être sans séparateurs de taille k
   (expanseurs pour le résultat optimal Ω(n) variables). La paire (G⁰, G¹)
   est riche en automorphismes — c'est ce qui aveugle C^k.
2. **ABD** : groupe abélien fini (≥ 2 éléments) ; la tractabilité vient du
   polymorphisme de Mal'tsev (élimination gaussienne), la non-définissabilité
   du type affine.
3. **Les deux résultats sont des bornes sur des LOGIQUES, pas des circuits** :
   la « complexité » mesurée est le nombre de variables / la définissabilité,
   pas la taille de circuit.

## 4. Outils techniques

- Jeux d'Ehrenfeucht-Fraïssé à k galets avec comptage (bijection games,
  Hella) pour la borne C^k.
- Gadgets de twist à automorphismes locaux + invariant de parité globale.
- ABD : réduction Datalog-préservante des équations de groupe vers tout CSP
  dont la variété admet le type unaire ou affine (théorie des congruences
  modérées de Hobby-McKenzie).

## 5. Ce que ces papiers NE PROUVENT PAS

1. **Aucune borne de circuit, aucune séparation de classes de machines** :
   FPC ⊊ P ne dit rien sur P vs NP — les deux côtés sont dans P. C'est une
   séparation de *pouvoir définitionnel*.
2. **Ne séparent pas CPT de P** : Dawar-Richerby-Rossman 2008 montrent
   précisément que **CPT distingue les graphes CFI** (sur graphes de base
   ordonnés, via des ensembles héréditairement finis de rang non-borné).
   La question de Gurevich (CPT = P sur structures non-ordonnées ?) reste
   ouverte — les CFI ne sont PAS un témoin contre CPT.
3. **Le mécanisme exige un domaine à invariant de parité** : SAT n'étant pas
   affine sur Z₂, la transposition naïve échoue (réfuté empiriquement au
   Tour 25 du dépôt ; ABD délimite précisément le domaine d'application —
   CSP dont la variété admet le type affine).

## 6. Lien à la bibliographie §7 du cahier

§7.5ter déjà créé (post-Tour 25) avec ces références — l'audit ajoute les
énoncés verbatim et la Definition 3 (mécanisme de parité), qui manquaient.

## 7. Lien aux tours et tâches du dépôt

- **Tour 5** (CPT+C jeux de pavage, ❌) : l'erreur était d'encoder SAT *en
  surface* (coloration FO-définissable). Le vrai CFI cache l'information
  dans la *structure d'automorphismes* — exactement ce que dit la
  Definition 3.
- **Tour 25** (CFI-rigidification de SAT, ❌) : l'erreur complémentaire —
  des gadgets `(x_i⁰, x_i¹)` sans compensation deux-à-deux par
  automorphismes, donc sans invariant de parité globale. q.15 du cahier
  confirmée par les textes.
- **Cellules Atlas** :
  - « complexité descriptive × FPC » : **fermée** — FPC ⊊ P prouvé (CFI),
    avec réinterprétation CSP affine (ABD). Une borne FPC ne peut pas
    servir P vs NP (les deux côtés dans P).
  - « complexité descriptive × CPT » : **ouverte** — CPT distingue CFI
    (DRR 2008), aucun témoin contre CPT connu ; c'est la vraie question de
    Gurevich, intacte depuis 1988/1999.

## Limitations de l'audit

- CFI 1992 original non lu (paywall) — la borne optimale Ω(n) variables et
  les détails de la preuve par jeux ne sont pas extraits verbatim du
  primaire.
- La partie tame congruence theory d'ABD (Theorems 11, 15) est citée
  structurellement sans audit des preuves algébriques.
