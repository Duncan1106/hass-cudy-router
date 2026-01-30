from __future__ import annotations

from pathlib import Path

from custom_components.hass_cudy_router.api import CudyApi
from custom_components.hass_cudy_router.const import SENSORS, CAPABILITY_URLS

BASE = Path(__file__).resolve().parent / "html"

def read_html(model: str, name: str) -> str:
    p = BASE / model / name
    return p.read_text(encoding="utf-8", errors="ignore")

def html_exists(model: str, name: str) -> bool:
    name += ".html"
    p = BASE / model / name
    return p.is_file()

class FakeClient:
    def __init__(self, model: str) -> None:
        self._mapping = {}
        for sensor_key in SENSORS.keys():
            if html_exists(model, sensor_key):
                url = CAPABILITY_URLS[sensor_key][0]
                self._mapping[CudyApi.luci(url)] = read_html(model, f"{sensor_key}.html")

    async def get(self, path: str):
        if path in self._mapping.keys():
            return self._mapping[path]
        return ""