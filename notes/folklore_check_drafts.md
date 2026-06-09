# Check communautaire L18 — textes prêts à poster

> Préparé le 2026-06-09 (suite de `bib/l18_status.md` et `notes/dnf_min_ip.md`).
> **Étape 0 faite** : recherche d'une question existante sur
> cstheory.stackexchange (requêtes « DNF size inner product », « minimal DNF
> inner product bent ») — **aucune question existante trouvée**. La question
> n'a jamais été posée publiquement.
>
> **À faire par Tanguy** (les deux canaux sont complémentaires ; le premier
> suffit en général) :
> 1. Poster la question §1 sur https://cstheory.stackexchange.com (tags
>    suggérés : `cc.complexity-theory`, `boolean-functions`, `reference-request`).
> 2. Optionnel : envoyer le mail §2 à Mika Göös (adresse sur sa page EPFL).
>
> Si une référence sort : la consigner dans `bib/l18_status.md` (verdict
> passe à « folklore identifié ») et abandonner la note. Si rien ne sort
> sous ~1 semaine : le verdict « non recensé » est solide, passer à la
> relecture humaine de la preuve puis arXiv.

---

## 1. Question cstheory.stackexchange (anglais, format du site)

**Titre proposé :**

```
Is the exact minimum DNF size of the inner product function known?
```

**Corps :**

```markdown
Let $\mathrm{IP}_{2n}(x,y) = \sum_{i=1}^n x_i y_i \bmod 2$ be the inner
product function on $2n$ variables. I am interested in the minimum number
of terms (monomials) in a DNF — an OR of ANDs of literals, unbounded
fan-in — computing $\mathrm{IP}_{2n}$ exactly.

By a direct argument one can show:

$$\mathrm{DNF}(\mathrm{IP}_{2n}) = \frac{3^n - 1}{2},$$

and moreover $\mathrm{IP}_{2n}$ has exactly $(3^n-1)/2$ prime implicants,
each of which is *essential* (has a point covered by no other prime
implicant), so the minimal DNF is unique. The proof is an induction on the
disjoint XOR decomposition $\mathrm{IP}_{2(n+1)} = \mathrm{IP}_{2n} \oplus
x_{n+1}y_{n+1}$: writing $a_n = \#\mathrm{primes}(\mathrm{IP}_{2n})$ and
$b_n = \#\mathrm{primes}(\neg\mathrm{IP}_{2n})$, a case analysis gives
$a_{n+1} = 2a_n + b_n$, $b_{n+1} = a_n + 2b_n$, with $(a_1,b_1)=(1,2)$,
hence $a_n = (3^n-1)/2$. Essentiality follows from an explicit witness
construction per prime. (Verified by exhaustive search / exact set-cover
ILP up to $n = 4$, i.e. 8 variables, value 40.)

**Question: is this exact value already in the literature?** I could not
find it in:

- the recent depth-3 line for IP (Golovnev–Kulikov–Williams ITCS'21;
  Frankl–Gryaznov–Talebanfard ITCS'22; Göös–Guan–Mosnoi MFCS'23/I&C'24;
  Amano ISAAC'23) — these study $\Sigma_3^2$ complexity and the depth-2
  case is never stated, although FGT'22 prove the closely related fact
  that any 2-CNF consistent with IP accepts at most $3^{n/2}$ assignments
  (tight, unique optimum);
- Cohen–Shinkar (ITCS'16), which is about DNF *of parities* — a different
  model;
- Jukna's *Boolean Function Complexity*, where IP appears in communication
  complexity and $\Sigma_3^\oplus$ contexts but not for plain DNF size;
- the switching-theory literature (Sasao–Butler on minimum SOPs of
  bi-decomposable functions covers AND/OR bi-decompositions, not XOR).

Given that exact minimal-DNF computations for specific functions were a
specialty of the Russian school (Yablonskii and others, *Problemy
Kibernetiki*, 1960s–70s), a pointer into that literature would be
especially welcome. Note that the related constant $3^{n/2}$ also shows up
as the optimal value in FGT'22, so the result may well be folklore — I
would just like a citable source (or confirmation that there is none).
```

---

## 2. Mail à Mika Göös (optionnel, anglais)

**Objet :** `Exact minimum DNF size of inner product — known reference?`

```
Dear Professor Göös,

I have a quick reference question related to your work with Guan and
Mosnoi on depth-3 circuits for inner product.

By an induction over the disjoint XOR decomposition, one can show that
the minimum DNF size of IP_{2n} is exactly (3^n - 1)/2, with all prime
implicants essential (so the minimal DNF is unique). I could not find
this exact statement anywhere — not in the depth-3 line (where FGT'22's
tight 3^{n/2} bound for 2-CNFs consistent with IP seems to be the closest
relative), not in Cohen–Shinkar's DNF-of-parities, not in Jukna's book,
and not in the Sasao–Butler switching-theory literature on minimum SOPs.

Do you know whether this is folklore with a citable source (possibly in
the Russian literature on minimal DNFs), or genuinely unrecorded?

Thank you for your time,
Tanguy Le Mer
```

---

## 3. Journal du check

| Date | Action | Résultat |
|---|---|---|
| 2026-06-09 | Recherche question existante sur cstheory.SE (2 requêtes) | Aucune question existante |
| *(à remplir)* | Question postée sur cstheory.SE | *(lien)* |
| *(à remplir)* | Réponses reçues | *(référence trouvée OU rien après 1 semaine)* |
| *(à remplir)* | Mail à Göös | *(réponse)* |
