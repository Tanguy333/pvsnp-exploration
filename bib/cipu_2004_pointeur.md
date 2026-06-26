# Pointeur d'antériorité — Cipu 2004 (signalé par Mossinghoff, 2026-06-12)

Source : email de M. Mossinghoff à Tanguy. À VÉRIFIER sur le texte si une
revendication formelle est faite ; ici on consigne ce que Mossinghoff en dit.

- **Référence + PDF LUS EN ENTIER** (2026-06-27, PDF fourni par Tanguy) :
  Mihai Cipu, **« Upper bounds for norms of products of binomials »**,
  LMS J. Comput. Math. **7 (2004), 37–49**, DOI 10.1112/s1461157000001030.
- **Définitions exactes (p.1, verbatim)** : binômes = X^u − X^v ; les
  produits pertinents pour PTE sont les **produits purs** ∏(1−X^{a_i})
  (condition iii). La quantité PRIMAIRE est la **length L(P) = norme ℓ₁**
  (somme des |coefficients|). Il rapporte AUSSI la **norme euclidienne**.
  → Donc « L2 » seul (mon brouillon initial) était INEXACT : c'est ℓ₁
  (length) d'abord, ℓ₂ ensuite. (« 23e auto-correction ».)
- **Table 1, ligne n = 20 — REPRODUITE EXACTEMENT** : exposants
  {1–11, 13, 15, 17, 19, 21, 23, 25, 27, 31} (20 facteurs), degré 257,
  **hauteur 2**, **length L = 116 = B1(20)**, **‖·‖₂² = 132 = B2(20)**,
  multiplicité 20. → Cipu A un exemple mult-20 (B1=length ℓ₁, B2=ℓ₂²),
  vérifié par reconstruction exacte. NE PAS dire « il n'avait rien ».
- **Complémentarité avec V-047** : Cipu (degré 257, hauteur 2, optimise
  length/ℓ₂) vs nous (degré 307, **hauteur 1**, optimise hauteur puis degré).
  Objectifs distincts → notre nouveauté HAUTEUR 1 tient (confirmée
  Mossinghoff : pas d'exemple hauteur-1 mult-20 antérieur).
- **Lien P_j(D) RÉDUIT** : P_j(D) = ‖(1−x)^D(1+x)^j‖² = ‖(1−x)^{D−j}(1−x²)^j‖²
  est une forme close pour la norme ℓ₂² d'un produit pur, MAIS à exposants
  dans {1, 2} seulement — un cas très particulier de ses objets. Lien réel
  mais MINEUR ; ne pas le survendre.
- **Conséquence** : Cipu 2004 est ADJACENT mais NE PRÉEMPTE PAS notre
  résultat V-047 (produit pur plat = hauteur 1, multiplicité exactement 20,
  degré 307). Mossinghoff confirme explicitement : « *I do not believe
  another example with height 1 and multiplicity exactly 20 has appeared
  before.* »

## Statut du résultat V-047 après réponse de l'auteur

NOUVEAUTÉ CONFIRMÉE PAR L'AUTEUR DE LA TABLE. Notre produit
∏(1−x^{t}), t = {1,2,3,4,5,7,8,9,11,12,13,15,17,19,21,23,27,29,31,50},
degré 307, hauteur 1, multiplicité exactement 20, comble le rang m=20
absent de la Table 1 de BM 2000. Mossinghoff valide aussi l'idée
méthodologique (borner la hauteur de transit) comme « promising space »,
et note que le grand saut d'exposant 31→50 explique que leur méthode de
l'époque l'ait manqué.

## Actions possibles (non engagées)

- Soumission OEIS A059753 (extension du rang m=20) — désormais bien fondée
  (nouveauté confirmée). À étiqueter « smallest known / upper bound ».
- Vérifier le texte de Cipu 2004 SI une note/soumission formelle est faite
  (pour citer correctement l'adjacence L₂ vs hauteur).

## Cadre honnête (P vs NP)

Résultat réel et confirmé neuf, mais PÉRIPHÉRIQUE à P vs NP : c'est de la
théorie des nombres expérimentale (un rang d'une table de hauteur-1), sans
lien établi avec la séparation des classes. À ne pas surévaluer dans le
récit du dépôt.
