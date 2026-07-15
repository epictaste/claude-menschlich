#!/usr/bin/env python3
"""Mechanischer Slop-Check für den menschlich-Skill.

Prüft Markdown-Artikel (inkl. Frontmatter) auf die maschinell erkennbaren
AI-Slop-Muster aus SKILL.md + references/banned-list.md. Ersetzt NICHT das
Lesen (Ton, Colon-Setups, fabrizierte Zitate bleiben Handarbeit), macht aber
die harten Regeln prüfbar.

Aufruf:
    python3 slop_check.py <datei.md> [...]      # Exit 1 bei ERROR-Findings
    python3 slop_check.py --dir <ordner>        # alle .md rekursiv
"""

import re
import sys
import statistics
from pathlib import Path

# ERROR = blockierend (Regel aus SKILL.md verletzt)
BANNED_EXACT = [
    # Floskel-Opener / Übergänge / Schluss (banned-list.md, deutsch)
    "In der heutigen schnelllebigen Welt", "In der heutigen digitalen Welt",
    "Es ist wichtig zu beachten", "Es ist wichtig zu verstehen",
    "Zusammenfassend lässt sich sagen", "Am Ende des Tages",
    "Darüber hinaus", "Des Weiteren", "Nichtsdestotrotz",
    "Es sei angemerkt", "Um es einfach zu sagen",
    "Lass uns eintauchen", "Lass uns einen Blick werfen",
    "Tauche ein in", "Entdecke die Welt von",
    "In diesem Artikel", "Im Folgenden zeige ich",
    # Kicker-Opener (Quelle: no_ai_slop CLAUDE.md, deutsch)
    "Aber jetzt kommt der Clou", "Und genau hier wird es spannend",
    "Aber hier ist der Haken", "Und das Beste daran",
    # Hype (artikel.md 5.2b)
    "Game-Changer", "game-changer", "revolutionär", "bahnbrechend",
    "nahtlos", "mühelos",
]
# 100%-KI-Indikatoren (halluzinierte Markup-Reste)
MARKUP_TOKENS = ["oaicite", "contentReference", "grok_card", "attributableIndex", "turn0search"]

# WARN = prüfen, kann legitim sein
FILLER_WORDS = [
    "eigentlich", "im Grunde", "letztlich", "letzten Endes", "quasi",
    "sozusagen", "regelrecht", "geradezu", "unglaublich", "enorm",
]

CONTRAST_RE = re.compile(
    r"(?:[Ee]s ist nicht [^.]{3,60}, (?:es ist|sondern))"
    r"|(?:[Nn]icht nur [^.]{3,60}, sondern (?:auch )?)"
    r"|(?:[Dd]as ist kein [^.]{3,60}, das ist)"
)
QUESTION_PAIR_RE = re.compile(r"\?\s+Und wenn (?:ja|nein|doch)")


def check_file(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors, warns = [], []

    n = text.count("—")
    if n:
        errors.append(f'{n}x Em-Dash (verboten, auch im Frontmatter)')

    for phrase in BANNED_EXACT:
        if phrase in text:
            errors.append(f'verbotene Phrase: {phrase}')

    for tok in MARKUP_TOKENS:
        if tok in text:
            errors.append(f"halluzinierter Markup-Rest: {tok}")

    for m in CONTRAST_RE.finditer(text):
        errors.append(f'Kontrast-Parallelismus: {m.group(0)[:60]}')

    if QUESTION_PAIR_RE.search(text):
        warns.append("rhetorisches KI-Fragenpaar (...? Und wenn ja ...)")

    body = text.split("---", 2)[2] if text.startswith("---") else text
    # HTML-Kommentare (Prüfprotokoll) nicht in Stil-Statistik zählen
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

    for w in FILLER_WORDS:
        c = len(re.findall(rf"\b{re.escape(w)}\b", body, re.I))
        if c >= 2:
            warns.append(f'Füllwort {w} {c}x (Beleg oder streichen)')

    paras = [p for p in body.split("\n\n") if len(p.strip()) > 0
             and not p.strip().startswith(("#", "-", "1.", "2.", "3.", "4.", "```", ">", "👉", "|", "!"))]
    one_liners = [p for p in paras if len(p.split()) <= 6]
    if len(one_liners) >= 3:
        warns.append(f"{len(one_liners)} Ein-Zeilen-Drama-Absätze (Rhythmus-Trick, max 1-2)")
    lens = [len(p.split()) for p in paras if len(p.split()) > 10]
    if len(lens) >= 4 and statistics.pstdev(lens) / (statistics.mean(lens) or 1) < 0.25:
        warns.append("monotone Absatzlängen (Abweichung <25%): Rhythmus brechen")

    return errors, warns


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] == "--dir":
        files = sorted(Path(args[1]).rglob("*.md"))
    else:
        files = [Path(a) for a in args]
    if not files:
        print(__doc__)
        return 2

    had_error = False
    for f in files:
        errors, warns = check_file(f)
        if not errors and not warns:
            print(f"OK    {f.name}")
            continue
        print(f"{'FAIL' if errors else 'WARN'}  {f.name}")
        for e in errors:
            print(f"      ERROR: {e}")
        for w in warns:
            print(f"      warn:  {w}")
        had_error = had_error or bool(errors)
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
