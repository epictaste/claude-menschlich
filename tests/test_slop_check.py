"""Selbsttest für den Slop-Check. Läuft in CI und lokal via `pytest -q`."""
import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "menschlich" / "scripts" / "slop_check.py"
_spec = importlib.util.spec_from_file_location("slop_check", _SCRIPT)
slop_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(slop_check)


def _write(tmp_path, text):
    f = tmp_path / "x.md"
    f.write_text(text, encoding="utf-8")
    return f


def test_clean_text_passes(tmp_path):
    clean = "Ich hab das getestet. Es lief gut, und ich zeig dir warum.\n\nMehr gibts nicht zu sagen."
    errors, _ = slop_check.check_file(_write(tmp_path, clean))
    assert errors == []


def test_em_dash_is_error(tmp_path):
    errors, _ = slop_check.check_file(_write(tmp_path, "Das ist gut — sehr gut sogar."))
    assert any("Em-Dash" in e for e in errors)


def test_banned_phrase_is_error(tmp_path):
    errors, _ = slop_check.check_file(_write(tmp_path, "In der heutigen schnelllebigen Welt zählt Tempo."))
    assert any("verbotene Phrase" in e for e in errors)


def test_contrast_parallelism_is_error(tmp_path):
    errors, _ = slop_check.check_file(_write(tmp_path, "Nicht nur schnell, sondern auch billig war das."))
    assert any("Kontrast-Parallelismus" in e for e in errors)


def test_hallucinated_markup_is_error(tmp_path):
    errors, _ = slop_check.check_file(_write(tmp_path, "Quelle oaicite steht hier."))
    assert any("Markup-Rest" in e for e in errors)
