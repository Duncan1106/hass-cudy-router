from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Tuple


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _load_specs_translation_keys() -> dict[str, set[str]]:
    from custom_components.hass_cudy_router import models as model_pkg

    # Fetch registry - support different implementations
    registry = None
    for attr in ("_SPEC_REGISTRY", "SPEC_REGISTRY", "REGISTRY"):
        if hasattr(model_pkg, attr):
            registry = getattr(model_pkg, attr)
            break

    # If the model package exposes a getter, prefer it
    if hasattr(model_pkg, "get_all_specs"):
        specs = model_pkg.get_all_specs()
        # could be list or dict
        if isinstance(specs, dict):
            registry = specs
        else:
            registry = {s.model: s for s in specs}

    if not isinstance(registry, dict) or not registry:
        raise RuntimeError(
            "Could not locate ModelSpec registry. "
            "Expected model.py/model package to expose _SPEC_REGISTRY or get_all_specs()."
        )

    model_to_keys: dict[str, set[str]] = {}
    for model_name, spec in registry.items():
        keys: set[str] = set()
        for desc in getattr(spec, "sensor_descriptions", ()) or ():
            tk = getattr(desc, "translation_key", None)
            # If translation_key is not set, HA will not translate this entity by translation_key
            if tk:
                keys.add(str(tk))
        model_to_keys[str(model_name)] = keys

    return model_to_keys


def _translation_sensor_keys(translations: dict[str, Any]) -> set[str]:
    entity = translations.get("entity", {})
    sensor = entity.get("sensor", {})
    if isinstance(sensor, dict):
        return set(sensor.keys())
    return set()


def _compare(
    lang: str,
    used: set[str],
    present: set[str],
) -> Tuple[set[str], set[str]]:
    missing = used - present
    unused = present - used
    return missing, unused


def main() -> int:
    root = _repo_root()
    translations_dir = root / "custom_components" / "hass_cudy_router" / "translations"
    en_path = translations_dir / "en.json"
    pl_path = translations_dir / "pl.json"

    try:
        model_to_keys = _load_specs_translation_keys()
    except Exception as e:
        print(f"[ERROR] Could not load ModelSpec translation keys: {e}")
        return 2

    all_used_keys: set[str] = set().union(*model_to_keys.values())

    # Load translations
    try:
        en = _load_json(en_path)
    except Exception as e:
        print(f"[ERROR] Failed reading {en_path}: {e}")
        return 2

    try:
        pl = _load_json(pl_path)
    except Exception as e:
        print(f"[ERROR] Failed reading {pl_path}: {e}")
        return 2

    en_keys = _translation_sensor_keys(en)
    pl_keys = _translation_sensor_keys(pl)

    en_missing, en_unused = _compare("en", all_used_keys, en_keys)
    pl_missing, pl_unused = _compare("pl", all_used_keys, pl_keys)

    print("=== Translation validation (based on ModelSpec.sensor_descriptions.translation_key) ===")
    print(f"Models loaded: {len(model_to_keys)}")
    for m, ks in sorted(model_to_keys.items()):
        print(f"  - {m}: {len(ks)} translation_key(s)")
    print(f"TOTAL translation_key(s) used by sensors: {len(all_used_keys)}")
    print()

    def dump(title: str, items: set[str]) -> None:
        print(title)
        if not items:
            print("  (none)")
            return
        for k in sorted(items):
            print(f"  - {k}")

    print(f"[en.json] entries: {len(en_keys)}")
    dump("[en.json] MISSING keys (used by sensors, not present in translations):", en_missing)
    dump("[en.json] UNUSED keys (present in translations, not used by any sensor):", en_unused)
    print()

    print(f"[pl.json] entries: {len(pl_keys)}")
    dump("[pl.json] MISSING keys (used by sensors, not present in translations):", pl_missing)
    dump("[pl.json] UNUSED keys (present in translations, not used by any sensor):", pl_unused)
    print()

    # Helpful hint: warn if any SensorEntityDescription still has name= set (won't translate)
    # We can't reliably detect name in HA entity UI, but we can flag descriptions that set name.
    try:
        from custom_components.hass_cudy_router import model as model_pkg  # noqa: F401
        registry = getattr(model_pkg, "_SPEC_REGISTRY", {})
        named = []
        for model_name, spec in registry.items():
            for desc in getattr(spec, "sensor_descriptions", ()) or ():
                if getattr(desc, "translation_key", None) and getattr(desc, "name", None):
                    named.append((model_name, desc.translation_key, desc.name))
        if named:
            print("WARNING: Some SensorEntityDescriptions set both translation_key and name.")
            print("         If name is set, HA may show the literal name instead of translation.")
            for m, tk, nm in named:
                print(f"  - {m}: {tk} has name='{nm}'")
            print()
    except Exception:
        pass

    if en_missing or pl_missing:
        print("RESULT: ❌ Missing translation keys found.")
        return 1

    print("RESULT: ✅ OK (no missing keys).")
    return 0


if __name__ == "__main__":
    sys.exit(main())