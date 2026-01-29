from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .client import CudyClient
from .coordinator import CudyCoordinator
from .api import CudyApi
from .models import get_spec


class CudyIntegration:
    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: CudyClient,
        spec,
    ) -> None:
        self.hass = hass
        self.entry = entry
        self.client = client
        self.spec = spec

        self.api = CudyApi(client, spec)
        self.coordinator = CudyCoordinator(
            hass=hass,
            entry=entry,
            api=self.api,
            host=entry.data.get("host"),
        )

    async def async_setup(self) -> None:
        await self.coordinator.async_config_entry_first_refresh()


async def create_model_integration(
    model: str,
    hass: HomeAssistant,
    entry: ConfigEntry,
    client: CudyClient,
) -> CudyIntegration:
    spec = get_spec(model)

    integration = CudyIntegration(hass, entry, client, spec)
    await integration.async_setup()
    return integration