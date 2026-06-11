# Brouillon — email à Chen Shuwen (certificats PTE)

**Subject: Unconditional non-existence certificates for ideal PTE solutions (size 11 and beyond), via exact lattice enumeration**

Dear Chen Shuwen,

I came to the Prouhet-Tarry-Escott problem from an unexpected direction:
a 2024 conjecture in computational complexity (Krishan-Vishwanathan,
ECCC TR24-074) turns out to be a question about the shortest vectors of
the lattice of integer polynomials divisible by (x-1)^{k+1} — and those
shortest vectors are precisely PTE solutions. While studying it, we
obtained several results that may interest you for your tables and
survey (arXiv:2506.11429, which we read with great profit — including
your remark that AI could play a role: this work is AI-assisted, with
every claim verified by exact computation).

Our method is exact lattice enumeration (LLL + Fincke-Pohst in exact
rational arithmetic): it examines ALL solutions in a bounded window at
once, with no symmetry or parametric-form assumption. This complements
the large symmetric searches (Borwein-Lisonek-Percival; Coppersmith-
Mossinghoff-Scheinerman-Vanderkam) whose bounds are much larger but
conditional on the symmetric form. Results:

1. **Size 11 (degree 10): no ideal solution — symmetric or not — has
   all its 22 integers within a window of 111 consecutive values**
   (span <= 110). To our knowledge this is the first unconditional
   statement at this size.

2. **Tarry's 1913 size-8 solution is provably minimal**: no ideal
   solution of size 8 has span < 50 (exhaustive over [0, 49]). Your
   table's "smallest known" can be upgraded to "smallest".

3. **Escott's 1910 size-7 solution is near-optimal**: no size-7 ideal
   solution has span <= 81, so the minimal span lies in (81, 102].

4. **Sizes 13 to 50**: no ideal solution exists with span <= roughly
   (size + 19) — apparently the first certificates of any kind at
   these sizes.

5. Related to Borwein-Mossinghoff's minimal-degree problem: **no
   height-1 polynomial with a zero of order 18 at x = 1 exists with
   degree <= 96** (so the minimal degree for multiplicity 18 lies in
   [97, 262143], the upper end being Prouhet's classical solution,
   which we reconstructed and verified coefficient-by-coefficient).

One more observation related to your survey: your Conjecture 1
(interlacing of normalized solutions) suggested to us a natural
extension — that the lP-minimal MULTISET solutions in a bounded window
(the shortest lattice vectors) might also interlace, i.e. have
alternating signs. We tested this on 72 exactly-enumerated minimal
vectors across 15 cells: only 4 alternate. So while your conjecture
concerns ideal solutions (where interlacing is natural, by the
constant-difference argument), the structure does NOT extend to the
l2-minimal multiset solutions: their optima are palindromic (mirror-
symmetric multisets) rather than interlacing, with multiplicities and,
in deep windows, non-unit extreme coefficients. This delimits, we
believe, the natural boundary of the interlacing phenomenon — the data
is available if useful.

All scripts are replayable in one command (Python, exact arithmetic),
and I would be happy to share them, along with a short note. If any of
these bounds duplicate something already known, I would be grateful for
the reference.

Best regards,
Tanguy Le Mer
