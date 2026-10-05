#!/usr/bin/env python3
"""Short public extract of the course: cover, contents, chapter 1, bibliography.

usage: make_extract.py FULL.pdf EXTRACT.pdf COVER.jpg

Pages are located from the text of the compiled PDF:
  - cover: page 1;
  - contents: the page whose heading is "Table des matieres" and the
    continuation pages carrying the running header "Table des matieres <roman>";
  - chapter 1: from the page whose first line is "1" (chapter opening page)
    to the page before the one whose first line is "2";
  - bibliography: from the first page after the contents whose first line
    starts with "Bibliographie" up to the last page.
Requires poppler-utils (pdfinfo, pdftotext, pdftoppm) and qpdf.
"""
import re
import subprocess
import sys


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def main(src, out, cover):
    n = int(re.search(r"Pages:\s+(\d+)", run("pdfinfo", src)).group(1))
    lines = {}
    for i in range(1, n + 1):
        txt = run("pdftotext", "-layout", "-f", str(i), "-l", str(i), src, "-")
        lines[i] = [l.strip() for l in txt.splitlines() if l.strip()]

    heading = re.compile(r"^Table des mati[eè]res$", re.I)
    running = re.compile(r"^Table des mati[eè]res\s+[ivxlc]+$", re.I)

    toc_first = next(i for i in range(2, n + 1) if lines[i] and heading.match(lines[i][0]))
    toc_last = toc_first
    while toc_last + 1 <= n and lines[toc_last + 1] and running.match(lines[toc_last + 1][0]):
        toc_last += 1

    def chapter_start(k, after):
        return next(i for i in range(after, n + 1) if lines[i] and lines[i][0] == str(k))

    ch1_first = chapter_start(1, toc_last + 1)
    ch2_first = chapter_start(2, ch1_first + 1)

    bib_first = next(
        i for i in range(toc_last + 1, n + 1)
        if lines[i] and re.match(r"^Bibliographie\b", lines[i][0], re.I)
    )

    pages = (
        [1]
        + list(range(toc_first, toc_last + 1))
        + list(range(ch1_first, ch2_first))
        + list(range(bib_first, n + 1))
    )
    print("extract pages:", pages, "of", n)
    spec = ",".join(str(p) for p in pages)
    subprocess.run(["qpdf", "--empty", "--pages", src, spec, "--", out], check=True)

    prefix = cover[:-4] if cover.endswith(".jpg") else cover
    subprocess.run(
        ["pdftoppm", "-jpeg", "-jpegopt", "quality=86", "-scale-to-x", "520",
         "-scale-to-y", "-1", "-f", "1", "-l", "1", "-singlefile", src, prefix],
        check=True,
    )


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
