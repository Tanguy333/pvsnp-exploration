# -*- coding: utf-8 -*-
r"""PR-010 — Lecture exécutable du survey d'Agrawal, « The Isomorphism
Conjecture for NP » (PDF IITK 2009 ; Computability in Context, 2011) —
les lemmes de lecture de la candidature n° 7 et les numéros qu'elle cite :
Props 3.5 / 4.1 / 6.19, Thms 6.3-6.20, Cor. 7.5, la question AC⁰[2], le
lien « barreau r ⟹ C ⊄ r », les deux conjectures rivales et P ≠ NP.

Usage : python -u checks/pr010_lecture_agrawal.py [chemin.pdf]
Télécharge le PDF dans PR010_DIR (ou à côté du script) s'il est absent,
extrait le texte (pypdf), écrit le texte intégral à côté du PDF et
imprime des fenêtres de contexte autour des mots-clés (motifs tolérants
aux espaces intra-mots).
"""
import os, re, sys, urllib.request

URL = "https://www.cse.iitk.ac.in/users/manindra/survey/Isomorphism-Conjecture.pdf"
MOTS = ["Proposition 3.5", "Proposition 4.1", "Proposition 6.19", "Theorem 6.20",
        "Theorem 6.16", "Theorem 6.15", "Theorem 6.3", "Theorem 6.4", "Theorem 7.1",
        "Corollary 7.5", "Easy Cylinder", "Goldreich", "Encrypted Complete Set",
        "either implies", "finite", "Complete Degree Conjecture", "AC0[2]",
        "TC0", "open", "one-way", "P = NP", "P 6= NP", "random oracle", "Rogers"]

def extraire(pdf):
    from pypdf import PdfReader
    r = PdfReader(pdf)
    return "".join(f"\n=== PAGE {i+1} ===\n" + (p.extract_text() or "") for i, p in enumerate(r.pages))

def main():
    scr = os.environ.get("PR010_DIR", os.path.dirname(os.path.abspath(__file__)))
    pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(scr, "agrawal_survey.pdf")
    if not os.path.exists(pdf):
        print(f"téléchargement {URL} -> {pdf}", flush=True)
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(pdf, "wb") as f:
            f.write(r.read())
    texte = extraire(pdf)
    txt = os.path.splitext(pdf)[0] + ".txt"
    open(txt, "w", encoding="utf-8").write(texte)
    print(f"{len(texte)} caractères extraits -> {txt}")
    plat = re.sub(r"\s+", " ", texte.replace("/", ""))
    def tol(ph):
        return r"\s*".join(r"\s*".join(re.escape(c) for c in m) for m in ph.split(" "))
    for mot in MOTS:
        occ = [m.start() for m in re.finditer(tol(mot), plat)]
        print(f"\n##### « {mot} » : {len(occ)} occurrence(s)")
        for k, pos in enumerate(occ[:8]):
            a, b = max(0, pos - 350), min(len(plat), pos + 650)
            print(f"  [{k+1}] …{plat[a:b]}…")

if __name__ == "__main__":
    main()
