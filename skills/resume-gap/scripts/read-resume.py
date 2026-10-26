#!/usr/bin/env python3
"""Print a resume's text grouped by section, with line numbers.

The line numbers matter: they are how the review says "this sits at line 7 of
TECHNICAL SKILLS, move it up" instead of vaguely gesturing at the document.

Usage:
    python3 read-resume.py resume.pdf [resume2.pdf ...]

Supports .pdf (needs pymupdf) and .docx (needs python-docx).
"""

import sys
from pathlib import Path

# Headings recognised across the layouts people actually use. Matching is
# case-insensitive and prefix-based, so "EXPERIENCE" also catches
# "EXPERIENCE & PROJECTS".
HEADINGS = [
    # English
    'SUMMARY', 'PROFILE', 'HIGHLIGHTS', 'EXPERIENCE', 'WORK EXPERIENCE',
    'EMPLOYMENT', 'PROJECTS', 'TECHNICAL SKILLS', 'SKILLS', 'EDUCATION',
    'CERTIFICATIONS', 'CERTIFICATES', 'PUBLICATIONS', 'LANGUAGES', 'AWARDS',
    'VOLUNTEER', 'INTERESTS', 'REFERENCES',
    # Turkish
    'ÖZET', 'PROFİL', 'ÖNE ÇIKANLAR', 'DENEYİM', 'İŞ DENEYİMİ', 'PROJELER',
    'TEKNİK YETKİNLİKLER', 'YETKİNLİKLER', 'BECERİLER', 'EĞİTİM',
    'SERTİFİKALAR', 'YAYINLAR', 'DİLLER', 'ÖDÜLLER', 'İLGİ ALANLARI',
    # German / French / Spanish — enough to not mangle common EU resumes
    'BERUFSERFAHRUNG', 'AUSBILDUNG', 'KENNTNISSE',
    'EXPÉRIENCE', 'FORMATION', 'COMPÉTENCES',
    'EXPERIENCIA', 'FORMACIÓN', 'HABILIDADES',
]


def pdf_lines(path):
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # older installs
        except ImportError:
            sys.exit("This file needs pymupdf:  pip3 install pymupdf")
    with pymupdf.open(path) as doc:
        return [line.strip()
                for page in doc
                for line in page.get_text().splitlines()
                if line.strip()]


def docx_lines(path):
    try:
        import docx
    except ImportError:
        sys.exit("This file needs python-docx:  pip3 install python-docx")
    document = docx.Document(path)
    lines = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    for table in document.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells if c.text.strip()]
            if cells:
                lines.append(' | '.join(cells))
    return lines


def read(path):
    suffix = Path(path).suffix.lower()
    if suffix == '.pdf':
        return pdf_lines(path)
    if suffix in ('.docx', '.docm'):
        return docx_lines(path)
    if suffix in ('.txt', '.md'):
        return [l.strip() for l in Path(path).read_text(encoding='utf-8').splitlines() if l.strip()]
    sys.exit(f"Unsupported file type: {suffix}")


def match_heading(line):
    upper = line.upper()
    for heading in HEADINGS:
        # A heading is a short line, not a sentence that happens to start with one.
        if upper.startswith(heading) and len(line) < len(heading) + 8:
            return heading
    return None


def sectioned(lines):
    section, index = 'HEADER', 0
    for line in lines:
        heading = match_heading(line)
        if heading:
            section, index = heading, 0
            continue
        yield section, index, line
        index += 1


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    for path in sys.argv[1:]:
        if not Path(path).exists():
            print(f"!! not found: {path}", file=sys.stderr)
            continue
        print(f"\n===== {path} =====")
        current = None
        for section, index, text in sectioned(read(path)):
            if section != current:
                print(f"\n--- {section} ---")
                current = section
            print(f"{index:>3}  {text}")


if __name__ == '__main__':
    main()
