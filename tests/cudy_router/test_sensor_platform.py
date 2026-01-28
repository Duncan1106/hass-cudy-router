import pytest
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.hass_cudy_router.const import *
from custom_components.hass_cudy_router.models import get_spec
from custom_components.hass_cudy_router.sensor import async_setup_entry


@pytest.mark.asyncio
async def test_sensor_setup_creates_entities(hass: HomeAssistant):
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "123"

    coordinator = MagicMock()
    coordinator.data = {MODULE_SYSTEM: {SENSOR_SYSTEM_FIRMWARE_VERSION: "1.0.0"}}
    coordinator.async_add_listener = MagicMock()

    spec = get_spec("WR6500")

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "spec": spec,
    }

    added = []
    def add_entities(entities):
        added.extend(entities)

    await async_setup_entry(hass, entry, add_entities)

    # At least one entity and firmware exists among them
    assert len(added) > 0
    fw = [e for e in added if e.entity_description.key == SENSOR_SYSTEM_FIRMWARE_VERSION]
    assert fw
    assert fw[0].native_value == "1.0.0"