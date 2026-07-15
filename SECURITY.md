# Sicherheit

## Sicherheitsmodell

`menschlich` ist ein Agent-Skill plus ein lokales Python-Skript (`slop_check.py`). Das Skript liest Markdown-Dateien, die du ihm übergibst, und gibt eine Textausgabe zurück. Es macht keine Netzwerkzugriffe, schreibt keine Dateien und braucht keine Secrets oder API-Keys.

- **Keine externen Aufrufe.** Reine lokale Textanalyse mit der Python-Standardbibliothek.
- **Keine Secrets.** Es gibt nichts zu hinterlegen.
- **Nur Lesezugriff.** Das Skript verändert deine Dateien nicht; das Umschreiben macht der Agent, und du gibst es frei.

## Schwachstelle melden

Bitte melde Sicherheitsprobleme über die **GitHub Security Advisories** dieses Repos (Tab „Security" → „Report a vulnerability"), nicht als öffentliches Issue. Ich melde mich zeitnah zurück.
