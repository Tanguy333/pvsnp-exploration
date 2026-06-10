# Brouillon — email à Krishan & Vishwanathan (test V-004 de leur Conjecture 5)

> **Pour Tanguy** : à envoyer sous ton identité, comme pour Göös. Les
> adresses des auteurs sont sur la page ECCC du rapport
> (https://eccc.weizmann.ac.il/report/2024/074/) — Vaibhav Krishan et
> Sundar Vishwanathan (IIT Bombay au moment de la publication). L'email
> est en anglais, factuel, court, avec divulgation de l'assistance IA
> (même standard d'honnêteté que pour Göös). Le script peut être joint
> (`checks/task_v004_kv_conjecture5.py`, ~150 lignes, numpy seul).

---

**Subject:** Computational verification of Conjecture 5 in your ECCC
TR24-074 (torus polynomials)

Dear Dr. Krishan, dear Prof. Vishwanathan,

My name is Tanguy Le Mer. I studied mathematics and algorithmic
complexity in classe préparatoire and at the University of Poitiers
(France), and I maintain a small research-exploration repository on
circuit lower bounds.

I read with great interest your ECCC report TR24-074, "Towards ACC Lower
Bounds using Torus Polynomials". Since your Conjecture 5 — that the
lattice L(B) always contains a shortest (ℓ2) vector γ with γ_n = 1 — is
a concrete statement about an explicit integer lattice, I tested it
computationally at small sizes, and I thought the outcome might be of
interest to you.

**Setup.** I built the basis B (columns = shifted alternating binomial
stencils, B[i,k] = (−1)^{i−k} · C(d+1, i−k)), reduced it with LLL
(δ = 0.99), and then ran a Fincke–Pohst enumeration that provably finds
ALL lattice vectors of minimal ℓ2 norm, with final norms verified in
exact integer arithmetic.

**Result.** For every pair (n, d) with n = 6..20 and d up to min(9, n−3)
— 109 cells in total — there is always a shortest vector with |γ_n| = 1
(equivalently γ_n = 1 up to global sign). The sets {|γ_n|} over all
minimal vectors were always {1} or {0, 1}, never excluding 1. So your
Conjecture 5 holds on this entire range.

**A structural remark.** The minimal vectors do not look like
(integer) Chebyshev-type dual certificates: their supports have holes,
signs do not strictly alternate, and they correlate weakly with the
optimal LP duals of the corresponding torus programs. Instead they
appear to be quasi-palindromic arrangements of small finite-difference
bumps (motifs like (−1, 2, −1) spread along the window), with the
shift-invariance of the stencil lattice clearly visible among the
minimizers.

**A small quantitative observation.** The minimal squared norms are much
smaller than the single-stencil value C(2d+2, d+1): for instance 18
versus 924 at (n, d) = (16, 5), and 1716 versus 12870 at (10, 7). Integer
combinations compress the stencils substantially — considerably below
what the Minkowski-type bound in your Lemma 3.9 would suggest at these
sizes. I do not know whether this helps, but the measured gap seemed
worth reporting.

**Caveats.** These are small sizes — far from the regime d ~ √n·polylog(n)
relevant to your program — so this is empirical support only, of course
not a proof. I should also disclose that this exploration was carried out
with the help of an AI assistant (Anthropic's Claude) in a
verify-everything-by-exact-computation workflow; every claim above rests
on exact integer arithmetic, and I am happy to share the short Python
script (numpy only) if useful.

Thank you for your work — the reduction of torus lower bounds to a
shortest-vector statement is a beautiful and very testable formulation.

Best regards,
Tanguy Le Mer

---

> **Note interne** : si réponse, l'archiver dans `tours/` ou `bib/` et
> mettre à jour le statut de V-004 (appui empirique → éventuellement
> mentionné par les auteurs).
