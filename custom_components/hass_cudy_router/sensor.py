from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import *
from .coordinator import CudyCoordinator
from .models import ModelSpec


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: CudyCoordinator = data["coordinator"]
    spec: ModelSpec = data["spec"]

    if "sensor" not in spec.platforms:
        return

    entities = [CudySensor(coordinator, entry, desc, spec) for desc in spec.sensor_descriptions]
    async_add_entities(entities)


class CudySensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CudyCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
        spec: ModelSpec,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._spec = spec
        self._entry = entry

        entry_data = getattr(entry, "data", {})
        self._host = entry_data.get("host", "") if isinstance(entry_data, dict) else ""

        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        stable_id = (
            getattr(self._entry, "unique_id", None)
            or self._host
            or getattr(self._entry, "entry_id", "")
        )

        data = getattr(self.coordinator, "data", None) or {}
        system = data.get(MODULE_SYSTEM, {}) if isinstance(data, dict) else {}

        sw_version = None
        if isinstance(system, dict):
            sw_version = system.get(SENSOR_SYSTEM_FIRMWARE_VERSION) or system.get(SENSOR_FIRMWARE_VERSION)

        return DeviceInfo(
            identifiers={(DOMAIN, stable_id)},
            name=f"Cudy Router ({self._host})" if self._host else "Cudy Router",
            manufacturer="Cudy",
            model=self._spec.model,
            sw_version=sw_version,
        )

    @property
    def native_value(self) -> Any:
        data = getattr(self.coordinator, "data", None) or {}
        key = self.entity_description.key

        for prefix, module in self._spec.module_map.items():
            if key.startswith(prefix):
                module_data = data.get(module, {})
                if isinstance(module_data, dict):
                    return module_data.get(key)
                return None

        return data.get(key)