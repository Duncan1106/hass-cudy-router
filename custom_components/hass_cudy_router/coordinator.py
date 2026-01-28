from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class CudyCoordinator(DataUpdateCoordinator[dict[str, Any]]):

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: Any,
        host: str | None = None,
    ) -> None:
        scan_seconds = int(entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))

        super().__init__(
            hass,
            _LOGGER,
            name=f"Cudy Router ({host or entry.data.get('host', 'unknown')})",
            update_interval=timedelta(seconds=scan_seconds),
            config_entry=entry,
        )

        self.api = api
        self.data: dict[str, Any] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        if not self.api:
            raise UpdateFailed("No API client set on coordinator")

        try:
            result = await self.api.get_data()
            if result is None:
                result = {}
            if not isinstance(result, dict):
                raise UpdateFailed("API.get_data returned non-dict result")

            self.data = result
            return result
        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.debug("Error updating Cudy data: %s", err, exc_info=True)
            raise UpdateFailed(err) from err