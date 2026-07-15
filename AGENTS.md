# AGENTS.md

Orientierung für Agenten (und Menschen), die in diesem Repo arbeiten.

## Was das hier ist

`menschlich` ist ein Agent-Skill, der AI-Slop aus deutschen Texten rausnimmt, bevor sie veröffentlicht werden. Die deutsche Variante der Idee aus [realrossmanngroup/no_ai_slop_writing_rules](https://github.com/realrossmanngroup/no_ai_slop_writing_rules). Eigenständig auf Deutsch geschrieben, inspiriert von deren Ansatz.

## Struktur

```
skills/menschlich/
  SKILL.md                  # der Skill: Marker, Prozess, Deutsch-Spezifika
  references/banned-list.md # deutsche Muster-Referenz zum Nachschlagen
  scripts/slop_check.py     # mechanischer Slop-Check (Markdown, Exit 1 blockiert)
tests/test_slop_check.py    # Selbsttest (CI)
.claude-plugin/             # Claude-Code-Plugin- + Marketplace-Manifest
.codex-plugin/              # Codex/Agents-Manifest (skills + interface)
```

Der Skill ist ein self-contained Ordner unter `skills/menschlich/`. SKILL.md, references/ und scripts/ gehören als Einheit zusammen.

## Commands

```bash
python3 skills/menschlich/scripts/slop_check.py <datei.md>      # eine Datei prüfen
python3 skills/menschlich/scripts/slop_check.py --dir <ordner>  # rekursiv
python3 -m pytest -q                                            # Selbsttest
```

## Regeln

- **Deutsch, echte Umlaute** (ä ö ü ß), nie ae/oe/ue/ss.
- **Kein Em-Dash „—"** im Repo-Text selbst (der Skill prüft ja genau darauf).
- **Nichts aus dem Quell-Repo 1:1 kopieren**, es hat keine Lizenz. Nur eigenständige deutsche Formulierungen. Englische Wortlisten bleiben verlinkt, nicht gespiegelt.
- Version in `.claude-plugin/plugin.json` und `.codex-plugin/plugin.json` synchron halten.
