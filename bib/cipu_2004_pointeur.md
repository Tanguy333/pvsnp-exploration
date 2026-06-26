# Pointeur d'antériorité — Cipu 2004 (signalé par Mossinghoff, 2026-06-12)

Source : email de M. Mossinghoff à Tanguy. À VÉRIFIER sur le texte si une
revendication formelle est faite ; ici on consigne ce que Mossinghoff en dit.

- **Référence** : Mihai Cipu, LMS Journal of Computation and Mathematics
  (LMS JCM), 2004. Sujet : polynômes produits purs (pure product polynomials).
- **Différence clé** : Cipu **minimise d'autres quantités** que la hauteur
  (max des coefficients) — typiquement la **norme L₂ des coefficients** ou
  analogue. Ses exemples à **multiplicité 20 ont hauteur 2** (donc PAS
  hauteur 1) — excellents pour le but L₂, mais ne répondent pas à la
  question d(m) de Borwein–Mossinghoff (hauteur 1).
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
