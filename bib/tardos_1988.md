# A-003 : Audit — Tardos, « The gap between monotone and non-monotone circuit complexity is exponential »

> Tâche type A. Exécutée le 2026-06-09. **Texte intégral lu** (2 pages, scan
> hébergé par l'auteure :
> [cs.cornell.edu/~eva/Gap...pdf](https://www.cs.cornell.edu/~eva/Gap.Between.Monotone.NonMonotone.Circuit.Complexity.is.Exponential.pdf)).
> Citations textuelles marquées « > » (orthographe OCR corrigée quand évidente).

## 1. Référence canonique

- É. Tardos, *« The gap between monotone and non-monotone circuit complexity
  is exponential »*, Combinatorica, pp. 141-142. Reçu le 6 octobre 1986.
- **Divergence de millésime constatée** : l'en-tête du scan original porte
  « COMBINATORICA 7 (4) (1987) 141—142 », tandis que la fiche Springer
  ([doi:10.1007/BF02122563](https://doi.org/10.1007/BF02122563)) et la
  citation d'usage (dont notre cahier §7) disent Combinatorica 8, 1988.
  Citer « 1988 » reste l'usage ; la divergence est notée ici par fidélité au
  document.
- Note de 2 pages — l'un des ratios influence/longueur les plus élevés du
  domaine.

## 2. Résultat principal — énoncé exact

> « A. A. Razborov has shown that there exists a polynomial time computable
> monotone Boolean function whose monotone circuit complexity is at least
> n^{c log n}. We observe that this lower bound can be improved to
> exp(c·n^{1/6−o(1)}). »

(Exposant : `n` = nombre de bits d'entrée = v² pour un graphe à v sommets ;
l'amélioration Alon-Boppana donne exp en `v^{1/3}` = `n^{1/6}`.)

**Corollaire-pivot** (attribué dans la note à Razborov ; Alon-Boppana) :

> « Let φ(X) be any monotone graph function such that ω(X) ≤ φ(X) ≤ χ(X) [(*)].
> Then for any function 3 ≤ f(v) ≤ (v/log v)^{2/3}/4 the monotone circuit
> complexity of deciding whether or not φ(X) ≥ f(v) is at least
> exp(c·f(v)^{1/2}). »

**La construction** : la θ-capacité de Lovász du complément.

> « The function φ(X) = θ(X̄), where X̄ denotes the complement of X, is a
> monotone function satisfying (*). Grötschel, Lovász and Schrijver gave a
> polynomial time approximation algorithm for θ. »

Comme l'arrondi de l'approximation peut perdre la monotonie, Tardos perturbe
par le nombre d'arêtes e(X) pour obtenir :

> « φ(X) is a polynomial time computable monotone function satisfying (*). »

La borne du corollaire s'applique alors à une fonction **dans P** :
gap monotone/non-monotone exponentiel. ∎

## 3. Hypothèses non-triviales

1. **Le sandwich ω ≤ θ̄ ≤ χ** (théorème du sandwich de Lovász 1979) — c'est
   ce qui permet à l'argument d'approximation de Razborov/Alon-Boppana
   (conçu pour CLIQUE) de s'appliquer tel quel à θ̄.
2. **GLS / méthode de l'ellipsoïde** (Grötschel-Lovász-Schrijver 1981,
   Khachiyan 1979) pour la calculabilité polynomiale de θ à ε près. La
   fonction témoin est donc poly-time mais *pas* combinatoirement simple.
3. L'argument de borne inférieure lui-même est **celui d'Alon-Boppana 1987**
   (méthode d'approximation par tournesols) — Tardos n'introduit pas de
   nouvelle technique de borne, mais une nouvelle *fonction témoin*.

## 4. Outils techniques

- Méthode d'approximation de Razborov 1985 (version Alon-Boppana 1987).
- θ-fonction de Lovász (Shannon capacity, IEEE IT 1979) + sandwich.
- Algorithme d'approximation polynomial de θ (GLS 1981, ellipsoïde).
- Astuce de monotonisation : perturbation par e(X) après arrondi.

## 5. Ce que le papier NE PROUVE PAS

1. **Aucune borne pour les circuits généraux (non-monotones).** C'est même
   tout le contraire : il prouve que les bornes monotones *ne disent rien*
   des circuits généraux. La fonction témoin a complexité monotone
   exponentielle ET circuits généraux polynomiaux.
2. **Rien sur P vs NP.** Conséquence (négative) : les bornes monotones
   exponentielles pour CLIQUE (Razborov 1985, Alon-Boppana 1987) ne peuvent
   pas être un chemin vers NP ⊄ P/poly par levée de la restriction monotone —
   le gap est intrinsèque au modèle, pas à la difficulté de la fonction.
3. **Ne ferme pas la voie monotone pour toute fonction** : pour les *slice
   functions* (Berkowitz), complexités monotone et générale coïncident à
   polynôme près — ce contexte n'est pas dans la note (ajout du dépôt,
   clairement attribué : Berkowitz 1982), mais montre que la barrière de
   Tardos s'applique aux bornes monotones *génériques*, pas à des classes
   restreintes soigneusement choisies.

## 6. Statut de barrière (lecture pour l'Atlas)

C'est la **barrière #4 du cahier** (« barrière monotone Razborov-Tardos »,
activée au Tour 24). Formulation opérationnelle issue de l'audit :

> Toute technique de borne inférieure qui fonctionne *uniformément* pour
> toutes les fonctions monotones (ou qui ne lit que la structure
> monotone/positive — circuits monotones, circuits arithmétiques monotones,
> circuits tropicaux via Jerrum-Snir 1982) est bornée par le témoin de
> Tardos : elle « prouverait » une borne exponentielle pour une fonction de
> P, donc ne peut pas séparer quoi que ce soit de P.

Test pratique (cahier §4 q.14) : toute piste dans ces cadres doit dire
explicitement pourquoi son argument ne s'applique PAS à θ̄-perturbée.

## 7. Lien à la bibliographie §7 du cahier et aux tours du dépôt

- Cahier §7.3 : cité comme renforcement de Razborov 1985 / Alon-Boppana 1987.
  L'audit précise le mécanisme exact (sandwich + GLS) et la divergence de
  millésime (7(4) 1987 sur le scan vs 8 (1988) chez Springer).
- **Tour 24 (tropical)** : la réfutation invoquait Tardos comme barrière
  létale via Jerrum-Snir (tropical = monotone arithmétique). L'audit
  confirme : la fonction de Tardos est le contre-exemple structurel canonique
  à tout transfert monotone → général.
- **Tour 7 (formules monotones)** et **Tour 11 (KW monotone)** : leçons
  compatibles — q.9 du cahier (« le cadre monotone n'est pas suffisant pour
  P vs NP ») est exactement le contenu de ce papier.
- Cellule Atlas correspondante : ligne « approches monotones/tropicales » ×
  colonne « barrière Tardos » = **fermée, avec témoin** (θ̄-perturbée ∈ P,
  complexité monotone exp(n^{1/6−o(1)})).

## Limitations de l'audit

- Le scan est de qualité OCR moyenne ; les exposants exacts (n^{1/6−o(1)},
  f(v)^{1/2}, (v/log v)^{2/3}/4) ont été reconstruits à partir du texte
  OCR + connaissance des énoncés standards — la version Springer fait foi.
- Les preuves d'Alon-Boppana (sur lesquelles tout repose) ne sont pas
  auditées ici (papier séparé, 23 pages — tâche candidate si besoin).
