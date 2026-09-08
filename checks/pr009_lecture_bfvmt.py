# -*- coding: utf-8 -*-
r"""PR-009 — Lecture exécutable de Buhrman-Fortnow-van Melkebeek-Torenvliet,
« Separating complexity classes using autoreducibility » (arXiv
math/9807185 ; SICOMP 29(5), 2000) — les deux « lemmes de lecture » de
la candidature n° 6 :
  (i)  la Figure 7 (tableau des séparations « dans les deux sens »)
       contient-elle une case P ≠ NP ?
  (ii) les théorèmes positifs (4.3 / 4.4) ne valent-ils que pour un
       nombre CONSTANT de niveaux / d'alternances ?
plus les verbatims utiles à l'instruction : Post's program, oracle
access (non-relativisation), Theorem 3.1 / 4.1 / 4.2 / 5.1, Lemma 5.2.

Usage : python -u checks/pr009_lecture_bfvmt.py [chemin.pdf]
Télécharge le PDF arXiv dans le scratchpad s'il est absent, extrait le
texte (pypdf), et imprime des fenêtres de contexte autour des mots-clés.
Le texte intégral est écrit à côté du PDF (bfvmt_arxiv.txt).
"""
import os
import re
import sys
import urllib.request

URL = "https://arxiv.org/pdf/math/9807185"
MOTS = [
    "Post's Program", "Figure 7", "Figure", "Section 5",
    "Theorem 5.1", "Theorem 5.2", "Theorem 5.3", "Theorem 5.4",
    "Lemma 5.1", "Lemma 5.2", "Theorem 3.1", "Theorem 4.3",
    "Theorem 4.4", "Theorem 4.5", "Theorem 4.9",
    "constant k", "constant number", "failed to account", "recursiv",
    "alternation", "NP = NL", "NL = NP", "P = NP", "PSPACE",
    "not autoreducible", "coheren", "mitotic",
]


def extraire(pdf):
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader  # type: ignore
    r = PdfReader(pdf)
    pages = []
    for i, p in enumerate(r.pages):
        pages.append(f"\n=== PAGE {i + 1} ===\n" + (p.extract_text() or ""))
    return "".join(pages)


def main():
    scr = os.environ.get("PR009_DIR", os.path.dirname(os.path.abspath(__file__)))
    pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(scr, "bfvmt_arxiv.pdf")
    if not os.path.exists(pdf):
        print(f"téléchargement {URL} -> {pdf}", flush=True)
        urllib.request.urlretrieve(URL, pdf)
    txt_path = os.path.splitext(pdf)[0] + ".txt"
    texte = extraire(pdf)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(texte)
    print(f"{len(texte)} caractères extraits -> {txt_path}")
    # Le PDF de 1998 (polices Type 1 anciennes) rend des espaces dans les
    # mots (« T uring », « P ost ») et préfixe les chiffres par « / »
    # (« Theorem /4/./1 ») : on retire les « / » et on cherche avec des
    # motifs tolérants aux espaces entre lettres.
    plat = re.sub(r"\s+", " ", texte.replace("/", ""))

    def tolerant(phrase):
        mots = phrase.split(" ")
        return r"\s*".join(r"\s*".join(re.escape(c) for c in m) for m in mots)

    for mot in MOTS:
        occ = [m.start() for m in re.finditer(tolerant(mot), plat)]
        print(f"\n##### « {mot} » : {len(occ)} occurrence(s)")
        for k, pos in enumerate(occ[:8]):
            a, b = max(0, pos - 400), min(len(plat), pos + 700)
            print(f"  [{k + 1}] …{plat[a:b]}…")


if __name__ == "__main__":
    main()
