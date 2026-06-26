# Brouillon — réponse à Michael Mossinghoff (suite à sa confirmation)

> À envoyer par Tanguy. Collégial, focalisé. Répond à : Cipu 2004, la
> méthode de transit, le saut 31→50. Offre la donnée τ(m). Honnête sur
> verifié vs exploratoire. Code/données disponibles.

---

**Subject:** Re: Height-1 pure product at multiplicity 20 — thank you, and the transit data

Dear Michael,

Thank you so much — I'm delighted it's of interest, and grateful for the
Cipu reference; I'll look it up. The distinction you draw is exactly
right: my search fixes height = 1 (max coefficient) and minimizes degree,
so Cipu's L2-minimizing examples at multiplicity 20, being height 2, live
in a different optimum. Good to know the adjacency precisely.

On the transient-height idea, it turned into a small but clean invariant
that may amuse you. Define τ(m) as the smallest transient height attained
along the *ascending* partial products of an extremal (smallest-degree)
height-1 example at multiplicity m. Computing this for your Table 1 plus
m = 20:

  m :  6  8  9 12 13 14 15 16 17 18 19 20 21
  τ :  2  2  2  2  2  2  3  3  3  2  2  3  2

So the extremals split into a transit-2 family and a transit-3 family
{15, 16, 17, 20} — and m = 20 is precisely a transit-3 rank, which (as you
suspected) is likely why an ascending search bounded near height 2 would
miss it. The 31 → 50 jump is the signature of that: the degree-307 example
needs that large gap to keep the full product flat while passing through a
height-3 intermediate.

Two caveats I want to state plainly: (i) τ(m) is defined on the *ascending*
order of exponents — a different traversal might realize a lower transient,
so this is an upper bound on a "true" transit invariant, not a theorem;
(ii) my 307 is minimal only within (transit ≤ 6, degree ≤ 330) — I have not
ruled out a smaller degree at transit ≥ 7, so it is a smallest-known value
in your table's sense, not a proven minimum.

I did read Cipu's paper after your note — thank you, it was just the right
pointer. I reproduced his n = 20 entry exactly: the product over exponents
{1–11, 13, 15, …, 27, 31} has length 116 and squared Euclidean norm 132
(his B1, B2), with degree 257 and height 2. So it sits right beside the
height-1 degree-307 example, with the complementarity you described — he
minimizes length / Euclidean norm and allows height 2, whereas I fix
height 1 and minimize degree. (My own route to these came from the integer
lattice of polynomials of degree ≤ n divisible by (1−x)^{d+1}, studied by
Krishan and Vishwanathan, ECCC TR24-074, 2024, for degree/error tradeoffs;
there one minimizes the Euclidean norm, which is how I ended up next door
to Cipu's question.)

I'm tempted to record the m = 20 value at OEIS A059753 (which currently
stops at m = 14), clearly flagged as a smallest-known upper bound — would
that seem reasonable to you, or premature?

I'll certainly keep you posted as the transit-height exploration develops,
and would gladly share the (short, exact-arithmetic) code or data whenever
it would be useful.

With thanks and best regards,
Tanguy

---

## Statut épistémique (hors email, pour Tanguy)
- τ(m) table : MESURÉE exact (V-047/V-048). « transit défini sur l'ordre
  croissant » = caveat honnête déjà inscrit.
- 307 minimal sous (transit ≤ 6, degré ≤ 330) : MESURÉ (V-049). Caveat
  transit ≥ 7 inscrit.
- **Forme close P_j(D) = ‖(1−x)^D(1+x)^j‖² : VÉRIFIÉE EXACTE** (convolution
  vs formule, D ≤ 11, j ≤ 6, 2026-06-27). N_cœur = 4P_{a+2}−4P_{a+1}+P_a
  (V-032). Mention du réseau KV (TR24-074) ajoutée — contexte honnête.
- Cipu 2004 : PDF LU EN ENTIER (2026-06-27). Sa ligne n=20 REPRODUITE
  EXACTEMENT (length 116, ‖·‖₂² 132, degré 257, hauteur 2 = ses B1/B2). Norme
  primaire = ℓ₁ (length), ℓ₂ secondaire (corrige mon « L2 » initial — 23e
  auto-correction). L'email mentionne SEULEMENT le fait vérifié (reproduction
  + complémentarité hauteur 1 vs 2) ; le lien P_j(D) (forme close exposants
  {1,2}, mineur) a été RETIRÉ de l'email pour ne pas survendre. Détails et
  délimitation : bib/cipu_2004_pointeur.md.
- Offrir le code = engagement tenable (svp non requis ; checks/task_v047 +
  task_v049 sont propres et exacts).
