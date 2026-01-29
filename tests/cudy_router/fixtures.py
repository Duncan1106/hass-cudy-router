from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parent / "html"

def read_html(model: str, name: str) -> str:
    p = BASE / model / name
    return p.read_text(encoding="utf-8", errors="ignore")