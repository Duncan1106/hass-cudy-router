"""Validate translation files against const.SENSORS.

What it checks:
- Each sensor key defined in const.SENSORS must exist in translations under:
  entity.sensor.<key>.name
- BUTTON_REBOOT must exist under:
  entity.button.<key>.name

Run (PyCharm or CLI):
  python -m tests.translation_validator

Optional:
  python -m tests.translation_validator --langs en pl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from custom_components.hass_cudy_router.const import (
    DOMAIN,
    BUTTON_REBOOT,
    SENSORS,
    SENSORS_KEY_KEY,
)


ROOT = Path(__file__).resolve().parents[2]  # repo root (tests/..)
TRANSLATIONS_DIR = ROOT / "custom_components" / DOMAIN / "translations"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_translation_keys() -> dict[str, set[str]]:
    """Return required translation keys per platform."""
    sensor_keys: set[str] = set()

    for module_sensors in SENSORS.values():
        for spec in module_sensors:
            key = spec.get(SENSORS_KEY_KEY)
            if isinstance(key, str) and key:
                sensor_keys.add(key)

    button_keys: set[str] = {BUTTON_REBOOT}

    return {
        "sensor": sensor_keys,
        "button": button_keys,
    }


def _extract_entity_keys(translations: dict[str, Any], platform: str) -> set[str]:
    """Extract translation keys for a given platform from HA translation JSON."""
    entity = translations.get("entity")
    if not isinstance(entity, dict):
        return set()

    platform_obj = entity.get(platform)
    if not isinstance(platform_obj, dict):
        return set()

    # Expected: entity.<platform>.<translation_key> is an object (usually contains "name")
    return {k for k, v in platform_obj.items() if isinstance(k, str) and isinstance(v, dict)}


def validate_language(lang: str) -> int:
    """Validate a single language file. Returns number of hard problems."""
    path = TRANSLATIONS_DIR / f"{lang}.json"
    if not path.exists():
        print(f"❌ Missing translations file: {path}")
        return 1

    translations = _load_json(path)
    expected = expected_translation_keys()

    problems = 0

    for platform, required_keys in expected.items():
        present_keys = _extract_entity_keys(translations, platform)

        missing = sorted(required_keys - present_keys)
        extra = sorted(present_keys - required_keys)

        if missing:
            problems += len(missing)
            print(f"\n[{lang}] ❌ Missing entity.{platform} keys ({len(missing)}):")
            for k in missing:
                print(f"  - {k}")

        # Extras are a warning only (you might have legacy keys, diagnostics, etc.)
        if extra:
            print(f"\n[{lang}] ⚠️  Extra entity.{platform} keys ({len(extra)}):")
            for k in extra:
                print(f"  - {k}")

    if problems == 0:
        print(f"✅ {lang}.json OK")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate HA translations against const.SENSORS"
    )
    parser.add_argument(
        "--langs",
        nargs="*",
        default=None,
        help="Languages to validate (default: all *.json in translations dir)",
    )
    args = parser.parse_args()

    if args.langs:
        langs = args.langs
    else:
        if not TRANSLATIONS_DIR.exists():
            print(f"❌ Translations dir not found: {TRANSLATIONS_DIR}")
            return 2
        langs = sorted(p.stem for p in TRANSLATIONS_DIR.glob("*.json"))

    total_problems = 0
    for lang in langs:
        total_problems += validate_language(lang)

    if total_problems:
        print(f"\n❌ Total problems: {total_problems}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())