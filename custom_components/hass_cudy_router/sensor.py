from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import *
from .coordinator import CudyCoordinator


@dataclass(frozen=True)
class _SensorDef:
    module: str
    key: str
    icon: str | None
    entity_category: Any | None
    state_class: Any | None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: CudyCoordinator = data["coordinator"]
    entities: list[CudySensor] = []
    modules: dict[str, dict[str, Any]] = coordinator.data or {}
    for module_name, module_data in modules.items():
        if module_name == MODULE_DEVICE_LIST:
            continue
        sensor_defs = SENSORS.get(module_name, [])
        if not isinstance(module_data, dict) or not sensor_defs:
            continue
        for sd in sensor_defs:
            sensor_key = sd.get(SENSORS_KEY_KEY)
            if not sensor_key:
                continue

            if sensor_key not in module_data:
                continue
            entities.append(
                CudySensor(
                    coordinator=coordinator,
                    entry=entry,
                    sensor_def=_SensorDef(
                        module=module_name,
                        key=sensor_key,
                        icon=sd.get(SENSORS_KEY_ICON),
                        entity_category=sd.get(SENSORS_KEY_CATEGORY),
                        state_class=sd.get(SENSORS_KEY_CLASS),
                    ),
                )
            )

    async_add_entities(entities)


class CudySensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: CudyCoordinator, entry: ConfigEntry, sensor_def: _SensorDef) -> None:
        self.coordinator = coordinator
        self._entry = entry
        self._def = sensor_def

        self._attr_unique_id = f"{entry.entry_id}_{sensor_def.key}"
        self._attr_icon = sensor_def.icon
        self._attr_entity_category = sensor_def.entity_category
        self._attr_state_class = sensor_def.state_class

    @property
    def available(self) -> bool:
        return getattr(self.coordinator, "last_update_success", True)

    @property
    def native_value(self) -> Any:
        data = self.coordinator.data or {}
        module = data.get(self._def.module, {})
        if not isinstance(module, dict):
            return None
        return module.get(self._def.key)

    async def async_added_to_hass(self) -> None:
        self.coordinator.async_add_listener(self.async_write_ha_state)