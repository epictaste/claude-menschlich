# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## [1.0.0] · 2026-07-15

### Hinzugefügt
- `menschlich`-Skill: entschlackt deutsche Artikel und Fließtexte von AI-Slop-Mustern (Em-Dashes, Kontrast-Parallelismus, Dreier-Listen, hohle Überschriften, Floskeln, Füllwörter, erfundene Zahlen).
- `scripts/slop_check.py`: mechanischer Slop-Check für Markdown (inkl. Frontmatter), Exit 1 bei blockierenden Findings.
- Deutsche Muster-Referenz in `references/banned-list.md`.
- Installierbar als Claude-Code-Plugin, via Agent-Skills-CLI und manuell.
- Selbsttest + CI (pytest).
