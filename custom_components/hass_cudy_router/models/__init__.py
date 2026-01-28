from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import SensorEntityDescription
from custom_components.hass_cudy_router.const import *

ParserFn = Callable[[str], dict[str, Any]]
DeviceListParserFn = Callable[[str], list[dict[str, Any]]]


@dataclass(frozen=True)
class ModelSpec:
    model: str
    pages: dict[str, str]
    parsers: dict[str, ParserFn]
    device_list_page: str | None
    device_list_parser: DeviceListParserFn | None
    platforms: set[str]
    supports_reboot: bool
    module_map: dict[str, str]
    sensor_descriptions: tuple[SensorEntityDescription, ...]


SPEC_REGISTRY: dict[str, ModelSpec] = {}


def register_spec(spec: ModelSpec) -> None:
    SPEC_REGISTRY[spec.model] = spec


def get_spec(model: str) -> ModelSpec:
    if model in SPEC_REGISTRY:
        return SPEC_REGISTRY[model]
    if "Generic" in SPEC_REGISTRY:
        return SPEC_REGISTRY["Generic"]
    raise ValueError(f"No ModelSpec registered for '{model}' and no Generic fallback")


def build_module_map() -> dict[str, str]:
    return {
        "info_": MODULE_INFO,
        "system_": MODULE_SYSTEM,
        "mesh_": MODULE_MESH,
        "lan_": MODULE_LAN,
        "wan_": MODULE_WAN,
        "24g_": MODULE_WIRELESS_24G,
        "5g_": MODULE_WIRELESS_5G,
        "dhcp_": MODULE_DHCP,
        "gsm_": MODULE_GSM,
        "sms_": MODULE_SMS,
        "device_": MODULE_DEVICES,
    }

from . import Generic
from . import P5
from . import R700
from . import WR6500