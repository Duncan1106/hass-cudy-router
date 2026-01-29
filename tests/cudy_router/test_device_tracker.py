from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.hass_cudy_router.const import *
from custom_components.hass_cudy_router.device_tracker import (
    async_setup_entry,
    CudyDeviceTracker,
)
from custom_components.hass_cudy_router.models import get_spec


@pytest.fixture
def coordinator() -> MagicMock:
    c = MagicMock()
    c.host = "192.168.0.1"
    c.last_update_success = True
    c.data = {}
    return c


def _set_devices(coordinator: MagicMock, devices: list[dict[str, Any]]) -> None:
    coordinator.data = {
        MODULE_DEVICES: {
            OPTIONS_DEVICE_LIST: devices,
        }
    }


@pytest.mark.asyncio
async def test_async_setup_entry_adds_entities(
    hass: HomeAssistant, coordinator: MagicMock
):
    entry = MagicMock()
    entry.entry_id = "test_entry"

    spec = get_spec("WR6500")

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "spec": spec,
    }

    _set_devices(
        coordinator,
        [
            {DEVICE_MAC: "AA:BB:CC:DD:EE:FF"},
            {DEVICE_MAC: "11-22-33-44-55-66"},
        ],
    )

    added: list[Any] = []

    def add_entities(entities) -> None:
        added.extend(entities)

    await async_setup_entry(hass, entry, add_entities)

    assert len(added) == 2
    assert all(isinstance(e, CudyDeviceTracker) for e in added)

    assert added[0].mac_address == "AA:BB:CC:DD:EE:FF"
    assert added[1].mac_address == "11-22-33-44-55-66"


def test_tracker_available_reflects_coordinator_state(coordinator: MagicMock):
    tracker = CudyDeviceTracker(
        coordinator,
        MagicMock(entry_id="x"),
        {DEVICE_MAC: "AA"},
    )

    coordinator.last_update_success = True
    assert tracker.available is True

    coordinator.last_update_success = False
    assert tracker.available is False


def test_tracker_is_connected_wired_true(coordinator: MagicMock):
    _set_devices(
        coordinator,
        [
            {
                DEVICE_MAC: "AA",
                DEVICE_CONNECTION_TYPE: "wired",
            }
        ],
    )

    tracker = CudyDeviceTracker(
        coordinator,
        MagicMock(entry_id="x"),
        {DEVICE_MAC: "AA"},
    )
    assert tracker.is_connected is True


def test_tracker_is_connected_wifi_true(coordinator: MagicMock):
    _set_devices(
        coordinator,
        [
            {
                DEVICE_MAC: "AA",
                DEVICE_CONNECTION_TYPE: "wifi"
            }
        ],
    )

    tracker = CudyDeviceTracker(
        coordinator,
        MagicMock(entry_id="x"),
        {DEVICE_MAC: "AA"},
    )
    assert tracker.is_connected is True


def test_tracker_is_connected_missing_device_false(coordinator: MagicMock):
    _set_devices(
        coordinator,
        [
            {DEVICE_MAC: "BB", DEVICE_CONNECTION_TYPE: "wired"},
        ],
    )

    tracker = CudyDeviceTracker(
        coordinator,
        MagicMock(entry_id="x"),
        {DEVICE_MAC: "AA"},
    )
    assert tracker.is_connected is False


def test_extra_state_attributes_returns_device_dict(coordinator: MagicMock):
    device = {
        DEVICE_MAC: "AA",
        DEVICE_CONNECTION_TYPE: "wifi",
        "hostname": "Phone",
        "ip": "192.168.0.50",
    }

    _set_devices(coordinator, [device])

    tracker = CudyDeviceTracker(
        coordinator,
        MagicMock(entry_id="x"),
        device,
    )

    assert tracker.extra_state_attributes == device