from __future__ import annotations

from typing import Any

from custom_components.hass_cudy_router.const import SENSOR_SYSTEM_MODEL
from custom_components.hass_cudy_router.models import SPEC_REGISTRY
from custom_components.hass_cudy_router.parser import parse_system_info

async def detect_model(client: Any) -> str:
    path = "/cgi-bin/luci/admin/system/status?detail=1"
    try:
        html = await client.get(path)
        if html:
            data = parse_system_info(html)
            if SENSOR_SYSTEM_MODEL in data.keys():
                potential_model = data[SENSOR_SYSTEM_MODEL]
                if potential_model in SPEC_REGISTRY.keys():
                    return potential_model
            return "Generic"
    except Exception:
        html = None
    if not html:
        return "Generic"
    return "Generic"